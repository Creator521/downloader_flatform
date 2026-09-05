import React from 'react';
import { View, StyleSheet, TouchableOpacity, Text, Dimensions } from 'react-native';
import { useVideoPlayer, VideoView } from 'expo-video';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function PlayerScreen() {
  const router = useRouter();
  const { uri, title } = useLocalSearchParams<{ uri: string; title: string }>();
  const insets = useSafeAreaInsets();

  const player = useVideoPlayer(uri ? { uri: uri } : null, (player) => {
    player.loop = false;
    player.play();
  });

  if (!uri) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Video not found</Text>
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <Text style={styles.backText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()} style={styles.closeButton}>
          <Ionicons name="close" size={28} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.title} numberOfLines={1}>{title || 'Playing Video'}</Text>
      </View>
      <View style={styles.videoContainer}>
        <VideoView
          player={player}
          style={styles.video}
          allowsFullscreen
          allowsPictureInPicture
          nativeControls
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    zIndex: 10,
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  closeButton: {
    marginRight: 16,
  },
  title: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    flex: 1,
  },
  videoContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  video: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height - 100,
  },
  errorText: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 50,
  },
  backButton: {
    marginTop: 20,
    padding: 12,
    backgroundColor: '#a78bfa',
    borderRadius: 8,
    alignSelf: 'center',
  },
  backText: {
    color: '#fff',
    fontWeight: '600',
  }
});
