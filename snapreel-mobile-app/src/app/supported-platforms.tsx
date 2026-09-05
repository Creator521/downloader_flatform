import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

const { width } = Dimensions.get('window');

interface Platform {
  id: string;
  name: string;
  icon: string;
  color: string;
  description: string;
  maxQuality: string;
  supported: boolean;
}

const PLATFORMS: Platform[] = [
  {
    id: '1',
    name: 'Instagram',
    icon: 'camera',
    color: '#E1306C',
    description: 'Reels, Stories, Posts',
    maxQuality: '1080p',
    supported: true,
  },
  {
    id: '2',
    name: 'YouTube',
    icon: 'play-circle',
    color: '#FF0000',
    description: 'Videos, Shorts, Playlists',
    maxQuality: '1080p',
    supported: true,
  },
  {
    id: '3',
    name: 'TikTok',
    icon: 'musical-notes',
    color: '#000',
    description: 'Videos, Sounds',
    maxQuality: '720p',
    supported: true,
  },
  {
    id: '4',
    name: 'Facebook',
    icon: 'logo-facebook',
    color: '#1877F2',
    description: 'Videos, Reels',
    maxQuality: '1080p',
    supported: true,
  },
  {
    id: '5',
    name: 'X (Twitter)',
    icon: 'logo-twitter',
    color: '#1DA1F2',
    description: 'Videos, Tweets',
    maxQuality: '720p',
    supported: true,
  },
  {
    id: '6',
    name: 'Vimeo',
    icon: 'play-circle',
    color: '#1ab7ea',
    description: 'Videos',
    maxQuality: '1080p',
    supported: true,
  },
  {
    id: '7',
    name: 'DailyMotion',
    icon: 'play-circle',
    color: '#0066ff',
    description: 'Videos',
    maxQuality: '720p',
    supported: true,
  },
  {
    id: '8',
    name: 'Pinterest',
    icon: 'pin',
    color: '#E60023',
    description: 'Pins, Videos',
    maxQuality: '720p',
    supported: true,
  },
  {
    id: '9',
    name: 'Snapchat',
    icon: 'camera-outline',
    color: '#FFFC00',
    description: 'Stories, Snaps',
    maxQuality: '480p',
    supported: false,
  },
  {
    id: '10',
    name: 'Reddit',
    icon: 'logo-reddit',
    color: '#FF4500',
    description: 'Videos, Gifs',
    maxQuality: '1080p',
    supported: true,
  },
  {
    id: '11',
    name: 'Twitch',
    icon: 'play-circle',
    color: '#6441a5',
    description: 'Clips, VODs',
    maxQuality: '1080p',
    supported: true,
  },
  {
    id: '12',
    name: 'Telegram',
    icon: 'send',
    color: '#0088cc',
    description: 'Videos, Media',
    maxQuality: '720p',
    supported: true,
  },
];

type FilterType = 'all' | 'supported' | 'coming-soon';

export default function SupportedPlatformsScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [selectedFilter, setSelectedFilter] = useState<FilterType>('all');

  const getFilteredPlatforms = (): Platform[] => {
    if (selectedFilter === 'supported') {
      return PLATFORMS.filter(p => p.supported);
    } else if (selectedFilter === 'coming-soon') {
      return PLATFORMS.filter(p => !p.supported);
    }
    return PLATFORMS;
  };

  const platforms = getFilteredPlatforms();

  const PlatformCard = ({ platform }: { platform: Platform }) => (
    <View
      style={[
        styles.platformCard,
        !platform.supported && styles.platformCardDisabled,
      ]}
    >
      <View style={[styles.platformIconWrapper, { backgroundColor: `${platform.color}20` }]}>
        <Ionicons name={platform.icon as any} size={32} color={platform.color} />
        {!platform.supported && (
          <View style={styles.comingSoonBadge}>
            <Text style={styles.comingSoonText}>Soon</Text>
          </View>
        )}
      </View>
      
      <Text style={styles.platformName}>{platform.name}</Text>
      <Text style={styles.platformDesc}>{platform.description}</Text>
      
      <View style={styles.qualityBadge}>
        <Ionicons name="film" size={12} color="#a78bfa" />
        <Text style={styles.qualityText}>Up to {platform.maxQuality}</Text>
      </View>
      
      {platform.supported && (
        <TouchableOpacity style={styles.downloadButton}>
          <Ionicons name="download" size={14} color="#fff" />
          <Text style={styles.downloadButtonText}>Download</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Supported Platforms</Text>
        <TouchableOpacity>
          <Ionicons name="search" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Filter Tabs */}
      <View style={styles.filterContainer}>
        <TouchableOpacity
          onPress={() => setSelectedFilter('all')}
          style={[
            styles.filterTab,
            selectedFilter === 'all' && styles.filterTabActive,
          ]}
        >
          <Text
            style={[
              styles.filterTabText,
              selectedFilter === 'all' && styles.filterTabTextActive,
            ]}
          >
            All ({PLATFORMS.length})
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          onPress={() => setSelectedFilter('supported')}
          style={[
            styles.filterTab,
            selectedFilter === 'supported' && styles.filterTabActive,
          ]}
        >
          <Text
            style={[
              styles.filterTabText,
              selectedFilter === 'supported' && styles.filterTabTextActive,
            ]}
          >
            Supported ({PLATFORMS.filter(p => p.supported).length})
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity
          onPress={() => setSelectedFilter('coming-soon')}
          style={[
            styles.filterTab,
            selectedFilter === 'coming-soon' && styles.filterTabActive,
          ]}
        >
          <Text
            style={[
              styles.filterTabText,
              selectedFilter === 'coming-soon' && styles.filterTabTextActive,
            ]}
          >
            Coming ({PLATFORMS.filter(p => !p.supported).length})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Platforms Grid */}
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.platformsGrid}>
          {platforms.map(platform => (
            <PlatformCard key={platform.id} platform={platform} />
          ))}
        </View>

        {/* Info Section */}
        <View style={styles.infoSection}>
          <Text style={styles.infoTitle}>More Coming Soon!</Text>
          <Text style={styles.infoText}>
            We're constantly adding support for more platforms. If you don't see your favorite platform, let us know!
          </Text>
          <TouchableOpacity style={styles.suggestButton}>
            <Ionicons name="bulb-outline" size={16} color="#a78bfa" />
            <Text style={styles.suggestButtonText}>Suggest a Platform</Text>
          </TouchableOpacity>
        </View>

        {/* Quality Info */}
        <View style={styles.qualityInfoSection}>
          <Text style={styles.qualityInfoTitle}>Quality Information</Text>
          
          <View style={styles.qualityInfoRow}>
            <View style={styles.qualityInfoDot} />
            <View>
              <Text style={styles.qualityInfoLabel}>1080p (Full HD)</Text>
              <Text style={styles.qualityInfoDesc}>Best quality, larger file size</Text>
            </View>
          </View>
          
          <View style={styles.qualityInfoRow}>
            <View style={styles.qualityInfoDot} />
            <View>
              <Text style={styles.qualityInfoLabel}>720p (HD)</Text>
              <Text style={styles.qualityInfoDesc}>Good quality, moderate file size</Text>
            </View>
          </View>
          
          <View style={styles.qualityInfoRow}>
            <View style={styles.qualityInfoDot} />
            <View>
              <Text style={styles.qualityInfoLabel}>480p (SD)</Text>
              <Text style={styles.qualityInfoDesc}>Lower quality, smaller file</Text>
            </View>
          </View>
        </View>

        <View style={styles.spacer} />
      </ScrollView>
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
  filterContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  filterTab: {
    flex: 1,
    paddingVertical: 8,
    alignItems: 'center',
    borderBottomWidth: 2,
    borderBottomColor: 'transparent',
  },
  filterTabActive: {
    borderBottomColor: '#a78bfa',
  },
  filterTabText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6b7280',
  },
  filterTabTextActive: {
    color: '#a78bfa',
  },
  content: {
    flex: 1,
  },
  platformsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
  },
  platformCard: {
    width: (width - 40 - 12) / 2,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 12,
    alignItems: 'center',
  },
  platformCardDisabled: {
    opacity: 0.6,
  },
  platformIconWrapper: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
    position: 'relative',
  },
  comingSoonBadge: {
    position: 'absolute',
    bottom: -2,
    right: -2,
    backgroundColor: '#f97316',
    paddingHorizontal: 5,
    paddingVertical: 2,
    borderRadius: 10,
  },
  comingSoonText: {
    fontSize: 8,
    fontWeight: '700',
    color: '#fff',
  },
  platformName: {
    fontSize: 14,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 4,
  },
  platformDesc: {
    fontSize: 11,
    color: '#9ca3af',
    marginBottom: 8,
    textAlign: 'center',
  },
  qualityBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    borderRadius: 6,
    marginBottom: 8,
  },
  qualityText: {
    fontSize: 10,
    color: '#a78bfa',
    fontWeight: '600',
  },
  downloadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    width: '100%',
    paddingVertical: 8,
    backgroundColor: '#a78bfa',
    borderRadius: 6,
  },
  downloadButtonText: {
    fontSize: 11,
    fontWeight: '600',
    color: '#fff',
  },
  infoSection: {
    marginHorizontal: 16,
    marginVertical: 16,
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 13,
    color: '#9ca3af',
    lineHeight: 18,
    marginBottom: 12,
  },
  suggestButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#a78bfa',
  },
  suggestButtonText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#a78bfa',
  },
  qualityInfoSection: {
    marginHorizontal: 16,
    marginVertical: 16,
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.1)',
  },
  qualityInfoTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 12,
  },
  qualityInfoRow: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 12,
  },
  qualityInfoDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#a78bfa',
    marginTop: 4,
    flexShrink: 0,
  },
  qualityInfoLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 2,
  },
  qualityInfoDesc: {
    fontSize: 11,
    color: '#9ca3af',
  },
  spacer: {
    height: 20,
  },
});
