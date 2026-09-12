import { useLocalSearchParams, useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

import {
  getRecommendations,
  RecommendationResult,
} from "@/services/recommendationApi";

export default function RecommendationsScreen() {
  const router = useRouter();

  const { object, category, confidence } = useLocalSearchParams<{
    object: string;
    category: string;
    confidence: string;
  }>();

  const [recommendations, setRecommendations] =
    useState<RecommendationResult | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!object || !category || !confidence) {
      setError("Prediction information is missing.");
      setLoading(false);
      return;
    }

    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        setError(null);

        const result = await getRecommendations(
          object,
          category,
          Number(confidence),
        );

        setRecommendations(result);
      } catch (err) {
        console.error("Recommendation error:", err);
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load recommendations.",
        );
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [object, category, confidence]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>What should I do?</Text>

        {/* Loading */}
        {loading && (
          <View style={styles.card}>
            <Text style={styles.loadingText}>
              🔄 Preparing recommendations...
            </Text>
          </View>
        )}

        {/* Error */}
        {!loading && error && (
          <View style={styles.warningCard}>
            <Text style={styles.cardTitle}>⚠️ Recommendations Unavailable</Text>

            <Text style={styles.description}>{error}</Text>
          </View>
        )}

        {/* Recommendations */}
        {!loading && recommendations && (
          <>
            {/* Recommended Action */}
            <View style={styles.actionCard}>
              <Text style={styles.icon}>🌱</Text>

              <Text style={styles.cardTitle}>Recommended Action</Text>

              <Text style={styles.actionText}>
                {recommendations.recommended_action}
              </Text>

              <Text style={styles.sourceText}>
                {recommendations.llm_enhanced
                  ? "Gemini-enhanced guidance"
                  : "Knowledge base guidance"}
              </Text>
            </View>

            {/* Recycling */}
            <View style={styles.card}>
              <Text style={styles.icon}>♻️</Text>

              <Text style={styles.cardTitle}>Recycle</Text>

              <Text style={styles.description}>
                {recommendations.recycling}
              </Text>
            </View>

            {/* Disposal */}
            <View style={styles.card}>
              <Text style={styles.icon}>🗑️</Text>

              <Text style={styles.cardTitle}>Disposal</Text>

              <Text style={styles.description}>{recommendations.disposal}</Text>
            </View>

            {/* Reuse */}
            <View style={styles.card}>
              <Text style={styles.icon}>🌱</Text>

              <Text style={styles.cardTitle}>Reuse</Text>

              {recommendations.reuse.map((item, index) => (
                <Text key={index} style={styles.listItem}>
                  • {item}
                </Text>
              ))}
            </View>

            {/* Upcycling */}
            <View style={styles.card}>
              <Text style={styles.icon}>💡</Text>

              <Text style={styles.cardTitle}>Upcycle</Text>

              {recommendations.upcycling.map((item, index) => (
                <Text key={index} style={styles.listItem}>
                  • {item}
                </Text>
              ))}
            </View>

            {/* Safety */}
            {recommendations.warnings.length > 0 && (
              <View style={styles.warningCard}>
                <Text style={styles.icon}>⚠️</Text>

                <Text style={styles.cardTitle}>Safety</Text>

                {recommendations.warnings.map((warning, index) => (
                  <Text key={index} style={styles.listItem}>
                    • {warning}
                  </Text>
                ))}
              </View>
            )}
          </>
        )}

        {/* Back / Scan Again */}
        <Pressable
          style={styles.camButton}
          onPress={() => router.replace("/camera")}
        >
          <Text style={styles.buttonText}>← Scan Another Item</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#F5F7F5",
  },

  container: {
    flex: 1,
  },

  contentContainer: {
    padding: 24,
    paddingTop: 20,
    paddingBottom: 30,
  },

  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#1B5E20",
    marginBottom: 20,
  },

  card: {
    backgroundColor: "#FFFFFF",
    borderRadius: 18,
    padding: 22,
    marginBottom: 16,
    elevation: 3,
  },

  actionCard: {
    backgroundColor: "#E8F5E9",
    borderRadius: 18,
    padding: 22,
    marginBottom: 16,
    elevation: 3,
  },

  warningCard: {
    backgroundColor: "#FFF8E1",
    borderRadius: 18,
    padding: 22,
    marginBottom: 16,
  },

  icon: {
    fontSize: 30,
    marginBottom: 10,
  },

  cardTitle: {
    fontSize: 21,
    fontWeight: "bold",
    color: "#222",
    marginBottom: 8,
  },

  actionText: {
    fontSize: 20,
    fontWeight: "600",
    color: "#2E7D32",
  },

  sourceText: {
    fontSize: 13,
    color: "#666",
    marginTop: 8,
  },

  description: {
    fontSize: 16,
    color: "#555",
    lineHeight: 24,
  },

  listItem: {
    fontSize: 16,
    color: "#555",
    lineHeight: 25,
    marginBottom: 4,
  },

  loadingText: {
    fontSize: 18,
    fontWeight: "600",
    color: "#2E7D32",
    textAlign: "center",
  },

  camButton: {
    backgroundColor: "#2E7D32",
    padding: 18,
    borderRadius: 14,
    alignItems: "center",
    marginTop: 8,
  },

  buttonText: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "600",
  },
});
