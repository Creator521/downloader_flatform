let FileSystem: any;
try {
  FileSystem = require('expo-file-system/legacy');
} catch (e) {
  // Ignored on web
}
import { Platform } from 'react-native';

const STORAGE_FILE = Platform.OS !== 'web' && FileSystem ? `${FileSystem.documentDirectory}downloads_db.json` : '';

export interface RecentDownload {
  id: string;
  title: string;
  platform: string;
  quality: string;
  size: string;
  status: 'completed' | 'downloading';
  date: string;
  thumbnail?: string;
  duration?: string;
  uri?: string; // The local file path
}

export const getDownloads = async (): Promise<RecentDownload[]> => {
  if (Platform.OS === 'web' || !FileSystem) {
    try {
      const stored = localStorage.getItem('downloads_db');
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      return [];
    }
  }

  try {
    const info = await FileSystem.getInfoAsync(STORAGE_FILE);
    if (!info.exists) {
      return [];
    }
    const data = await FileSystem.readAsStringAsync(STORAGE_FILE);
    return JSON.parse(data);
  } catch (err) {
    console.error('Error reading downloads from storage:', err);
    return [];
  }
};

export const saveDownload = async (download: RecentDownload) => {
  const currentDownloads = await getDownloads();
  const newDownloads = [download, ...currentDownloads];

  if (Platform.OS === 'web' || !FileSystem) {
    try {
      localStorage.setItem('downloads_db', JSON.stringify(newDownloads));
    } catch (e) {
      // Ignore
    }
    return;
  }

  try {
    await FileSystem.writeAsStringAsync(STORAGE_FILE, JSON.stringify(newDownloads));
  } catch (err) {
    console.error('Error saving download to storage:', err);
  }
};

export const removeDownload = async (id: string) => {
  const currentDownloads = await getDownloads();
  const newDownloads = currentDownloads.filter(d => d.id !== id);

  if (Platform.OS === 'web' || !FileSystem) {
    try {
      localStorage.setItem('downloads_db', JSON.stringify(newDownloads));
    } catch (e) {
      // Ignore
    }
    return;
  }

  try {
    await FileSystem.writeAsStringAsync(STORAGE_FILE, JSON.stringify(newDownloads));
  } catch (err) {
    console.error('Error removing download from storage:', err);
  }
};
