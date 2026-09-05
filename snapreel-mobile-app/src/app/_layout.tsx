import 'react-native-gesture-handler';
import { Drawer } from 'expo-router/drawer';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useNavigation } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import Toast from 'react-native-toast-message';
import { ShareIntentProvider } from 'expo-share-intent';

function DrawerContent() {
  const navigation = useNavigation();
  const router = useRouter();

  const MenuItem = ({ icon, label, route }: { icon: string; label: string; route: string }) => (
    <TouchableOpacity
      style={styles.menuItem}
      onPress={() => {
        try {
          if (route === 'index') {
            router.push('/');
          } else {
            router.push(`/${route}` as any);
          }
        } catch (err) {
          console.error("Navigation error:", err);
        }
      }}
    >
      <Ionicons name={icon as any} size={22} color="#a78bfa" />
      <Text style={styles.menuItemText}>{label}</Text>
    </TouchableOpacity>
  );

  return (
    <GestureHandlerRootView style={styles.drawerContainer}>
      <ScrollView style={styles.drawer} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.drawerHeader}>
          <View style={styles.drawerLogoContainer}>
            <Ionicons name="download-outline" size={32} color="#a78bfa" />
          </View>
          <Text style={styles.drawerBrand}>SnapReel</Text>
          <Text style={styles.drawerBrandSub}>Downloader</Text>
        </View>

        {/* Premium Banner */}
        <TouchableOpacity style={styles.premiumBanner}>
          <Ionicons name="star" size={24} color="#ffd700" />
          <View style={{ flex: 1 }}>
            <Text style={styles.premiumBannerTitle}>Go Premium</Text>
            <Text style={styles.premiumBannerSub}>No ads, faster downloads</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color="#a78bfa" />
        </TouchableOpacity>

        {/* Main Menu */}
        <View style={styles.menuSection}>
          <MenuItem icon="home" label="Home" route="index" />
          <MenuItem icon="download" label="My Downloads" route="downloads" />
          <MenuItem icon="globe" label="Browser" route="browser" />
          <MenuItem icon="help-circle" label="How to Use" route="how-to-use" />
          <MenuItem icon="apps" label="Supported Platforms" route="supported-platforms" />
        </View>

        {/* Settings & Info */}
        <View style={styles.menuSection}>
          <MenuItem icon="settings" label="Settings" route="settings" />
          <MenuItem icon="share-social" label="Share App" route="index" />
          <MenuItem icon="star-outline" label="Rate Us" route="index" />
          <MenuItem icon="help" label="Help & Support" route="index" />
        </View>

        {/* App Info */}
        <View style={styles.appInfo}>
          <Text style={styles.appInfoVersion}>Version 1.0.0</Text>
          <TouchableOpacity>
            <Text style={styles.appInfoLink}>Privacy Policy</Text>
          </TouchableOpacity>
          <TouchableOpacity>
            <Text style={styles.appInfoLink}>Terms of Use</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </GestureHandlerRootView>
  );
}

export default function Layout() {
  return (
    <ShareIntentProvider options={{ debug: false }}>
      <SafeAreaProvider>
      <Drawer
        screenOptions={{
          headerStyle: {
            backgroundColor: '#0f1419',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: '700',
          },
          sceneContainerStyle: {
            backgroundColor: '#0f1419',
          },
          drawerStyle: {
            backgroundColor: '#0f1419',
            width: '75%',
          },
          drawerInactiveTintColor: '#6b7280',
          drawerActiveTintColor: '#a78bfa',
        }}
        drawerContent={DrawerContent}
      >
        <Drawer.Screen
          name="index"
          options={{
            title: 'SnapReel Downloader',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="downloads"
          options={{
            title: 'My Downloads',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="browser"
          options={{
            title: 'Browser',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="settings"
          options={{
            title: 'Settings',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="how-to-use"
          options={{
            title: 'How to Use',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="supported-platforms"
          options={{
            title: 'Supported Platforms',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="premium"
          options={{
            title: 'Go Premium',
            headerShown: false,
          }}
        />
        <Drawer.Screen
          name="explore"
          options={{
            href: null,
          }}
        />
      </Drawer>
      <Toast />
    </SafeAreaProvider>
    </ShareIntentProvider>
  );
}

const styles = StyleSheet.create({
  drawerContainer: {
    flex: 1,
    backgroundColor: '#0f1419',
  },
  drawer: {
    flex: 1,
    backgroundColor: '#0f1419',
  },
  drawerHeader: {
    alignItems: 'center',
    paddingVertical: 24,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  drawerLogoContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  drawerBrand: {
    fontSize: 20,
    fontWeight: '700',
    color: '#fff',
  },
  drawerBrandSub: {
    fontSize: 14,
    fontWeight: '600',
    color: '#a78bfa',
  },
  premiumBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginHorizontal: 12,
    marginVertical: 16,
    paddingHorizontal: 12,
    paddingVertical: 12,
    backgroundColor: 'rgba(255, 215, 0, 0.1)',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: 'rgba(255, 215, 0, 0.2)',
  },
  premiumBannerTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#ffd700',
  },
  premiumBannerSub: {
    fontSize: 11,
    color: '#9ca3af',
    marginTop: 2,
  },
  menuSection: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  menuItemText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#d1d5db',
  },
  appInfo: {
    paddingHorizontal: 16,
    paddingVertical: 16,
    marginTop: 'auto',
  },
  appInfoVersion: {
    fontSize: 11,
    color: '#6b7280',
    marginBottom: 8,
  },
  appInfoLink: {
    fontSize: 11,
    color: '#a78bfa',
    marginBottom: 6,
  },
});
