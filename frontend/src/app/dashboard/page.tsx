import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DashboardContent } from "./content";

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}
