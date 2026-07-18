import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import { DashboardContent } from "./content";

export default async function DashboardPage() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session?.user) redirect("/");
  return <DashboardContent />;
}
