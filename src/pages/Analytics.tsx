import { Sidebar } from "@/components/Sidebar";
import AnalyticsDashboard from "@/components/analytics/AnalyticsDashboard";

export default function Analytics() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Analytics & Insights</h1>
        <AnalyticsDashboard />
      </main>
    </div>
  );
}