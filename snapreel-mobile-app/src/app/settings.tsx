import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function SettingsScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  const [wifiOnly, setWifiOnly] = useState(false);
  const [autoPreview, setAutoPreview] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [theme, setTheme] = useState('dark');

  const SettingRow = ({
    icon,
    label,
    value,
    onPress,
  }: {
    icon: string;
    label: string;
    value?: string;
    onPress?: () => void;
  }) => (
    <TouchableOpacity
      style={styles.settingRow}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.settingLeft}>
        <View style={styles.iconContainer}>
          <Ionicons name={icon as any} size={18} color="#a78bfa" />
        </View>
        <Text style={styles.settingLabel}>{label}</Text>
      </View>
      {value && <Text style={styles.settingValue}>{value}</Text>}
      {!value && <Ionicons name="chevron-forward" size={18} color="#666" />}
    </TouchableOpacity>
  );

  const ToggleSetting = ({
    icon,
    label,
    value,
    onToggle,
  }: {
    icon: string;
    label: string;
    value: boolean;
    onToggle: (v: boolean) => void;
  }) => (
    <View style={styles.settingRow}>
      <View style={styles.settingLeft}>
        <View style={styles.iconContainer}>
          <Ionicons name={icon as any} size={18} color="#a78bfa" />
        </View>
        <Text style={styles.settingLabel}>{label}</Text>
      </View>
      <Switch
        value={value}
        onValueChange={onToggle}
        trackColor={{ false: '#3a3a3a', true: '#a78bfa' }}
        thumbColor={value ? '#7c3aed' : '#fff'}
      />
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Settings</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Download Settings Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Download Settings</Text>
          
          <SettingRow
            icon="film"
            label="Default Quality"
            value="1080p"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="folder"
            label="Download Folder"
            value="Internal Storage/SnapReel"
            onPress={() => {}}
          />
          
          <ToggleSetting
            icon="wifi"
            label="Download via Wi-Fi only"
            value={wifiOnly}
            onToggle={setWifiOnly}
          />
        </View>

        {/* General Settings Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>General</Text>
          
          <ToggleSetting
            icon="eye"
            label="Auto download preview"
            value={autoPreview}
            onToggle={setAutoPreview}
          />
          
          <SettingRow
            icon="contrast"
            label="Theme"
            value="Dark"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="language"
            label="Language"
            value="English"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="trash"
            label="Clear Cache"
            value="45.2 MB"
            onPress={() => {}}
          />
        </View>

        {/* Notifications Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Notifications</Text>
          
          <ToggleSetting
            icon="notifications"
            label="Enable Notifications"
            value={notifications}
            onToggle={setNotifications}
          />
          
          <SettingRow
            icon="mail"
            label="Email Updates"
            onPress={() => {}}
          />
        </View>

        {/* About Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          
          <SettingRow
            icon="information-circle"
            label="Version"
            value="1.0.0"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="document-text"
            label="Privacy Policy"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="document-lock"
            label="Terms of Use"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="help-circle"
            label="Help & Support"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="star"
            label="Rate Us"
            onPress={() => {}}
          />
          
          <SettingRow
            icon="share-social"
            label="Share App"
            onPress={() => {}}
          />
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
  section: {
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#a78bfa',
    marginBottom: 12,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.05)',
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    flex: 1,
  },
  iconContainer: {
    width: 32,
    height: 32,
    borderRadius: 8,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  settingLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: '#d1d5db',
  },
  settingValue: {
    fontSize: 13,
    color: '#a78bfa',
    fontWeight: '600',
  },

  spacer: {
    height: 20,
  },
});
