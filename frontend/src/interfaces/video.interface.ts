// src/interfaces/video.interface.ts
export interface Video {
  id: number;
  title: string;
  description?: string;
  video_url: string;      // URL de S3
  thumbnail_url: string;  // URL de S3
  views: number;
  created_at: string;
  user_id: number;
  category_id: number;
}



export interface Comment {
  id?: number;
  text: string;
  video_id: number;
  user_id: number;
  created_at?: string;
}