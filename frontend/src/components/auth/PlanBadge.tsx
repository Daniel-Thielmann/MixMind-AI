"use client";

import { Badge } from "@/components/ui/badge";
import type { PlanTier } from "@/types/auth";

interface PlanBadgeProps {
  plan: PlanTier;
}

const planConfig: Record<PlanTier, { label: string; variant: "free" | "pro" | "enterprise" }> = {
  FREE: { label: "FREE", variant: "free" },
  PRO: { label: "PRO", variant: "pro" },
  ENTERPRISE: { label: "ENTERPRISE", variant: "enterprise" },
};

export function PlanBadge({ plan }: PlanBadgeProps) {
  const config = planConfig[plan] ?? planConfig.FREE;
  return <Badge variant={config.variant}>{config.label}</Badge>;
}
