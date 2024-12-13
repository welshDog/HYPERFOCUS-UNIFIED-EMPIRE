import { Sidebar } from "@/components/Sidebar";

export default function Train() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Brain Training</h1>
        <div className="grid gap-6">
          {/* Brain training games section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Focus Games</h2>
            {/* Games grid will go here */}
          </section>
          
          {/* Focus timer section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Focus Timer</h2>
            {/* Focus timer component will go here */}
          </section>
        </div>
      </main>
    </div>
  );
}