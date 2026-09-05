import React, { useState, useEffect, useCallback } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  Image, 
  StyleSheet, 
  ActivityIndicator, 
  Alert, 
  ScrollView,
  Platform,
  Dimensions
} from 'react-native';
import * as Clipboard from 'expo-clipboard';
import { fetchPreview, PreviewResponse } from '../api/preview';
import { downloadMedia, DownloadFormat } from '../api/download';
import { API_BASE_URL } from '../api/client';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useNavigation, useFocusEffect } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Sharing from 'expo-sharing';
import { getDownloads, saveDownload, RecentDownload, removeDownload } from '../api/storage';
import BottomTabBar from '../components/BottomTabBar';
import * as Haptics from 'expo-haptics';
import Toast from 'react-native-toast-message';
import { useShareIntent } from 'expo-share-intent';

let MediaLibrary: any;
try {
  MediaLibrary = require('expo-media-library/legacy');
} catch (e) {
  // Ignored on web
}

import * as FileSystem from 'expo-file-system';
import * as IntentLauncher from 'expo-intent-launcher';

const { width } = Dimensions.get('window');
const PLATFORM_SIZE = 60;

const formatDuration = (seconds?: number | string | null) => {
  if (seconds === undefined || seconds === null || seconds === '') return '0:00';
  const parsed = parseInt(String(seconds), 10);
  if (isNaN(parsed) || parsed <= 0) return '0:00';
  const h = Math.floor(parsed / 3600);
  const m = Math.floor((parsed % 3600) / 60);
  const s = parsed % 60;
  if (h > 0) {
    return `${h}:${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
  }
  return `${m}:${s < 10 ? '0' : ''}${s}`;
};


export default function HomeScreen() {
  const router = useRouter();
  const navigation = useNavigation();
  const insets = useSafeAreaInsets();
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState<PreviewResponse | null>(null);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [isDownloading, setIsDownloading] = useState(false);
  const [recentDownloads, setRecentDownloads] = useState<RecentDownload[]>([]);
  const { hasShareIntent, shareIntent, resetShareIntent, error } = useShareIntent();

  useEffect(() => {
    checkClipboard();
    requestPermissions();
  }, []);

  useFocusEffect(
    useCallback(() => {
      const loadDownloads = async () => {
        const data = await getDownloads();
        setRecentDownloads(data.slice(0, 3)); // Only show top 3 on home
      };
      loadDownloads();
    }, [])
  );

  useEffect(() => {
    if (hasShareIntent && shareIntent) {
      const intentAny = shareIntent as any;
      const sharedText = intentAny.value || intentAny.text || intentAny.webUrl;
      
      if (sharedText) {
        if (sharedText.includes('http')) {
          const urlMatch = sharedText.match(/(https?:\/\/[^\s]+)/g);
          const finalUrl = urlMatch ? urlMatch[0] : sharedText;
          setUrl(finalUrl);
          Toast.show({
            type: 'success',
            text1: 'Link Received',
            text2: 'Fetching preview...',
          });
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
          setTimeout(() => {
            handlePreviewInternal(finalUrl);
          }, 500);
        } else {
          Alert.alert("Share Intent", "No link found in: " + sharedText);
        }
      } else {
         // Fallback if we couldn't find text
         Alert.alert("Share Intent", "Could not extract link from: " + JSON.stringify(shareIntent));
      }
      resetShareIntent();
    }
  }, [hasShareIntent, shareIntent]);

  const requestPermissions = async () => {
    if (Platform.OS !== 'web' && MediaLibrary) {
      const { status } = await MediaLibrary.requestPermissionsAsync();
      if (status !== 'granted') {
        Toast.show({
          type: 'error',
          text1: 'Permission needed',
          text2: 'Please grant media library permissions to save files.',
        });
      }
    }
  };

  const checkClipboard = async () => {
    try {
      if (Platform.OS === 'web') return; // Browsers often block auto-clipboard reading
      const text = await Clipboard.getStringAsync();
      if (text && (text.includes('instagram.com') || text.includes('youtube.com') || text.includes('tiktok.com'))) {
        Alert.alert(
          "Link Detected",
          "We found a link in your clipboard. Do you want to paste it?",
          [
            { text: "Cancel", style: "cancel" },
            { text: "Paste", onPress: () => setUrl(text) }
          ]
        );
      }
    } catch (err) {
      console.log('Clipboard check failed:', err);
    }
  };

  const handlePaste = async () => {
    try {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      const text = await Clipboard.getStringAsync();
      setUrl(text);
      Toast.show({
        type: 'success',
        text1: 'Link Pasted',
      });
    } catch (err) {
      console.log('Paste failed:', err);
      if (Platform.OS === 'web') {
        window.alert('Please paste the URL manually. Clipboard access is blocked by your browser.');
      }
    }
  };

  const handlePreview = async () => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    handlePreviewInternal(url);
  };

  const handlePreviewInternal = async (targetUrl: string) => {
    console.log('Preview button clicked. URL:', targetUrl);
    if (!targetUrl) {
      if (Platform.OS === 'web') {
        window.alert('Please enter a valid URL');
      } else {
        Toast.show({
          type: 'error',
          text1: 'Invalid URL',
          text2: 'Please enter a valid URL to download',
        });
      }
      return;
    }
    
    setLoading(true);
    setPreview(null);
    try {
      console.log('Fetching preview for:', targetUrl);
      const data = await fetchPreview(targetUrl);
      console.log('Preview data received:', data);
      setPreview(data);
    } catch (err: any) {
      console.error('Preview fetch error:', err);
      const msg = err.message || 'Something went wrong';
      if (Platform.OS === 'web') {
        window.alert('Preview Failed: ' + msg);
      } else {
        Toast.show({
          type: 'error',
          text1: 'Preview Failed',
          text2: msg,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (format: DownloadFormat) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    if (!preview) return;
    
    setIsDownloading(true);
    setDownloadProgress(0);
    
    try {
      const ext = format === 'audio' ? 'm4a' : 'mp4';
      const safeTitle = preview.title.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 30);
      const filename = `${safeTitle}_${Date.now()}.${ext}`;
      
      const result = await downloadMedia({
        url,
        format,
        filename,
        onProgress: (progress) => {
          // If progress is negative or Infinity due to missing Content-Length, default to 0 or handle it
          setDownloadProgress(Math.max(0, isFinite(progress) ? progress : 0));
        }
      });
      
      if (result && result.uri) {
        let finalDuration = preview.duration;
        if (Platform.OS !== 'web' && MediaLibrary) {
          const asset = await MediaLibrary.createAssetAsync(result.uri);
          if (asset) {
            if (asset.duration && asset.duration > 0) {
              finalDuration = asset.duration;
            }
            Toast.show({
              type: 'success',
              text1: 'Download Complete',
              text2: 'File saved to gallery.',
            });
            Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
          } else {
            Toast.show({
              type: 'info',
              text1: 'Saved to Cache',
              text2: 'File downloaded but could not be saved to gallery.',
            });
          }
        } else {
          Toast.show({
            type: 'success',
            text1: 'Download Complete',
            text2: 'File downloaded successfully.',
          });
          Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
        }
        
        let fileSize = 'Unknown';
        if (Platform.OS !== 'web' && FileSystem && result?.uri) {
          try {
            const info = await FileSystem.getInfoAsync(result.uri);
            if (info.exists && info.size) {
              fileSize = (info.size / (1024 * 1024)).toFixed(2) + ' MB';
            }
          } catch (e) {
            console.log('Error getting file size', e);
          }
        }
        
        const newDownload: RecentDownload = {
            id: Date.now().toString(),
            title: preview.title || 'Downloaded Video',
            platform: url.includes('youtube') ? 'youtube' : url.includes('instagram') ? 'instagram' : 'tiktok',
            quality: format,
            size: fileSize,
            status: 'completed',
            date: new Date().toISOString().split('T')[0],
            duration: formatDuration(finalDuration),
            uri: result.uri
          };
          await saveDownload(newDownload);
          setRecentDownloads(prev => [newDownload, ...prev].slice(0, 3));
      }
    } catch (err: any) {
      Toast.show({
        type: 'error',
        text1: 'Download Failed',
        text2: err.message || 'Check your network connection.',
      });
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
    } finally {
      setIsDownloading(false);
      setDownloadProgress(0);
    }
  };

  const PlatformIcon = ({ name, icon }: { name: string; icon: any }) => (
    <TouchableOpacity style={styles.platformItem} onPress={() => router.push('/supported-platforms')}>
      <View style={styles.platformIconWrapper}>
        {typeof icon === 'string' ? (
          <Ionicons name={icon as any} size={28} color="#fff" />
        ) : (
          icon
        )}
      </View>
      <Text style={styles.platformName}>{name}</Text>
    </TouchableOpacity>
  );

  const handleDelete = async (id: string) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    await removeDownload(id);
    setRecentDownloads(prev => prev.filter(d => d.id !== id));
    Toast.show({
      type: 'success',
      text1: 'Download removed',
    });
  };

  const confirmDelete = (id: string, title: string) => {
    Alert.alert(
      "Delete Video",
      `Are you sure you want to delete "${title}"?`,
      [
        { text: "Cancel", style: "cancel" },
        { text: "Delete", onPress: () => handleDelete(id), style: "destructive" }
      ]
    );
  };

  const openOptions = (item: RecentDownload) => {
    Alert.alert(
      "Video Options",
      item.title,
      [
        { text: "Share", onPress: async () => {
            if (item.uri) {
              try {
                await Sharing.shareAsync(item.uri);
              } catch (e) {
                console.error("Share error", e);
              }
            }
          }
        },
        { text: "Delete", onPress: () => confirmDelete(item.id, item.title), style: "destructive" },
        { text: "Cancel", style: "cancel" }
      ]
    );
  };

  const HowItWorksStep = ({ number, title, desc }: { number: string; title: string; desc: string }) => (
    <View style={styles.stepContainer}>
      <View style={styles.stepNumber}>
        <Text style={styles.stepNumberText}>{number}</Text>
      </View>
      <Text style={styles.stepTitle}>{title}</Text>
      <Text style={styles.stepDesc}>{desc}</Text>
    </View>
  );

  const RecentDownloadItem = ({ item }: { item: RecentDownload }) => (
    <TouchableOpacity 
      style={styles.downloadItem}
      onPress={async () => {
        if (item.uri) {
          try {
              if (Platform.OS === 'android') {
                const contentUri = await FileSystem.getContentUriAsync(item.uri);
                await IntentLauncher.startActivityAsync('android.intent.action.VIEW', {
                  data: contentUri,
                  flags: 1, // FLAG_GRANT_READ_URI_PERMISSION
                  type: item.quality === 'audio' ? 'audio/*' : 'video/*',
                });
              } else {
                await Sharing.shareAsync(item.uri);
              }
            } catch (e: any) {
              try {
                // Fallback to share sheet if direct intent fails
                await Sharing.shareAsync(item.uri);
              } catch (shareErr) {
                Alert.alert('Could not open video', String(e.message));
              }
            }
        }
      }}
    >
      <View style={styles.downloadThumbnail}>
        <View style={styles.playButton}>
          <Ionicons name="play" size={20} color="#fff" />
        </View>
        <Text style={styles.duration}>{item.duration}</Text>
      </View>
      <View style={styles.downloadInfo}>
        <Text style={styles.downloadTitle} numberOfLines={1}>{item.title}</Text>
        <View style={styles.downloadMeta}>
          <Text style={styles.downloadQuality}>{item.quality}</Text>
          <Text style={styles.downloadDot}>•</Text>
          <Text style={styles.downloadSize}>{item.size}</Text>
        </View>
        <Text style={[styles.downloadStatus, item.status === 'completed' && styles.statusCompleted]}>
          {item.status === 'completed' ? 'Completed' : 'Downloading'}
        </Text>
        <Text style={styles.downloadDate}>{item.date}</Text>
      </View>
      <TouchableOpacity 
        style={styles.moreButton}
        onPress={() => openOptions(item)}
      >
        <Ionicons name="ellipsis-vertical" size={20} color="#a78bfa" />
      </TouchableOpacity>
    </TouchableOpacity>
  );

  return (
    <View style={{ flex: 1 }}>
      <ScrollView style={styles.container} showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">

      {/* Header with Logo */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <View style={styles.logoContainer}>
          <TouchableOpacity 
            onPress={() => {
              try {
                (navigation as any).openDrawer();
              } catch (err) {
                console.error(err);
              }
            }} 
            style={{ marginRight: 12, marginTop: 4 }}
          >
            <Ionicons name="menu" size={28} color="#fff" />
          </TouchableOpacity>
          <View style={{ flexDirection: 'row', alignItems: 'baseline', gap: 6 }}>
            <Text style={styles.logoBrand}>SnapReel</Text>
            <Text style={styles.logoSubtext}>Downloader</Text>
          </View>
        </View>
        <TouchableOpacity style={styles.premiumBadge} onPress={() => router.push('/premium')}>
          <Ionicons name="star" size={16} color="#ffd700" />
        </TouchableOpacity>
      </View>

      {/* Hero Section */}
      <View style={styles.heroSection}>
        <View style={styles.heroTag}>
          <Ionicons name="flash" size={14} color="#a78bfa" />
          <Text style={styles.heroTagText}>Fast • Simple • Secure</Text>
        </View>
        <Text style={styles.heroTitle}>Download from</Text>
        <Text style={styles.heroPlatforms}>100+ Platforms</Text>
        <Text style={styles.heroDescription}>
          Paste a link below to download videos, reels, shorts and more.
        </Text>

        {/* URL Input */}
        <View style={styles.urlInputWrapper}>
          <View style={styles.urlInputContainer}>
            <Ionicons name="link" size={18} color="#a78bfa" />
            <TextInput
              style={styles.urlInput}
              placeholder="Paste video URL here..."
              placeholderTextColor="#666"
              value={url}
              onChangeText={setUrl}
              autoCapitalize="none"
              autoCorrect={false}
            />
          </View>
          <TouchableOpacity style={styles.pasteButton} onPress={handlePaste}>
            <Ionicons name="clipboard" size={16} color="#fff" />
            <Text style={styles.pasteButtonText}>Paste</Text>
          </TouchableOpacity>
        </View>

        {/* Preview Button */}
        <TouchableOpacity 
          style={[styles.previewButton, !url && styles.previewButtonDisabled]} 
          onPress={handlePreview}
          disabled={!url || loading}
          activeOpacity={0.8}
        >
          {loading ? (
            <ActivityIndicator color="#fff" size="small" />
          ) : (
            <>
              <Ionicons name="download" size={18} color="#fff" />
              <Text style={styles.previewButtonText}>Preview Video</Text>
            </>
          )}
        </TouchableOpacity>

        {preview && (
          <View style={styles.previewCard}>
            <Image 
              source={{ uri: preview.thumbnail?.startsWith('/') ? `${API_BASE_URL}${preview.thumbnail}` : preview.thumbnail }} 
              style={styles.previewImage} 
            />
            <View style={styles.previewDetails}>
              <Text style={styles.previewTitle} numberOfLines={2}>{preview.title}</Text>
              <Text style={styles.previewMeta}>{formatDuration(preview.duration)} • {preview.uploader}</Text>
            </View>
            <View style={styles.downloadButtonsRow}>
              <TouchableOpacity style={styles.dlButton} onPress={() => handleDownload('video')} disabled={isDownloading}>
                <Ionicons name="videocam" size={16} color="#fff" />
                <Text style={styles.dlButtonText}>Video</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.dlButton} onPress={() => handleDownload('high_quality')} disabled={isDownloading}>
                <Ionicons name="star" size={16} color="#fff" />
                <Text style={styles.dlButtonText}>HQ Video</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.dlButton} onPress={() => handleDownload('audio')} disabled={isDownloading}>
                <Ionicons name="musical-note" size={16} color="#fff" />
                <Text style={styles.dlButtonText}>Audio</Text>
              </TouchableOpacity>
            </View>
            {isDownloading && (
              <View style={styles.progressContainer}>
                <Text style={styles.progressText}>Downloading... {Math.round(downloadProgress * 100)}%</Text>
                <View style={styles.progressBar}>
                  <View style={[styles.progressFill, { width: `${downloadProgress * 100}%` }]} />
                </View>
              </View>
            )}
          </View>
        )}
      </View>

      {/* Supported Platforms */}
      <View style={styles.platformsSection}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Supported Platforms</Text>
          <TouchableOpacity 
            style={{ flexDirection: 'row', alignItems: 'center' }} 
            onPress={() => router.push('/supported-platforms')}
          >
            <Text style={styles.viewAllLink}>View All</Text>
            <Ionicons name="chevron-forward" size={14} color="#a78bfa" />
          </TouchableOpacity>
        </View>
        
        <View style={styles.platformsGrid}>
          <PlatformIcon name="Instagram" icon={<Ionicons name="camera" size={24} color="#E1306C" />} />
          <PlatformIcon name="YouTube" icon={<Ionicons name="play-circle" size={24} color="#FF0000" />} />
          <PlatformIcon name="TikTok" icon={<Ionicons name="musical-notes" size={24} color="#000" />} />
          <PlatformIcon name="Facebook" icon={<Ionicons name="logo-facebook" size={24} color="#1877F2" />} />
          <PlatformIcon name="Twitter" icon={<Ionicons name="logo-twitter" size={24} color="#1DA1F2" />} />
          <PlatformIcon name="More" icon={<Ionicons name="ellipsis-horizontal" size={24} color="#666" />} />
        </View>
      </View>

      {/* How It Works */}
      <View style={styles.howItWorksSection}>
        <Text style={styles.sectionTitle}>How it works</Text>
        <View style={styles.stepsContainer}>
          <HowItWorksStep 
            number="1" 
            title="Copy Link" 
            desc="Copy the link of any video you want to download."
          />
          <HowItWorksStep 
            number="2" 
            title="Preview" 
            desc="Preview the video to make sure it's the right one."
          />
          <HowItWorksStep 
            number="3" 
            title="Download" 
            desc="Choose quality and download to your device."
          />
        </View>
      </View>

      {/* Recent Downloads */}
      <View style={styles.recentSection}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Recent Downloads</Text>
          <TouchableOpacity 
            style={{ flexDirection: 'row', alignItems: 'center' }} 
            onPress={() => router.push('/downloads')}
          >
            <Text style={styles.viewAllLink}>View All</Text>
            <Ionicons name="chevron-forward" size={14} color="#a78bfa" />
          </TouchableOpacity>
        </View>
        
        <View>
          {recentDownloads.map(item => (
            <RecentDownloadItem key={item.id} item={item} />
          ))}
        </View>
      </View>

      <View style={styles.spacer} />
      </ScrollView>
      <BottomTabBar />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f1419',
  },
  adContainer: {
    width: '100%',
    alignItems: 'center',
    paddingVertical: 8,
  },
  
  // Header
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 24,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoBrand: {
    fontSize: 22,
    fontWeight: '700',
    color: '#fff',
  },
  logoSubtext: {
    fontSize: 20,
    fontWeight: '700',
    color: '#a78bfa',
  },
  premiumBadge: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Hero Section
  heroSection: {
    paddingHorizontal: 20,
    paddingBottom: 32,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  heroTag: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    alignSelf: 'flex-start',
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    marginBottom: 16,
  },
  heroTagText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#a78bfa',
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: '700',
    color: '#e5e7eb',
    marginBottom: 4,
  },
  heroPlatforms: {
    fontSize: 32,
    fontWeight: '700',
    color: '#a78bfa',
    marginBottom: 12,
  },
  heroDescription: {
    fontSize: 14,
    color: '#9ca3af',
    marginBottom: 20,
    lineHeight: 20,
  },
  urlInputWrapper: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 16,
  },
  urlInputContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
    borderRadius: 12,
    paddingHorizontal: 12,
    gap: 10,
  },
  urlInput: {
    flex: 1,
    height: 48,
    fontSize: 14,
    color: '#fff',
  },
  pasteButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    backgroundColor: '#a78bfa',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    minHeight: 48,
  },
  pasteButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },
  previewButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    backgroundColor: '#7c3aed',
    paddingVertical: 16,
    borderRadius: 12,
    width: '100%',
    shadowColor: '#a78bfa',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
  },
  previewButtonDisabled: {
    opacity: 0.5,
  },
  previewButtonText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
  },

  // Platforms Section
  platformsSection: {
    paddingHorizontal: 20,
    paddingVertical: 28,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#fff',
  },
  viewAllLink: {
    fontSize: 13,
    fontWeight: '600',
    color: '#a78bfa',
  },
  platformsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 16,
  },
  platformItem: {
    alignItems: 'center',
    width: (width - 40 - 16 * 2) / 3,
  },
  platformIconWrapper: {
    width: PLATFORM_SIZE,
    height: PLATFORM_SIZE,
    borderRadius: PLATFORM_SIZE / 2,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
  },
  platformName: {
    fontSize: 12,
    fontWeight: '600',
    color: '#d1d5db',
  },

  // How It Works Section
  howItWorksSection: {
    paddingHorizontal: 20,
    paddingVertical: 28,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  stepsContainer: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 20,
  },
  stepContainer: {
    flex: 1,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.1)',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  stepNumber: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#a78bfa',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  stepNumberText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
  },
  stepTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
    textAlign: 'center',
  },
  stepDesc: {
    fontSize: 11,
    color: '#9ca3af',
    textAlign: 'center',
    lineHeight: 16,
  },

  // Recent Downloads Section
  recentSection: {
    paddingHorizontal: 20,
    paddingVertical: 28,
  },
  downloadItem: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  downloadThumbnail: {
    width: 80,
    height: 80,
    borderRadius: 8,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  playButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  duration: {
    position: 'absolute',
    bottom: 4,
    right: 4,
    fontSize: 10,
    fontWeight: '600',
    color: '#fff',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    paddingHorizontal: 4,
    paddingVertical: 2,
    borderRadius: 2,
  },
  downloadInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  downloadTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  downloadMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginBottom: 6,
  },
  downloadQuality: {
    fontSize: 12,
    color: '#d1d5db',
  },
  downloadDot: {
    color: '#6b7280',
  },
  downloadSize: {
    fontSize: 12,
    color: '#d1d5db',
  },
  downloadStatus: {
    fontSize: 11,
    fontWeight: '600',
    color: '#f97316',
    marginBottom: 4,
  },
  statusCompleted: {
    color: '#22c55e',
  },
  downloadDate: {
    fontSize: 11,
    color: '#6b7280',
  },
  moreButton: {
    paddingHorizontal: 8,
    justifyContent: 'center',
  },

  spacer: {
    height: 40,
  },
  previewCard: {
    marginTop: 20,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
    padding: 16,
  },
  previewImage: {
    width: '100%',
    height: 180,
    borderRadius: 8,
    marginBottom: 12,
  },
  previewDetails: {
    marginBottom: 12,
  },
  previewTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  previewMeta: {
    fontSize: 12,
    color: '#9ca3af',
  },
  downloadButtonsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  dlButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
    paddingVertical: 10,
    borderRadius: 8,
  },
  dlButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#a78bfa',
  },
  progressContainer: {
    marginTop: 12,
  },
  progressText: {
    color: '#fff',
    fontSize: 12,
    marginBottom: 4,
  },
  progressBar: {
    height: 4,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 2,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#a78bfa',
    borderRadius: 2,
  },
});
