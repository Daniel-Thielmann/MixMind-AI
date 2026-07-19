import type { UploadAnalysisResponse } from "@/types";

const ANALYZE_AUTHORIZATION_ENDPOINT = "/api/analyze/authorize";
const FRIENDLY_ERROR_MESSAGE =
  "Unable to analyze the selected tracks. Please try again.";
export const AUTH_REQUIRED_MESSAGE =
  "You need to sign in before running an analysis.";

export class ApiService {
  constructor(private readonly baseUrl = "") {}

  async analyzeTracks(
    trackA: File,
    trackB: File,
  ): Promise<UploadAnalysisResponse> {
    const formData = new FormData();
    formData.append("track_a", trackA);
    formData.append("track_b", trackB);

    try {
      const authorizationResponse = await fetch(
        `${this.baseUrl}${ANALYZE_AUTHORIZATION_ENDPOINT}`,
        { method: "POST" },
      );
      if (!authorizationResponse.ok) {
        if (authorizationResponse.status === 401) {
          throw new Error(AUTH_REQUIRED_MESSAGE);
        }
        const payload = (await authorizationResponse.json().catch(() => null)) as
          | { detail?: string }
          | null;
        throw new Error(payload?.detail ?? FRIENDLY_ERROR_MESSAGE);
      }

      const authorization = (await authorizationResponse.json()) as {
        uploadUrl: string;
        headers: Record<string, string>;
      };
      const response = await fetch(authorization.uploadUrl, {
        method: "POST",
        headers: authorization.headers,
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error(AUTH_REQUIRED_MESSAGE);
        }

        const payload = (await response.json().catch(() => null)) as
          | { detail?: string }
          | null;
        throw new Error(payload?.detail ?? FRIENDLY_ERROR_MESSAGE);
      }

      return (await response.json()) as UploadAnalysisResponse;
    } catch (error) {
      throw error instanceof Error ? error : new Error(FRIENDLY_ERROR_MESSAGE);
    }
  }
}

export const apiService = new ApiService();
