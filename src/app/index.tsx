import * as ImagePicker from "expo-image-picker";
import { useRouter } from "expo-router";
import { Pressable, StyleSheet, Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function HomeScreen() {
  const router = useRouter();

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      allowsEditing: false,
      quality: 1,
    });

    if (!result.canceled) {
      const imageUri = result.assets[0].uri;

      router.push({
        pathname: "/result",
        params: {
          image: imageUri,
        },
      });
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.logo}>♻️</Text>

      <Text style={styles.title}>WasteWise</Text>

      <Text style={styles.subtitle}>Smart waste management powered by AI</Text>

      <Pressable
        style={styles.scanButton}
        onPress={() => router.push("/camera")}
      >
        <Text style={styles.buttonText}>📷 Scan Waste</Text>
      </Pressable>

      <Pressable style={styles.uploadButton} onPress={pickImage}>
        <Text style={styles.buttonText}>🖼️ Upload Image</Text>
      </Pressable>

      <Text style={styles.description}>
        Identify • Recycle • Reuse • Upcycle
      </Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
    backgroundColor: "#F5F7F5",
  },

  logo: {
    fontSize: 60,
    marginBottom: 10,
  },

  title: {
    fontSize: 38,
    fontWeight: "bold",
    color: "#1B5E20",
  },

  subtitle: {
    fontSize: 16,
    color: "#666",
    marginTop: 8,
    marginBottom: 40,
    textAlign: "center",
  },

  scanButton: {
    width: "100%",
    padding: 18,
    borderRadius: 14,
    backgroundColor: "#2E7D32",
    alignItems: "center",
    marginBottom: 16,
  },

  uploadButton: {
    width: "100%",
    padding: 18,
    borderRadius: 14,
    backgroundColor: "#81C784",
    alignItems: "center",
  },

  buttonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "600",
  },

  description: {
    marginTop: 40,
    fontSize: 14,
    color: "#777",
  },
});
