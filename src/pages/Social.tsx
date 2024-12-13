import { Sidebar } from "@/components/Sidebar";

export default function Social() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Community</h1>
        <div className="grid gap-6">
          {/* Social feed section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Social Feed</h2>
            {/* Social feed will go here */}
          </section>
          
          {/* Discussion forums section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Discussion Forums</h2>
            {/* Forums list will go here */}
          </section>
        </div>
      </main>
    </div>
  );
}