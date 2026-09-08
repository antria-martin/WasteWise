import { CameraType, CameraView, useCameraPermissions } from "expo-camera";
import { useRouter } from "expo-router";
import { useRef, useState } from "react";
import {
  Button,
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function CameraScreen() {
  const insets = useSafeAreaInsets();
  const router = useRouter();

  const [permission, requestPermission] = useCameraPermissions();

  const [facing, setFacing] = useState<CameraType>("back");

  const [photo, setPhoto] = useState<string | null>(null);

  const cameraRef = useRef<CameraView>(null);

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.permissionContainer}>
        <Text style={styles.permissionText}>
          WasteWise needs access to your camera.
        </Text>

        <Button title="Allow Camera" onPress={requestPermission} />
      </View>
    );
  }

  // Show photo preview
  if (photo) {
    return (
      <View style={styles.previewContainer}>
        <Image source={{ uri: photo }} style={styles.previewImage} />

        <View
          style={[
            styles.previewControls,
            { paddingBottom: insets.bottom + 16 },
          ]}
        >
          <TouchableOpacity
            style={styles.retakeButton}
            onPress={() => setPhoto(null)}
          >
            <Text style={styles.buttonText}>↩ Retake</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.useButton}
            onPress={() => {
              router.push({
                pathname: "/result",
                params: {
                  image: photo,
                },
              });
            }}
          >
            <Text style={styles.buttonText}>✓ Use Photo</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  // Camera screen
  return (
    <View style={styles.container}>
      <CameraView ref={cameraRef} style={styles.camera} facing={facing} />

      <View style={[styles.controls, { paddingBottom: insets.bottom + 16 }]}>
        <TouchableOpacity
          style={styles.captureButton}
          onPress={async () => {
            if (!cameraRef.current) {
              return;
            }

            const capturedPhoto = await cameraRef.current.takePictureAsync();

            if (capturedPhoto?.uri) {
              setPhoto(capturedPhoto.uri);
            }
          }}
        >
          <View style={styles.captureInner} />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.flipButton}
          onPress={() => {
            setFacing((current) => (current === "back" ? "front" : "back"));
          }}
        >
          <Text style={styles.flipText}>🔄</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
  },

  camera: {
    flex: 1,
  },

  controls: {
    position: "absolute",
    bottom: 40,
    width: "100%",
    alignItems: "center",
  },

  captureButton: {
    width: 78,
    height: 78,
    borderRadius: 39,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },

  captureInner: {
    width: 64,
    height: 64,
    borderRadius: 32,
    borderWidth: 3,
    borderColor: "#2E7D32",
  },

  flipButton: {
    position: "absolute",
    right: 30,
    top: 20,
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: "rgba(0,0,0,0.5)",
    alignItems: "center",
    justifyContent: "center",
  },

  flipText: {
    fontSize: 24,
  },

  previewContainer: {
    flex: 1,
    backgroundColor: "#000",
  },

  previewImage: {
    flex: 1,
    width: "100%",
    resizeMode: "contain",
  },

  previewControls: {
    position: "absolute",
    bottom: 40,
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-evenly",
  },

  retakeButton: {
    backgroundColor: "#555",
    paddingVertical: 16,
    paddingHorizontal: 28,
    borderRadius: 14,
  },

  useButton: {
    backgroundColor: "#2E7D32",
    paddingVertical: 16,
    paddingHorizontal: 28,
    borderRadius: 14,
  },

  buttonText: {
    color: "#fff",
    fontSize: 17,
    fontWeight: "600",
  },

  permissionContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 30,
  },

  permissionText: {
    fontSize: 18,
    textAlign: "center",
    marginBottom: 20,
  },
});
