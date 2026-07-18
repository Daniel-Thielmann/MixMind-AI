export type PlanTier = "FREE" | "PRO" | "ENTERPRISE";

export interface AuthUser {
  id: string;
  name: string;
  email: string;
  image?: string | null;
  plan: PlanTier;
  aiCreditsUsed: number;
  aiCreditsLimit: number;
}

export interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  isAuthenticated: boolean;
}
