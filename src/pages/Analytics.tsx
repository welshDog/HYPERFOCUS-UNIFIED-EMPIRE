import { Sidebar } from "@/components/Sidebar";

export default function Analytics() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Analytics & Insights</h1>
        <div className="grid gap-6">
          {/* Weekly progress section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Weekly Progress</h2>
            {/* Progress charts will go here */}
          </section>
          
          {/* Focus insights section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Focus Insights</h2>
            {/* Focus insights will go here */}
          </section>
        </div>
      </main>
    </div>
  );
}