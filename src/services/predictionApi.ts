import * as FileSystem from "expo-file-system/legacy";
import { getApiUrl } from "./apiConfig";

const PREDICT_ENDPOINT = "/api/predict";

export type TopPrediction = {
  object: string;
  category: string;
  confidence: number;
};

export type PredictionResult = {
  identifiable: boolean;
  object: string | null;
  category: string | null;
  confidence: number;
  message?: string;
  top_k_predictions: TopPrediction[];
  latency?: {
    cv_latency_ms?: number;
  };
  preprocessed_preview?: string;
};

export async function predictWaste(
  imageUri: string,
): Promise<PredictionResult> {
  console.log("IMAGE URI:", imageUri);

  // Upload the camera file directly.
  const result = await FileSystem.uploadAsync(
    getApiUrl(PREDICT_ENDPOINT),
    imageUri,
    {
      httpMethod: "POST",
      uploadType: FileSystem.FileSystemUploadType.MULTIPART,
      fieldName: "image",
      mimeType: "image/jpeg",
    },
  );

  console.log("UPLOAD STATUS:", result.status);
  console.log("UPLOAD RESPONSE:", result.body);

  if (result.status < 200 || result.status >= 300) {
    let message = "Prediction failed.";

    try {
      const data = JSON.parse(result.body);

      if (typeof data?.detail === "string") {
        message = data.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(`${message} Status: ${result.status}`);
  }

  const data = JSON.parse(result.body);

  return {
    identifiable: Boolean(data.identifiable),
    object: data.object ?? null,
    category: data.category ?? null,
    confidence: Number(data.confidence ?? 0),
    message: data.message,
    top_k_predictions: Array.isArray(data.top_k_predictions)
      ? data.top_k_predictions
      : [],
    latency: data.latency,
    preprocessed_preview: data.preprocessed_preview,
  };
}
