import { useState, useEffect } from 'react';
import { Video } from './interfaces/video.interface';
import './index.css';

const API_URL = "http://34.237.142.30:8000";

function App() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);

  // 1. Cargar videos desde el Backend en AWS
  useEffect(() => {
    fetch(`${API_URL}/videos`)
      .then(res => res.json())
      .then(data => {
        setVideos(data);
        if (data.length > 0) setSelectedVideo(data[0]); // Selecciona el primero por defecto
      })
      .catch(err => console.error("Error cargando videos:", err));
  }, []);

  return (
    <div className="app-container">
      {/* Barra de Navegación */}
      <nav className="navbar">
        <div className="logo">YouTube Clone</div>
        <input type="text" placeholder="Buscar..." className="search-input" />
        <div className="user-avatar">H</div>
      </nav>

      <div className="main-layout">
        {/* Lado Izquierdo: Reproductor y Detalles */}
        <main className="video-section">
          {selectedVideo ? (
            <>
              <div className="player-wrapper">
                <video 
                  controls 
                  autoPlay 
                  key={selectedVideo.video_url} // Importante para que cambie el video al hacer clic
                  src={selectedVideo.video_url} 
                  className="main-video"
                />
              </div>
              <div className="video-details">
                <h1>{selectedVideo.title}</h1>
                <div className="stats">
                  <span>{selectedVideo.views} visualizaciones</span> • 
                  <span>{new Date(selectedVideo.created_at).toLocaleDateString()}</span>
                </div>
                <p className="description">{selectedVideo.description}</p>
              </div>
            </>
          ) : (
            <p>Cargando video...</p>
          )}
        </main>

        {/* Lado Derecho: Lista de Recomendados */}
        <aside className="recommendations">
          <h3>Siguientes</h3>
          {videos.map((video) => (
            <div 
              key={video.id} 
              className={`mini-card ${selectedVideo?.id === video.id ? 'active' : ''}`}
              onClick={() => setSelectedVideo(video)}
            >
              <img src={video.thumbnail_url} alt={video.title} />
              <div className="mini-info">
                <h4>{video.title}</h4>
                <p>{video.views} vistas</p>
              </div>
            </div>
          ))}
        </aside>
      </div>
    </div>
  );
}

export default App;