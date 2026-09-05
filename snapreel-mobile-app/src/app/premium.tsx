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

export default function PremiumScreen() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  const Feature = ({ icon, title, desc }: { icon: string; title: string; desc: string }) => (
    <View style={styles.featureItem}>
      <View style={styles.featureIconContainer}>
        <Ionicons name={icon as any} size={24} color="#ffd700" />
      </View>
      <View style={{ flex: 1 }}>
        <Text style={styles.featureTitle}>{title}</Text>
        <Text style={styles.featureDesc}>{desc}</Text>
      </View>
    </View>
  );

  const PricingPlan = ({
    period,
    price,
    savings,
  }: {
    period: string;
    price: string;
    savings?: string;
  }) => (
    <View style={[styles.planCard, savings && styles.planCardPopular]}>
      {savings && (
        <View style={styles.savingsBadge}>
          <Text style={styles.savingsText}>Save {savings}</Text>
        </View>
      )}
      <Text style={styles.planPeriod}>{period}</Text>
      <Text style={styles.planPrice}>${price}</Text>
      <TouchableOpacity style={styles.upgradeButton}>
        <Text style={styles.upgradeButtonText}>Upgrade Now</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={[styles.header, { paddingTop: insets.top + 16 }]}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="chevron-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Go Premium</Text>
        <View style={{ width: 24 }} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Hero Section */}
        <View style={styles.heroSection}>
          <View style={styles.premiumBadge}>
            <Ionicons name="star" size={32} color="#ffd700" />
          </View>
          <Text style={styles.heroTitle}>Go Premium</Text>
          <Text style={styles.heroSubtitle}>
            No ads, faster downloads, high quality and more.
          </Text>
        </View>

        {/* Premium Features */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Premium Features</Text>
          
          <Feature
            icon="flash"
            title="Faster Downloads"
            desc="Get priority access to download servers"
          />
          <Feature
            icon="document-lock"
            title="Ad-Free Experience"
            desc="Download without any interruptions"
          />
          <Feature
            icon="film"
            title="Maximum Quality"
            desc="Download videos in 4K and highest quality"
          />
          <Feature
            icon="download"
            title="Batch Downloads"
            desc="Download multiple videos at once"
          />
          <Feature
            icon="lock-closed"
            title="Enhanced Security"
            desc="Extra privacy and security features"
          />
          <Feature
            icon="infinite"
            title="Unlimited Downloads"
            desc="No daily or monthly download limits"
          />
        </View>

        {/* Pricing Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Choose Your Plan</Text>
          
          <View style={styles.pricingContainer}>
            <PricingPlan period="Monthly" price="4.99" />
            <PricingPlan
              period="Yearly"
              price="39.99"
              savings="33%"
            />
          </View>

          <View style={styles.autoRenewal}>
            <Ionicons name="information-circle" size={16} color="#a78bfa" />
            <Text style={styles.autoRenewalText}>
              All plans auto-renew. Cancel anytime from your account.
            </Text>
          </View>
        </View>

        {/* Comparison Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Free vs Premium</Text>
          
          <View style={styles.comparisonTable}>
            <View style={styles.comparisonHeader}>
              <Text style={styles.comparisonHeaderText}></Text>
              <Text style={styles.comparisonHeaderText}>Free</Text>
              <Text style={styles.comparisonHeaderText}>Premium</Text>
            </View>

            <ComparisonRow label="Ad-Free" free={false} premium={true} />
            <ComparisonRow label="Max Quality" free="720p" premium="4K" />
            <ComparisonRow label="Download Speed" free="Standard" premium="5x Faster" />
            <ComparisonRow label="Batch Download" free={false} premium={true} />
            <ComparisonRow label="Priority Support" free={false} premium={true} />
            <ComparisonRow label="Cloud Storage" free={false} premium={true} />
          </View>
        </View>

        {/* FAQ Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>FAQ</Text>
          
          <FAQItem
            question="Can I cancel anytime?"
            answer="Yes, you can cancel your subscription anytime. Your access will continue until the end of your billing period."
          />
          <FAQItem
            question="Is there a free trial?"
            answer="Yes, we offer a 7-day free trial. No credit card required to start your trial."
          />
          <FAQItem
            question="What payment methods do you accept?"
            answer="We accept all major credit cards, PayPal, and other popular payment methods."
          />
          <FAQItem
            question="Can I upgrade or downgrade?"
            answer="Yes, you can change your plan anytime. Changes take effect on your next billing cycle."
          />
        </View>

        {/* CTA Section */}
        <View style={styles.ctaSection}>
          <TouchableOpacity style={styles.ctaButton}>
            <Ionicons name="star" size={20} color="#fff" />
            <Text style={styles.ctaButtonText}>Start 7-Day Free Trial</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.restoreButton}>
            <Text style={styles.restoreButtonText}>Restore Purchase</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.spacer} />
      </ScrollView>
    </View>
  );
}

const ComparisonRow = ({
  label,
  free,
  premium,
}: {
  label: string;
  free: boolean | string;
  premium: boolean | string;
}) => (
  <View style={styles.comparisonRow}>
    <Text style={styles.comparisonLabel}>{label}</Text>
    <View style={styles.comparisonCell}>
      {typeof free === 'boolean' ? (
        free ? (
          <Ionicons name="checkmark-circle" size={20} color="#22c55e" />
        ) : (
          <Ionicons name="close-circle" size={20} color="#6b7280" />
        )
      ) : (
        <Text style={styles.comparisonCellText}>{free}</Text>
      )}
    </View>
    <View style={styles.comparisonCell}>
      {typeof premium === 'boolean' ? (
        <Ionicons name="checkmark-circle" size={20} color="#22c55e" />
      ) : (
        <Text style={styles.comparisonCellText}>{premium}</Text>
      )}
    </View>
  </View>
);

const FAQItem = ({
  question,
  answer,
}: {
  question: string;
  answer: string;
}) => (
  <View style={styles.faqItem}>
    <View style={styles.faqQuestionRow}>
      <Ionicons name="help-circle" size={16} color="#a78bfa" />
      <Text style={styles.faqQuestion}>{question}</Text>
    </View>
    <Text style={styles.faqAnswer}>{answer}</Text>
  </View>
);

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
  heroSection: {
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 32,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  premiumBadge: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255, 215, 0, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 8,
  },
  heroSubtitle: {
    fontSize: 14,
    color: '#9ca3af',
    textAlign: 'center',
  },
  section: {
    paddingHorizontal: 20,
    paddingVertical: 24,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 16,
  },
  featureItem: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  featureIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 215, 0, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
    flexShrink: 0,
  },
  featureTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 2,
  },
  featureDesc: {
    fontSize: 12,
    color: '#9ca3af',
  },
  pricingContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  planCard: {
    flex: 1,
    paddingHorizontal: 16,
    paddingVertical: 20,
    borderRadius: 12,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.2)',
    alignItems: 'center',
  },
  planCardPopular: {
    backgroundColor: 'rgba(167, 139, 250, 0.15)',
    borderColor: '#a78bfa',
  },
  savingsBadge: {
    backgroundColor: '#f97316',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 6,
    marginBottom: 12,
  },
  savingsText: {
    fontSize: 10,
    fontWeight: '700',
    color: '#fff',
  },
  planPeriod: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 8,
  },
  planPrice: {
    fontSize: 28,
    fontWeight: '700',
    color: '#a78bfa',
    marginBottom: 12,
  },
  upgradeButton: {
    width: '100%',
    paddingVertical: 10,
    backgroundColor: '#a78bfa',
    borderRadius: 8,
    alignItems: 'center',
  },
  upgradeButtonText: {
    fontSize: 13,
    fontWeight: '600',
    color: '#fff',
  },
  autoRenewal: {
    flexDirection: 'row',
    gap: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: 'rgba(167, 139, 250, 0.05)',
    borderRadius: 8,
    marginTop: 12,
  },
  autoRenewalText: {
    flex: 1,
    fontSize: 11,
    color: '#a78bfa',
    lineHeight: 14,
  },
  comparisonTable: {
    borderRadius: 8,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: 'rgba(167, 139, 250, 0.1)',
  },
  comparisonHeader: {
    flexDirection: 'row',
    backgroundColor: 'rgba(167, 139, 250, 0.1)',
    paddingHorizontal: 12,
    paddingVertical: 12,
  },
  comparisonHeaderText: {
    flex: 1,
    fontSize: 12,
    fontWeight: '700',
    color: '#a78bfa',
    textAlign: 'center',
  },
  comparisonRow: {
    flexDirection: 'row',
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  comparisonLabel: {
    flex: 1,
    fontSize: 12,
    fontWeight: '500',
    color: '#d1d5db',
  },
  comparisonCell: {
    flex: 1,
    alignItems: 'center',
  },
  comparisonCellText: {
    fontSize: 11,
    color: '#9ca3af',
  },
  faqItem: {
    marginBottom: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(167, 139, 250, 0.1)',
  },
  faqQuestionRow: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 8,
    alignItems: 'center',
  },
  faqQuestion: {
    fontSize: 13,
    fontWeight: '600',
    color: '#fff',
  },
  faqAnswer: {
    fontSize: 12,
    color: '#9ca3af',
    lineHeight: 16,
    marginLeft: 24,
  },
  ctaSection: {
    paddingHorizontal: 20,
    paddingVertical: 24,
  },
  ctaButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    paddingVertical: 16,
    backgroundColor: '#a78bfa',
    borderRadius: 12,
    marginBottom: 12,
  },
  ctaButtonText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#fff',
  },
  restoreButton: {
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: '#a78bfa',
    borderRadius: 8,
    alignItems: 'center',
  },
  restoreButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#a78bfa',
  },
  spacer: {
    height: 20,
  },
});
