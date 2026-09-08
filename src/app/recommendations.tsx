import { useRouter } from "expo-router";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function RecommendationsScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>What should I do?</Text>

        {/* Recommended Action */}

        <View style={styles.card}>
          <Text style={styles.icon}>♻️</Text>

          <Text style={styles.cardTitle}>Recycle</Text>

          <Text style={styles.description}>
            Empty, rinse and dry the plastic bottle before placing it in the
            appropriate recycling stream.
          </Text>
        </View>

        {/* Reuse */}

        <View style={styles.card}>
          <Text style={styles.icon}>🌱</Text>

          <Text style={styles.cardTitle}>Reuse</Text>

          <Text style={styles.description}>
            Use the bottle as a small plant pot or storage container.
          </Text>
        </View>

        {/* Upcycling */}

        <View style={styles.card}>
          <Text style={styles.icon}>💡</Text>

          <Text style={styles.cardTitle}>Upcycle</Text>

          <Text style={styles.description}>
            Turn the bottle into a hanging planter or creative storage
            container.
          </Text>
        </View>

        {/* Warning */}

        <View style={styles.warningCard}>
          <Text style={styles.icon}>⚠️</Text>

          <Text style={styles.cardTitle}>Safety</Text>

          <Text style={styles.description}>Do not burn plastic.</Text>
        </View>

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
    fontSize: 30,
    fontWeight: "bold",
    color: "#1B5E20",
    marginBottom: 24,
  },

  card: {
    backgroundColor: "#FFFFFF",
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
    elevation: 2,
  },

  icon: {
    fontSize: 32,
    marginBottom: 8,
  },

  cardTitle: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#222",
    marginBottom: 8,
  },

  description: {
    fontSize: 16,
    lineHeight: 24,
    color: "#555",
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
