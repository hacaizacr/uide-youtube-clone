from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, func
from typing import List
import random

from database import get_session, init_db
from models import Video, Category, Comment, User
from s3_service import upload_file_to_s3

import os
from dotenv import load_dotenv

# Esto busca el archivo .env y carga las variables en el sistema
load_dotenv()

# Ahora puedes usarlas así:
db_host = os.getenv("DB_HOST")
db_pass = os.getenv("DB_PASS")

app = FastAPI(title="YouTube Clon API - Cloud Architecture")

# Configuración obligatoria de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia esto por la IP pública o dominio del Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# --- ENDPOINTS DE VIDEOS ---

@app.get("/videos", response_model=List[Video])
def get_all_videos(session: Session = Depends(get_session)):
    return session.exec(select(Video)).all()

@app.get("/videos/{video_id}", response_model=Video)
def get_video_by_id(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    # Incrementar vistas de forma simple
    video.views += 1
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

@app.get("/videos/search/", response_model=List[Video])
def search_videos(q: str, session: Session = Depends(get_session)):
    statement = select(Video).where(Video.title.contains(q))
    return session.exec(statement).all()

@app.get("/videos/category/{category_id}/recommendations", response_model=List[Video])
def get_recommendations_by_category(category_id: int, current_video_id: int, session: Session = Depends(get_session)):
    # Trae 10 videos aleatorios de la misma categoría excluyendo el actual
    statement = select(Video).where(Video.category_id == category_id, Video.id != current_video_id)
    videos = session.exec(statement).all()
    return random.sample(videos, min(len(videos), 10))

@app.post("/videos/upload")
def upload_video(
    title: str = Form(...),
    description: str = Form(None),
    user_id: int = Form(...),
    category_id: int = Form(...),
    video_file: UploadFile = File(...),
    thumbnail_file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    video_url = upload_file_to_s3(video_file, "videos")
    thumbnail_url = upload_file_to_s3(thumbnail_file, "miniaturas")
    
    new_video = Video(
        title=title,
        description=description,
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        user_id=user_id,
        category_id=category_id
    )
    session.add(new_video)
    session.commit()
    session.refresh(new_video)
    return {"message": "Video subido con éxito", "video": new_video}

# --- ENDPOINTS DE COMENTARIOS ---

@app.get("/videos/{video_id}/comments")
def get_comments(video_id: int, session: Session = Depends(get_session)):
    statement = select(Comment).where(Comment.video_id == video_id)
    return session.exec(statement).all()

@app.post("/comments")
def create_comment(comment: Comment, session: Session = Depends(get_session)):
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, session: Session = Depends(get_session)):
    db_comment = session.get(Comment, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    session.delete(db_comment)
    session.commit()
    return {"detail": "Comentario eliminado"}

# --- ENDPOINTS DE CATEGORÍAS ---
@app.get("/categories", response_model=List[Category])
def list_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()

# --- ENDPOINTS DE USUARIOS (Nuevos) ---

@app.post("/users", response_model=User)
def register_user(user: User, session: Session = Depends(get_session)):
    """Crea un nuevo usuario (Requisito: Registro)"""
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user_profile(user_id: int, session: Session = Depends(get_session)):
    """Obtiene datos de un usuario (Requisito: Perfil público)"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.get("/users/{user_id}/videos", response_model=List[Video])
def get_videos_by_user(user_id: int, session: Session = Depends(get_session)):
    """Lista los videos subidos por un usuario específico"""
    statement = select(Video).where(Video.user_id == user_id)
    return session.exec(statement).all()


# --- ENDPOINTS DE CATEGORÍAS (Actualizado) ---

@app.post("/categories", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    """Crea una nueva categoría de video"""
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@app.get("/categories/{category_id}/videos", response_model=List[Video])
def get_videos_by_category(category_id: int, session: Session = Depends(get_session)):
    """Filtra y devuelve todos los videos de una categoría"""
    statement = select(Video).where(Video.category_id == category_id)
    return session.exec(statement).all()