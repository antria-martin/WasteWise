import { useLocalSearchParams, useRouter } from "expo-router";
import { Image, Pressable, StyleSheet, Text, View } from "react-native";

export default function ResultScreen() {
  const router = useRouter();

  const { image } = useLocalSearchParams<{
    image: string;
  }>();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Waste Identified</Text>

      {image && <Image source={{ uri: image }} style={styles.image} />}

      <View style={styles.resultCard}>
        <Text style={styles.itemName}>Plastic Bottle</Text>

        <Text style={styles.category}>Category: Plastic</Text>

        <View style={styles.confidenceContainer}>
          <Text style={styles.confidenceLabel}>Confidence</Text>

          <Text style={styles.confidence}>94%</Text>
        </View>
      </View>

      <Pressable
        style={styles.recommendButton}
        onPress={() => router.push("/recommendations")}
      >
        <Text style={styles.buttonText}>View Recommendations →</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F5F7F5",
    padding: 24,
    paddingTop: 60,
  },

  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#1B5E20",
    marginBottom: 20,
  },

  image: {
    width: "100%",
    height: 280,
    borderRadius: 20,
    marginBottom: 24,
  },

  resultCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 18,
    padding: 22,
    elevation: 3,
  },

  itemName: {
    fontSize: 26,
    fontWeight: "bold",
    color: "#222",
    marginBottom: 8,
  },

  category: {
    fontSize: 17,
    color: "#555",
    marginBottom: 20,
  },

  confidenceContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },

  confidenceLabel: {
    fontSize: 16,
    color: "#666",
  },

  confidence: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#2E7D32",
  },

  recommendButton: {
    backgroundColor: "#2E7D32",
    padding: 18,
    borderRadius: 14,
    alignItems: "center",
    marginTop: 24,
  },

  buttonText: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "600",
  },
});
