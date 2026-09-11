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

      {/* Camera guidance overlay */}
      <View style={styles.overlay} pointerEvents="none">
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Scan Waste</Text>

          <Text style={styles.headerSubtitle}>
            Place ONE waste item inside the frame
          </Text>
        </View>

        {/* Framing guide */}
        <View style={styles.frameContainer}>
          <View style={styles.frame}>
            <View style={[styles.corner, styles.topLeft]} />
            <View style={[styles.corner, styles.topRight]} />
            <View style={[styles.corner, styles.bottomLeft]} />
            <View style={[styles.corner, styles.bottomRight]} />
          </View>
        </View>

        {/* Instructions */}
        <View style={styles.instructions}>
          <Text style={styles.instructionsTitle}>For best results</Text>

          <Text style={styles.instruction}>✓ One waste item only</Text>

          <Text style={styles.instruction}>✓ No hands or other objects</Text>

          <Text style={styles.instruction}>✓ Use a clear background</Text>

          <Text style={styles.instruction}>✓ Keep the entire item visible</Text>
        </View>
      </View>

      {/* Camera controls */}
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

  /*
   * Guidance overlay sits above the camera.
   * It does not interfere with camera interaction.
   */
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    alignItems: "center",
  },

  header: {
    width: "100%",
    alignItems: "center",
    paddingTop: 55,
    paddingHorizontal: 24,
  },

  headerTitle: {
    color: "#FFFFFF",
    fontSize: 28,
    fontWeight: "bold",
    textShadowColor: "rgba(0,0,0,0.7)",
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 4,
  },

  headerSubtitle: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "500",
    textAlign: "center",
    marginTop: 6,
    textShadowColor: "rgba(0,0,0,0.7)",
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 4,
  },

  frameContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
  },

  frame: {
    width: "78%",
    height: "45%",
    position: "relative",
  },

  corner: {
    position: "absolute",
    width: 32,
    height: 32,
    borderColor: "#FFFFFF",
  },

  topLeft: {
    top: 0,
    left: 0,
    borderTopWidth: 4,
    borderLeftWidth: 4,
    borderTopLeftRadius: 8,
  },

  topRight: {
    top: 0,
    right: 0,
    borderTopWidth: 4,
    borderRightWidth: 4,
    borderTopRightRadius: 8,
  },

  bottomLeft: {
    bottom: 0,
    left: 0,
    borderBottomWidth: 4,
    borderLeftWidth: 4,
    borderBottomLeftRadius: 8,
  },

  bottomRight: {
    bottom: 0,
    right: 0,
    borderBottomWidth: 4,
    borderRightWidth: 4,
    borderBottomRightRadius: 8,
  },

  instructions: {
    backgroundColor: "rgba(0, 0, 0, 0.65)",
    borderRadius: 16,
    paddingVertical: 14,
    paddingHorizontal: 20,
    marginBottom: 190,
    width: "88%",
  },

  instructionsTitle: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 6,
  },

  instruction: {
    color: "#FFFFFF",
    fontSize: 14,
    lineHeight: 21,
  },

  controls: {
    position: "absolute",
    bottom: 40,
    width: "100%",
    alignItems: "center",
    zIndex: 10,
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
