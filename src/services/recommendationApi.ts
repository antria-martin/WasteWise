const API_BASE_URL = process.env.EXPO_PUBLIC_RECOMMEND_API_URL ?? "";

const RECOMMEND_ENDPOINT = "/recommend";

export type RecommendationResult = {
  recommended_action: string;
  recycling: string;
  disposal: string;
  reuse: string[];
  upcycling: string[];
  warnings: string[];
};

export async function getRecommendations(
  object: string,
  category: string,
  confidence: number,
): Promise<RecommendationResult> {
  const response = await fetch(`${API_BASE_URL}${RECOMMEND_ENDPOINT}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      object: object,
      category: category,
      confidence: confidence,
    }),
  });

  if (!response.ok) {
    throw new Error(`Recommendation API failed with status ${response.status}`);
  }

  const data = await response.json();

  return {
    recommended_action: data.recommended_action,
    recycling: data.recycling,
    disposal: data.disposal,
    reuse: data.reuse,
    upcycling: data.upcycling,
    warnings: data.warnings,
  };
}
