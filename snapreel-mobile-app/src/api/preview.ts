import { apiRequest } from './client';

export interface PreviewResponse {
  title: string;
  thumbnail: string;
  video_url: string;
  uploader?: string;
  view_count?: number;
  duration?: number;
}

/**
 * Fetches the preview data for a given video/audio URL.
 */
export const fetchPreview = async (url: string): Promise<PreviewResponse> => {
  return apiRequest<PreviewResponse>('/preview', 'POST', { url });
};
