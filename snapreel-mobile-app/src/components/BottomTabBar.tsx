import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, usePathname } from 'expo-router';

export default function BottomTabBar() {
  const router = useRouter();
  const pathname = usePathname();

  const isHome = pathname === '/' || pathname === '/index';
  const isDownloads = pathname === '/downloads';

  return (
    <View style={styles.container}>
      <TouchableOpacity 
        style={styles.tab} 
        onPress={() => router.push('/')}
        activeOpacity={0.7}
      >
        <Ionicons 
          name={isHome ? "home" : "home-outline"} 
          size={24} 
          color={isHome ? "#a78bfa" : "#6b7280"} 
        />
        <Text style={[styles.label, isHome && styles.activeLabel]}>Home</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={styles.tab} 
        onPress={() => router.push('/downloads')}
        activeOpacity={0.7}
      >
        <Ionicons 
          name={isDownloads ? "download" : "download-outline"} 
          size={24} 
          color={isDownloads ? "#a78bfa" : "#6b7280"} 
        />
        <Text style={[styles.label, isDownloads && styles.activeLabel]}>Downloads</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#0f1419',
    paddingBottom: Platform.OS === 'ios' ? 24 : 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: 'rgba(167, 139, 250, 0.1)',
  },
  tab: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
  },
  label: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '500',
  },
  activeLabel: {
    color: '#a78bfa',
    fontWeight: '600',
  },
});
