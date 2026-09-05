let FileSystem: any;
try {
  FileSystem = require('expo-file-system/legacy');
} catch (e) {
  // Ignored on web
}
import { API_BASE_URL } from './client';
import { Platform } from 'react-native';

export type DownloadFormat = 'video' | 'audio' | 'high_quality';

export interface DownloadOptions {
  url: string;
  format: DownloadFormat;
  filename: string;
  onProgress?: (progress: number) => void;
}

/**
 * Downloads a media file directly to the device storage.
 */
export const downloadMedia = async (options: DownloadOptions) => {
  const queryParams = `url=${encodeURIComponent(options.url)}&format=${encodeURIComponent(options.format)}`;
  const endpoint = `${API_BASE_URL}/download?${queryParams}`;

  if (Platform.OS === 'web') {
    // Web fallback using fetch and Blob
    try {
      const response = await fetch(endpoint, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Download failed on web');
      }

      const blob = await response.blob();
      const blobUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = options.filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(blobUrl);

      return { uri: blobUrl }; // Simulate successful response
    } catch (error) {
      throw error;
    }
  }

  // Native flow
  const fileUri = `${FileSystem.documentDirectory}${options.filename}`;

  const downloadResumable = FileSystem.createDownloadResumable(
    endpoint,
    fileUri,
    {},
    (downloadProgress) => {
      const progress = downloadProgress.totalBytesWritten / downloadProgress.totalBytesExpectedToWrite;
      if (options.onProgress) {
        options.onProgress(progress);
      }
    }
  );

  try {
    const result = await downloadResumable.downloadAsync();
    return result; // contains .uri
  } catch (error) {
    throw error;
  }
};
