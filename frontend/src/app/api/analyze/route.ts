import { createHmac } from "node:crypto";
import { headers } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const session = await auth.api.getSession({ headers: await headers() });
  const userId = session?.user?.id ?? "anonymous";
  const secret = process.env.INTERNAL_AUTH_SECRET ?? "";
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const signature = secret
    ? createHmac("sha256", secret).update(`${userId}:${timestamp}`).digest("hex")
    : "";
  const apiUrl = (process.env.BACKEND_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").replace(/\/$/, "");
  const formData = await request.formData();
  const response = await fetch(`${apiUrl}/api/v1/analysis/analyze`, {
    method: "POST",
    headers: secret
      ? {
          "X-MixMind-User": userId,
          "X-MixMind-Timestamp": timestamp,
          "X-MixMind-Signature": signature,
        }
      : undefined,
    body: formData,
  });
  const body = await response.json().catch(() => ({ detail: "Invalid backend response" }));
  return NextResponse.json(body, { status: response.status });
}
