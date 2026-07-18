import { createClient } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import * as schema from "@/db/schema";

const client = createClient({
  url: "file:./data/mixmind.db",
});

export const db = drizzle(client, { schema });
export type DbClient = typeof db;
