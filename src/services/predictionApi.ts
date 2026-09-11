const API_BASE_URL =
  process.env.EXPO_PUBLIC_PREDICT_API_URL ?? "";

const PREDICT_ENDPOINT = "/predict";
const IMAGE_FIELD_NAME = "image";

export type PredictionResult = {
  identifiable: boolean;
  object: string | null;
  object_confidence: number;
  category: string | null;
  category_confidence: number;
  mapped_category: string | null;
  consistent: boolean;
  message?: string;
};

export async function predictWaste(
  imageUri: string
): Promise<PredictionResult> {
  const formData = new FormData();

  formData.append(
    IMAGE_FIELD_NAME,
    {
      uri: imageUri,
      name: "waste.jpg",
      type: "image/jpeg",
    } as any
  );

  const response = await fetch(
    `${API_BASE_URL}${PREDICT_ENDPOINT}`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(
      `Prediction API failed with status ${response.status}`
    );
  }

  const data = await response.json();

  return {
    identifiable: data.identifiable,
    object: data.object,
    object_confidence: data.object_confidence,
    category: data.category,
    category_confidence: data.category_confidence,
    mapped_category: data.mapped_category,
    consistent: data.consistent,
    message: data.message,
  };
}