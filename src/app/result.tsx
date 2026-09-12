import { useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { Image, Pressable, StyleSheet, Text, View } from "react-native";

import { getCapturedImageUri } from "@/services/capturedImage";
import { PredictionResult, predictWaste } from "@/services/predictionApi";

export default function ResultScreen() {
  const router = useRouter();

  const [imageUri, setImageUri] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const uri = getCapturedImageUri();

    console.log("RESULT IMAGE URI:", uri);

    if (!uri) {
      setError("No image was provided.");
      setLoading(false);
      return;
    }

    setImageUri(uri);

    const runPrediction = async () => {
      try {
        setLoading(true);
        setError(null);

        const result = await predictWaste(uri);

        setPrediction(result);
      } catch (err) {
        console.error("Prediction error:", err);

        setError(
          err instanceof Error
            ? err.message
            : "Unable to identify the waste item.",
        );
      } finally {
        setLoading(false);
      }
    };

    runPrediction();
  }, []);

  const formatLabel = (value: string | null) => {
    if (!value) return "Unknown";

    return value
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Waste Identification</Text>

      {imageUri && <Image source={{ uri: imageUri }} style={styles.image} />}

      {/* Loading */}
      {loading && (
        <View style={styles.resultCard}>
          <Text style={styles.loadingText}>Analyzing waste...</Text>
        </View>
      )}

      {/* API / Network Error */}
      {!loading && error && (
        <>
          <View style={styles.errorCard}>
            <Text style={styles.errorTitle}>Identification Failed</Text>

            <Text style={styles.errorText}>{error}</Text>
          </View>

          <Pressable
            style={styles.backButton}
            onPress={() => router.replace("/")}
          >
            <Text style={styles.buttonText}>Scan Another Item</Text>
          </Pressable>
        </>
      )}

      {/* Prediction received */}
      {!loading && !error && prediction && (
        <>
          {/* Unidentifiable */}
          {!prediction.identifiable && (
            <>
              <View style={styles.errorCard}>
                <Text style={styles.errorTitle}>
                  Item Could Not Be Identified
                </Text>

                <Text style={styles.errorText}>
                  {prediction.message ??
                    "The item could not be identified confidently. Please upload a clearer image or ensure that the image contains a trash item."}
                </Text>
              </View>

              <Pressable
                style={styles.backButton}
                onPress={() => router.replace("/")}
              >
                <Text style={styles.buttonText}>Scan Another Item</Text>
              </Pressable>
            </>
          )}

          {/* Identifiable prediction */}
          {prediction.identifiable && (
            <>
              <View style={styles.resultCard}>
                <Text style={styles.itemName}>
                  {formatLabel(prediction.object)}
                </Text>

                <Text style={styles.category}>
                  Waste Category: {formatLabel(prediction.category)}
                </Text>

                <View style={styles.confidenceRow}>
                  <Text style={styles.confidenceLabel}>Model Confidence</Text>

                  <Text style={styles.confidence}>
                    {Math.round(prediction.confidence * 100)}%
                  </Text>
                </View>

                <View style={styles.consistencyContainer}>
                  <Text style={styles.consistencyLabel}>Identification</Text>

                  <Text style={styles.consistency}>Verified</Text>
                </View>
              </View>

              <Pressable
                style={styles.recommendButton}
                onPress={() =>
                  router.push({
                    pathname: "/recommendations",
                    params: {
                      object: prediction.object ?? "",
                      category: prediction.category ?? "",
                      confidence: prediction.confidence.toString(),
                    },
                  })
                }
              >
                <Text style={styles.buttonText}>View Recommendations</Text>
              </Pressable>
            </>
          )}
        </>
      )}
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

  confidenceRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },

  confidenceLabel: {
    fontSize: 16,
    color: "#666",
  },

  confidence: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#2E7D32",
  },

  consistencyContainer: {
    borderTopWidth: 1,
    borderTopColor: "#E0E0E0",
    paddingTop: 14,
    marginTop: 4,
    flexDirection: "row",
    justifyContent: "space-between",
  },

  consistencyLabel: {
    fontSize: 16,
    color: "#666",
  },

  consistency: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#2E7D32",
  },

  loadingText: {
    fontSize: 18,
    fontWeight: "600",
    color: "#2E7D32",
    textAlign: "center",
  },

  errorCard: {
    backgroundColor: "#FFF8E1",
    borderRadius: 18,
    padding: 22,
  },

  errorTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#8A5A00",
    marginBottom: 8,
  },

  errorText: {
    fontSize: 16,
    color: "#555",
    lineHeight: 24,
  },

  warningCard: {
    backgroundColor: "#FFF8E1",
    borderRadius: 18,
    padding: 22,
    marginTop: 24,
  },

  warningTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#8A5A00",
    marginBottom: 8,
  },

  warningText: {
    fontSize: 16,
    color: "#555",
    lineHeight: 24,
  },

  recommendButton: {
    backgroundColor: "#2E7D32",
    padding: 18,
    borderRadius: 14,
    alignItems: "center",
    marginTop: 24,
  },

  backButton: {
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
