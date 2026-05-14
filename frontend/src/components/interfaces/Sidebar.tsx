// src/components/Sidebar.tsx
import { Video } from '../../interfaces/video.interface';

interface SidebarProps {
  videos: Video[];
  onSelect: (video: Video) => void;
}

export function Sidebar({ videos, onSelect }: SidebarProps) {
  return (
    <aside className="w-full lg:w-[400px] flex flex-col gap-4">
      <h3 className="text-md font-bold text-gray-700 px-2">Videos Recomendados</h3>
      <div className="flex flex-col gap-3">
        {videos.map((video) => (
          <div 
            key={video.id} 
            onClick={() => onSelect(video)}
            className="flex gap-3 p-2 hover:bg-gray-100 rounded-xl cursor-pointer transition-all duration-200 group"
          >
            {/* Flexbox interno */}
            <div className="relative w-40 aspect-video flex-shrink-0 bg-gray-200 rounded-lg overflow-hidden">
              <img 
                src={video.thumbnail_url} 
                alt={video.title} 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
              />
            </div>
            <div className="flex flex-col justify-start">
              <h4 className="text-sm font-semibold line-clamp-2 text-gray-900 leading-tight mb-1">{video.title}</h4>
              <p className="text-xs text-gray-500">{video.views} vistas</p>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}