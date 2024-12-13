import { Sidebar } from "@/components/Sidebar";

export default function Profile() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Your Profile</h1>
        <div className="grid gap-6">
          {/* Profile stats section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Your Progress</h2>
            {/* Progress stats will go here */}
          </section>
          
          {/* Achievements section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Achievements</h2>
            {/* Achievements grid will go here */}
          </section>
        </div>
      </main>
    </div>
  );
}