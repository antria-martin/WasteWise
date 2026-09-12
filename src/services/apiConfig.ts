const REQUEST_TIMEOUT_MS = 30000;

export function getApiBaseUrl(): string {
  const baseUrl = process.env.EXPO_PUBLIC_API_BASE_URL?.trim();

  if (!baseUrl) {
    throw new Error(
      "Backend API URL is not configured. Set EXPO_PUBLIC_API_BASE_URL to your FastAPI server address.",
    );
  }

  return baseUrl.replace(/\/+$/, "");
}

export function getApiUrl(path: string): string {
  return `${getApiBaseUrl()}${path.startsWith("/") ? path : `/${path}`}`;
}

export async function fetchWithTimeout(
  input: RequestInfo | URL,
  init: RequestInit = {},
  timeoutMs: number = REQUEST_TIMEOUT_MS,
): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(input, {
      ...init,
      signal: controller.signal,
    });
  } catch (error) {
    console.error("Original fetch error:", error);

    if (error instanceof Error && error.name === "AbortError") {
      throw new Error(`Backend request timed out: ${error.message}`);
    }

    throw new Error(
      `Backend is unreachable: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
  } finally {
    clearTimeout(timeout);
  }
}

export async function getErrorMessage(
  response: Response,
  fallback: string,
): Promise<string> {
  try {
    const data = await response.json();
    if (typeof data?.detail === "string") {
      return data.detail;
    }
  } catch {
    // Response body was not JSON; use the supplied fallback below.
  }

  return `${fallback} Status: ${response.status}`;
}
