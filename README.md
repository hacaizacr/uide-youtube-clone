YouTube Clone - Cloud Architecture Project
Este proyecto es un clon funcional de YouTube desarrollado como parte del curso de Arquitectura de Computadoras en la UIDE. La aplicación permite la gestión de videos, usuarios y comentarios, integrando una arquitectura robusta en la nube utilizando Amazon Web Services (AWS).

🚀 Tecnologías Utilizadas
Backend: Python con FastAPI y SQLModel.

Frontend: React con TypeScript, Vite y Tailwind CSS.

Base de Datos: PostgreSQL alojado en Amazon RDS.

Almacenamiento: Amazon S3 (para archivos multimedia y hosting del frontend).

Servidor de Aplicaciones: Amazon EC2 (instancia t2.micro).

Infraestructura: AWS VPC, Subredes públicas/privadas, Internet Gateway y Security Groups.

<img width="3000" height="2500" alt="image" src="https://github.com/user-attachments/assets/7cb5f3d4-cfe0-4d68-a0bf-4a52d131dfa8" />

🏗️ Arquitectura del Sistema
La arquitectura sigue las mejores prácticas de seguridad y escalabilidad en la nube:

VPC Segmentada: Uso de subredes públicas para el servidor web y subredes privadas para la base de datos.

Desacoplamiento: Los archivos de video se sirven directamente desde S3 para reducir la carga en el servidor EC2.

Seguridad: Gestión de credenciales mediante variables de entorno (.env) y acceso restringido a RDS solo desde la IP privada de la EC2.

📁 Estructura del Proyecto

├── backend/            # API REST desarrollada con FastAPI
│   ├── main.py         # Punto de entrada de la aplicación
│   ├── models.py       # Definición de esquemas de base de datos
│   └── s3_service.py   # Lógica de integración con AWS S3
├── frontend/           # Interfaz de usuario en React
│   ├── src/            # Componentes y lógica del cliente
│   └── dist/           # Archivos compilados para despliegue
└── .gitignore          # Archivos excluidos de Git (llaves, .env, etc.)

🛠️ Configuración Local
Si deseas ejecutar este proyecto localmente, sigue estos pasos:

Backend
Navega a la carpeta /backend.

Crea un entorno virtual: python -m venv venv.

Instala las dependencias: pip install -r requirements.txt.

Configura tu archivo .env con las credenciales de AWS y RDS.

Inicia el servidor: uvicorn main:app --reload.

Frontend
Navega a la carpeta /frontend.

Instala las dependencias: npm install.

Inicia el modo desarrollo: npm run dev.

✒️ Autor
Harold - Estudiante de Ingeniería en Sistemas - UIDE
