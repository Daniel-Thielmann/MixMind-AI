import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { Pool } from "pg";
import { db } from "@/lib/db";
import * as schema from "@/db/schema";

const databaseUrl = process.env.DATABASE_URL?.trim();

const database = databaseUrl
  ? new Pool({
      connectionString: databaseUrl,
      ssl:
        process.env.NODE_ENV === "production"
          ? { rejectUnauthorized: false }
          : undefined,
      max: 5,
    })
  : drizzleAdapter(db, {
      provider: "sqlite",
      schema: {
        user: schema.user,
        session: schema.session,
        account: schema.account,
        verification: schema.verification,
      },
    });

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL ?? "http://127.0.0.1:3000",
  secret: process.env.BETTER_AUTH_SECRET,
  trustedOrigins: [
    "http://127.0.0.1:3000",
    "https://*.mixmind.app",
    process.env.BETTER_AUTH_URL,
  ].filter(Boolean) as string[],
  database,
  user: {
    additionalFields: {
      plan: {
        type: "string",
        required: false,
        defaultValue: "FREE",
        input: false,
      },
      aiCreditsUsed: {
        type: "number",
        required: false,
        defaultValue: 0,
        input: false,
      },
      aiCreditsLimit: {
        type: "number",
        required: false,
        defaultValue: 500,
        input: false,
      },
    },
  },
  socialProviders: {
    ...(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
      ? { google: { clientId: process.env.GOOGLE_CLIENT_ID, clientSecret: process.env.GOOGLE_CLIENT_SECRET } }
      : {}),
    ...(process.env.GITHUB_CLIENT_ID && process.env.GITHUB_CLIENT_SECRET
      ? { github: { clientId: process.env.GITHUB_CLIENT_ID, clientSecret: process.env.GITHUB_CLIENT_SECRET } }
      : {}),
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7,
    updateAge: 60 * 60 * 24,
  },
});
