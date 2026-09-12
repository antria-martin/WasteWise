import { fetchWithTimeout, getApiUrl, getErrorMessage } from "./apiConfig";

const RECOMMEND_ENDPOINT = "/api/recommend";

export type RecommendationResult = {
  recommended_action: string;
  recycling: string;
  disposal: string;
  reuse: string[];
  upcycling: string[];
  warnings: string[];
  summary: string;
  llm_enhanced: boolean;
};

export async function getRecommendations(
  object: string,
  category: string,
  confidence: number,
): Promise<RecommendationResult> {
  const response = await fetchWithTimeout(getApiUrl(RECOMMEND_ENDPOINT), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      predicted_object: object,
      predicted_category: category,
      confidence,
    }),
  });

  if (!response.ok) {
    throw new Error(
      await getErrorMessage(response, "Recommendation failed.")
    );
  }

  const data = await response.json();
  const recommendation = data.recommendation ?? {};

  return {
    recommended_action:
      recommendation.recommended_action ?? "Follow local waste disposal guidance.",
    recycling:
      recommendation.summary ??
      recommendation.recommended_action ??
      "Follow local recycling guidance for this item.",
    disposal: Array.isArray(recommendation.disposal_instructions)
      ? recommendation.disposal_instructions.join("\n")
      : "No disposal instructions were returned.",
    reuse: Array.isArray(recommendation.reuse_ideas)
      ? recommendation.reuse_ideas
      : [],
    upcycling: Array.isArray(recommendation.upcycling_ideas)
      ? recommendation.upcycling_ideas
      : [],
    warnings: Array.isArray(recommendation.safety_warnings)
      ? recommendation.safety_warnings
      : [],
    summary: recommendation.summary ?? "",
    llm_enhanced: Boolean(recommendation.llm_enhanced),
  };
}
