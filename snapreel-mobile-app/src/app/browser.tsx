import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface PopularSite {
  id: string;
  name: string;
  icon: string;
  color: string;
  url: string;
}

const POPULAR_SITES: PopularSite[] = [
  { id: '1', name: 'Instagram', icon: 'camera', color: '#E1306C', url: 'instagram.com' },
  { id: '2', name: 'YouTube', icon: 'play-circle', color: '#FF0000', url: 'youtube.com' },
  { id: '3', name: 'TikTok', icon: 'musical-notes', color: '#000', url: 'tiktok.com' },
  { id: '4', name: 'Facebook', icon: 'logo-facebook', color: '#1877F2', url: 'facebook.com' },
  { id: '5', name: 'X (Twitter)', icon: 'logo-twitter', color: '#1DA1F2', url: 'twitter.com' },
  { id: '6', name: 'Vimeo', icon: 'play-circle', color: '#1ab7ea', url: 'vimeo.com' },
  { id: '7', name: 'DailyMotion', icon: 'play-circle', color: '#0066ff', url: 'dailymotion.com' },
  { id: '8', name: 'More', icon: 'ellipsis-horizontal', color: '#666', url: '' },
];

export default function BrowserScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [searchText, setSearchText] = useState('');
  const [recentSearches] = useState(['instagram.com', 'youtube.com', 'tiktok.com']);

  const handleSitePress = (url: string) => {
    if (url) {
      setSearchText(url);
    }
  };

  const SiteCard = ({ site }: { site: PopularSite }) => (
    <TouchableOpacity
      onPress={() => handleSitePress(site.url)}
      style={styles.siteCard}
    >
      <View style={[styles.siteIcon, { backgroundColor: `${site.color}20` }]}>
        <Ionicons name={site.icon as any} size={24} color={site.color} />
      </View>
      <Text style={styles.siteName}>{site.name}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Browser</Text>
        <TouchableOpacity>
          <Ionicons name="download" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Search Bar */}
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={18} color="#666" />
          <TextInput
            style={styles.searchInput}
            placeholder="Search or enter website"
            placeholderTextColor="#666"
            value={searchText}
            onChangeText={setSearchText}
          />
        </View>

        {/* Popular Sites Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Popular Sites</Text>
          <View style={styles.sitesGrid}>
            {POPULAR_SITES.map(site => (
              <SiteCard key={site.id} site={site} />
            ))}
          </View>
        </View>

        {/* How to Download Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>How to download</Text>
          
          <View style={styles.stepCard}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>1</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>Open a platform</Text>
              <Text style={styles.stepDesc}>
                Go to any social platform and find the video you want.
              </Text>
            </View>
          </View>

          <View style={styles.stepCard}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>2</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>Play the video</Text>
              <Text style={styles.stepDesc}>
                Play the video and click on the download button.
              </Text>
            </View>
          </View>

          <View style={styles.stepCard}>
            <View style={styles.stepNumber}>
              <Text style={styles.stepNumberText}>3</Text>
            </View>
            <View style={styles.stepContent}>
              <Text style={styles.stepTitle}>Choose quality</Text>
              <Text style={styles.stepDesc}>
                Select your preferred quality and download it.
              </Text>
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
  content: {
    flex: 1,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginHorizontal: 16,
    marginVertical: 16,
    paddingHorizontal: 12,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
  },
  searchInput: {
    flex: 1,
    paddingVertical: 10,
    fontSize: 14,
    color: '#fff',
  },
  section: {
    paddingHorizontal: 16,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 16,
  },
  sitesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  siteCard: {
    width: '32%',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 12,
    borderRadius: 12,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.1)',
  },
  siteIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  siteName: {
    fontSize: 12,
    fontWeight: '600',
    color: '#d1d5db',
    textAlign: 'center',
  },
  stepCard: {
    flexDirection: 'row',
    gap: 12,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  stepNumber: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#a78bfa',
    justifyContent: 'center',
    alignItems: 'center',
  },
  stepNumberText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
  },
  stepContent: {
    flex: 1,
    justifyContent: 'center',
  },
  stepTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  stepDesc: {
    fontSize: 12,
    color: '#9ca3af',
    lineHeight: 16,
  },
  spacer: {
    height: 20,
  },
});
