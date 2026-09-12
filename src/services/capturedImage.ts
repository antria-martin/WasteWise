let capturedImageUri: string | null = null;

export function setCapturedImageUri(uri: string) {
  capturedImageUri = uri;
}

export function getCapturedImageUri(): string | null {
  return capturedImageUri;
}

export function clearCapturedImageUri() {
  capturedImageUri = null;
}
