// src/components/Player.tsx
import { Video } from '../../interfaces/video.interface';

interface PlayerProps {
  video: Video;
}

export function Player({ video }: PlayerProps) {
  return (
    <section className="flex-1">
      <video 
        key={video.id} 
        controls 
        autoPlay
        poster={video.thumbnail_url}
        className="w-full aspect-video rounded-xl bg-black shadow-lg"
      >
        <source src={video.video_url} type="video/mp4" />
        Tu navegador no soporta reproducción de video HTML5.
      </video>
      <h1 className="mt-4 text-2xl font-bold text-gray-900">{video.title}</h1>
      <p className="text-gray-600 text-sm mt-1">{video.views} vistas</p>
    </section>
  );
}