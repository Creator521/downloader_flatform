import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function HowToUseScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const Step = ({
    number,
    title,
    description,
  }: {
    number: string;
    title: string;
    description: string;
  }) => (
    <View style={styles.stepContainer}>
      <View style={styles.stepNumberCircle}>
        <Text style={styles.stepNumber}>{number}</Text>
      </View>
      <View style={styles.stepContent}>
        <Text style={styles.stepTitle}>{title}</Text>
        <Text style={styles.stepDescription}>{description}</Text>
      </View>
    </View>
  );

  const Feature = ({
    icon,
    title,
    description,
  }: {
    icon: string;
    title: string;
    description: string;
  }) => (
    <View style={styles.featureCard}>
      <View style={styles.featureIcon}>
        <Ionicons name={icon as any} size={24} color="#a78bfa" />
      </View>
      <Text style={styles.featureTitle}>{title}</Text>
      <Text style={styles.featureDescription}>{description}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>How to Use</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Introduction */}
        <View style={styles.introSection}>
          <Text style={styles.introTitle}>Welcome to SnapReel Downloader</Text>
          <Text style={styles.introText}>
            Download videos, reels, shorts, and audio from 100+ platforms easily and securely.
          </Text>
        </View>

        {/* Basic Steps */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Basic Steps</Text>
          
          <Step
            number="1"
            title="Copy the Video Link"
            description="Find any video on Instagram, YouTube, TikTok, Facebook, Twitter, or other supported platforms and copy its link."
          />
          
          <Step
            number="2"
            title="Paste the Link"
            description="Open SnapReel and paste the video link in the input field. You can use the paste button for quick access."
          />
          
          <Step
            number="3"
            title="Preview the Video"
            description="Click Preview to see the video details including duration, resolution, and file size."
          />
          
          <Step
            number="4"
            title="Select Quality"
            description="Choose your preferred quality (1080p, 720p, 480p, or 360p) and audio format if available."
          />
          
          <Step
            number="5"
            title="Download"
            description="Click Download and the video will be saved to your device's Downloads folder."
          />
        </View>

        {/* Key Features */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Key Features</Text>
          
          <View style={styles.featuresGrid}>
            <Feature
              icon="flash"
              title="Fast Downloads"
              description="Get your videos in seconds"
            />
            <Feature
              icon="shield-checkmark"
              title="Secure & Private"
              description="We don't store any of your data"
            />
            <Feature
              icon="film"
              title="Multiple Formats"
              description="Choose quality and format you want"
            />
            <Feature
              icon="download"
              title="Offline Access"
              description="Watch downloaded content anytime"
            />
            <Feature
              icon="apps"
              title="100+ Platforms"
              description="Support for all popular social platforms"
            />
            <Feature
              icon="notifications-outline"
              title="No Ads"
              description="Ad-free downloading experience"
            />
          </View>
        </View>

        {/* Pro Tips */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Pro Tips</Text>
          
          <View style={styles.tipCard}>
            <Ionicons name="bulb" size={20} color="#ffd700" />
            <View style={{ flex: 1 }}>
              <Text style={styles.tipTitle}>Use Auto-Paste</Text>
              <Text style={styles.tipText}>
                When you copy a video link, SnapReel will notify you and offer to paste it automatically.
              </Text>
            </View>
          </View>
          
          <View style={styles.tipCard}>
            <Ionicons name="bulb" size={20} color="#ffd700" />
            <View style={{ flex: 1 }}>
              <Text style={styles.tipTitle}>Higher Quality = Larger File</Text>
              <Text style={styles.tipText}>
                Choose a quality that matches your storage and internet speed for better experience.
              </Text>
            </View>
          </View>
          
          <View style={styles.tipCard}>
            <Ionicons name="bulb" size={20} color="#ffd700" />
            <View style={{ flex: 1 }}>
              <Text style={styles.tipTitle}>Manage Storage</Text>
              <Text style={styles.tipText}>
                Check your storage regularly and delete old videos to make room for new downloads.
              </Text>
            </View>
          </View>
          
          <View style={styles.tipCard}>
            <Ionicons name="bulb" size={20} color="#ffd700" />
            <View style={{ flex: 1 }}>
              <Text style={styles.tipTitle}>Use Wi-Fi Download</Text>
              <Text style={styles.tipText}>
                For faster and more reliable downloads, enable "Download via Wi-Fi only" in settings.
              </Text>
            </View>
          </View>
        </View>

        {/* FAQ Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Frequently Asked Questions</Text>
          
          <View style={styles.faqItem}>
            <Text style={styles.faqQuestion}>Q: Is it legal to download videos?</Text>
            <Text style={styles.faqAnswer}>
              A: Downloading for personal use is generally legal, but respect copyright laws in your country.
            </Text>
          </View>
          
          <View style={styles.faqItem}>
            <Text style={styles.faqQuestion}>Q: Can I download audio only?</Text>
            <Text style={styles.faqAnswer}>
              A: Yes, we support audio extraction from videos. Select the audio format in quality options.
            </Text>
          </View>
          
          <View style={styles.faqItem}>
            <Text style={styles.faqQuestion}>Q: How much storage do I need?</Text>
            <Text style={styles.faqAnswer}>
              A: Storage needs depend on video quality. 1080p videos are typically 15-30 MB per minute.
            </Text>
          </View>
          
          <View style={styles.faqItem}>
            <Text style={styles.faqQuestion}>Q: Can I download livestreams?</Text>
            <Text style={styles.faqAnswer}>
              A: Currently, we support downloading completed videos and reels. Livestreams are not supported.
            </Text>
          </View>
        </View>

        {/* Contact Support */}
        <View style={styles.supportSection}>
          <Text style={styles.supportTitle}>Need Help?</Text>
          <Text style={styles.supportText}>
            If you have any questions or issues, contact our support team.
          </Text>
          <TouchableOpacity style={styles.supportButton}>
            <Ionicons name="mail" size={18} color="#fff" />
            <Text style={styles.supportButtonText}>Contact Support</Text>
          </TouchableOpacity>
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
  introSection: {
    paddingHorizontal: 16,
    paddingVertical: 20,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  introTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
  },
  introText: {
    fontSize: 14,
    color: '#9ca3af',
    lineHeight: 20,
  },
  section: {
    paddingHorizontal: 16,
    paddingVertical: 20,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 16,
  },
  stepContainer: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  stepNumberCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#a78bfa',
    justifyContent: 'center',
    alignItems: 'center',
    flexShrink: 0,
  },
  stepNumber: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
  },
  stepContent: {
    flex: 1,
    paddingTop: 2,
  },
  stepTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
  },
  stepDescription: {
    fontSize: 12,
    color: '#9ca3af',
    lineHeight: 16,
  },
  featuresGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  featureCard: {
    width: '48%',
    paddingHorizontal: 12,
    paddingVertical: 14,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.1)',
    alignItems: 'center',
  },
  featureIcon: {
    marginBottom: 8,
  },
  featureTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 4,
    textAlign: 'center',
  },
  featureDescription: {
    fontSize: 11,
    color: '#9ca3af',
    textAlign: 'center',
    lineHeight: 14,
  },
  tipCard: {
    flexDirection: 'row',
    gap: 12,
    paddingHorizontal: 12,
    paddingVertical: 12,
    marginBottom: 12,
    backgroundColor: 'rgba(255, 215, 0, 0.05)',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: 'rgba(255, 215, 0, 0.1)',
  },
  tipTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#ffd700',
    marginBottom: 2,
  },
  tipText: {
    fontSize: 11,
    color: '#9ca3af',
    lineHeight: 14,
  },
  faqItem: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  faqQuestion: {
    fontSize: 13,
    fontWeight: '600',
    color: '#a78bfa',
    marginBottom: 6,
  },
  faqAnswer: {
    fontSize: 12,
    color: '#9ca3af',
    lineHeight: 16,
  },
  supportSection: {
    marginHorizontal: 16,
    marginVertical: 20,
    paddingHorizontal: 16,
    paddingVertical: 20,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
    alignItems: 'center',
  },
  supportTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
  },
  supportText: {
    fontSize: 12,
    color: '#9ca3af',
    marginBottom: 14,
    textAlign: 'center',
  },
  supportButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: '#a78bfa',
    borderRadius: 8,
  },
  supportButtonText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#fff',
  },
  spacer: {
    height: 20,
  },
});
