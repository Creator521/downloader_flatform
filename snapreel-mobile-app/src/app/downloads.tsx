import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  Dimensions,
  Alert,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useFocusEffect } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Sharing from 'expo-sharing';
import * as FileSystem from 'expo-file-system';
import * as IntentLauncher from 'expo-intent-launcher';
import { getDownloads, RecentDownload, removeDownload } from '../api/storage';
import BottomTabBar from '../components/BottomTabBar';
import { Swipeable } from 'react-native-gesture-handler';
import * as Haptics from 'expo-haptics';
import Toast from 'react-native-toast-message';

const { width } = Dimensions.get('window');

// Removed MOCK_DOWNLOADS

type FilterType = 'all' | 'videos' | 'reels' | 'shorts' | 'audio';

export default function DownloadsScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [selectedFilter, setSelectedFilter] = useState<FilterType>('all');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest'>('newest');
  const [storedDownloads, setStoredDownloads] = useState<RecentDownload[]>([]);

  useFocusEffect(
    useCallback(() => {
      const loadData = async () => {
        const data = await getDownloads();
        setStoredDownloads(data);
      };
      loadData();
    }, [])
  );

  const getFilteredDownloads = (): RecentDownload[] => {
    let filtered = storedDownloads;

    if (selectedFilter === 'reels') {
      filtered = filtered.filter(d => d.platform === 'instagram');
    } else if (selectedFilter === 'shorts') {
      filtered = filtered.filter(d => d.platform === 'youtube' && d.duration.includes('0:'));
    } else if (selectedFilter === 'audio') {
      filtered = filtered.filter(d => d.quality === 'MP3');
    } else if (selectedFilter === 'videos') {
      filtered = filtered.filter(d => d.quality !== 'MP3');
    }

    return filtered.sort((a, b) => {
      const dateA = new Date(a.date).getTime();
      const dateB = new Date(b.date).getTime();
      return sortBy === 'newest' ? dateB - dateA : dateA - dateB;
    });
  };

  const downloads = getFilteredDownloads();

  const getTotalStorage = () => {
    let totalMB = 0;
    storedDownloads.forEach(item => {
      if (typeof item.size === 'string' && item.size.includes('MB')) {
        const size = parseFloat(item.size.replace(' MB', ''));
        if (!isNaN(size)) totalMB += size;
      }
    });
    return totalMB.toFixed(2);
  };

  const handleDelete = async (id: string) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    await removeDownload(id);
    setStoredDownloads(prev => prev.filter(d => d.id !== id));
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

  const renderRightActions = (id: string) => {
    return (
      <TouchableOpacity 
        style={styles.deleteAction}
        onPress={() => handleDelete(id)}
      >
        <Ionicons name="trash" size={24} color="#fff" />
        <Text style={styles.deleteActionText}>Delete</Text>
      </TouchableOpacity>
    );
  };

  const FilterButton = ({ label, value }: { label: string; value: FilterType }) => (
    <TouchableOpacity
      onPress={() => setSelectedFilter(value)}
      style={[
        styles.filterButton,
        selectedFilter === value && styles.filterButtonActive,
      ]}
    >
      <Text
        style={[
          styles.filterButtonText,
          selectedFilter === value && styles.filterButtonTextActive,
        ]}
      >
        {label}
      </Text>
    </TouchableOpacity>
  );

  const DownloadItem = ({ item }: { item: RecentDownload }) => (
    <Swipeable renderRightActions={() => renderRightActions(item.id)}>
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
        onLongPress={() => {
          Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
          confirmDelete(item.id, item.title);
        }}
        delayLongPress={500}
      >
        <View style={styles.thumbnailContainer}>
          <View style={styles.thumbnail} />
          <View style={styles.playButton}>
            <Ionicons name="play" size={16} color="#fff" />
          </View>
          <Text style={styles.duration}>{item.duration}</Text>
        </View>
        <View style={styles.itemInfo}>
          <Text style={styles.itemTitle} numberOfLines={1}>
            {item.title}
          </Text>
          <View style={styles.metaRow}>
            <Text style={styles.quality}>{item.quality}</Text>
            <Text style={styles.dot}>•</Text>
            <Text style={styles.size}>{item.size}</Text>
          </View>
          <Text
            style={[
              styles.status,
              item.status === 'completed' && styles.statusCompleted,
            ]}
          >
            {item.status === 'completed' ? '✓ Completed' : 'Downloading'}
          </Text>
          <Text style={styles.date}>{item.date}</Text>
        </View>
        <TouchableOpacity 
          style={styles.moreButton}
          onPress={() => openOptions(item)}
        >
          <Ionicons name="ellipsis-vertical" size={20} color="#a78bfa" />
        </TouchableOpacity>
      </TouchableOpacity>
    </Swipeable>
  );

  return (
    <View style={{ flex: 1 }}>
      <View style={styles.container}>
        {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#fff" />
        </TouchableOpacity>
        <View style={{ alignItems: 'center' }}>
          <Text style={styles.headerTitle}>My Downloads</Text>
          <Text style={styles.storageText}>{getTotalStorage()} MB Used</Text>
        </View>
        <TouchableOpacity>
          <Ionicons name="search" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Sort Controls */}
      <View style={styles.controlsRow}>
        <TouchableOpacity
          onPress={() => setSortBy(sortBy === 'newest' ? 'oldest' : 'newest')}
          style={styles.sortButton}
        >
          <Ionicons name="funnel" size={18} color="#a78bfa" />
          <Text style={styles.sortButtonText}>
            Date ({sortBy === 'newest' ? 'Newest' : 'Oldest'})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.layoutToggle}>
          <Ionicons name="grid" size={18} color="#a78bfa" />
        </TouchableOpacity>
      </View>

      {/* Filter Tabs */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.filterContainer}
      >
        <FilterButton label="All" value="all" />
        <FilterButton label="Videos" value="videos" />
        <FilterButton label="Reels" value="reels" />
        <FilterButton label="Shorts" value="shorts" />
        <FilterButton label="Audio" value="audio" />
      </ScrollView>

      {/* Downloads List */}
      {downloads.length > 0 ? (
        <FlatList
          data={downloads}
          keyExtractor={(item) => item.id}
          renderItem={DownloadItem}
          contentContainerStyle={styles.listContent}
        />
      ) : (
        <View style={styles.emptyState}>
          <Ionicons name="download-outline" size={64} color="#666" />
          <Text style={styles.emptyTitle}>No downloads yet</Text>
          <Text style={styles.emptySubtitle}>
            Start by pasting a video link to download
          </Text>
        </View>
        )}
      </View>
      <BottomTabBar />
    </View>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f1419',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#fff',
  },
  storageText: {
    fontSize: 12,
    color: '#a78bfa',
    marginTop: 2,
  },
  controlsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  sortButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderRadius: 8,
  },
  sortButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#a78bfa',
  },
  layoutToggle: {
    padding: 8,
  },
  filterContainer: {
    maxHeight: 64,
    minHeight: 64,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  filterButton: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    marginRight: 8,
    borderRadius: 20,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.1)',
  },
  filterButtonActive: {
    backgroundColor: '#a78bfa',
    borderColor: '#a78bfa',
  },
  filterButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#d1d5db',
  },
  filterButtonTextActive: {
    color: '#fff',
  },
  listContent: {
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  deleteAction: {
    backgroundColor: '#ef4444',
    justifyContent: 'center',
    alignItems: 'center',
    width: 80,
    marginBottom: 16,
    borderRadius: 8,
  },
  deleteActionText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
    marginTop: 4,
  },
  downloadItem: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
    backgroundColor: '#0f1419',
  },
  thumbnailContainer: {
    width: 80,
    height: 80,
    borderRadius: 8,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
    overflow: 'hidden',
  },
  thumbnail: {
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
  },
  playButton: {
    position: 'absolute',
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
  itemInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  itemTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    marginBottom: 6,
  },
  quality: {
    fontSize: 12,
    color: '#d1d5db',
  },
  dot: {
    color: '#6b7280',
  },
  size: {
    fontSize: 12,
    color: '#d1d5db',
  },
  status: {
    fontSize: 11,
    fontWeight: '600',
    color: '#f97316',
    marginBottom: 4,
  },
  statusCompleted: {
    color: '#22c55e',
  },
  date: {
    fontSize: 11,
    color: '#6b7280',
  },
  moreButton: {
    paddingHorizontal: 8,
    justifyContent: 'center',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#fff',
    marginTop: 16,
  },
  emptySubtitle: {
    fontSize: 14,
    color: '#9ca3af',
    marginTop: 8,
    textAlign: 'center',
  },
});
