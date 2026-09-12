import { fetchWithTimeout, getApiUrl, getErrorMessage } from "./apiConfig";

export type HealthResult = {
  status: string;
  service?: string;
  confidence_threshold?: number;
  models?: {
    model_present?: boolean;
    inference_bundle_present?: boolean;
  };
};

export async function checkBackendHealth(): Promise<HealthResult> {
  const response = await fetchWithTimeout(getApiUrl("/api/health"), {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(await getErrorMessage(response, "Health check failed."));
  }

  return response.json();
}
