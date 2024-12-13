import { Sidebar } from "@/components/Sidebar";

export default function Settings() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Settings</h1>
        <div className="grid gap-6">
          {/* Accessibility settings section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Accessibility</h2>
            {/* Accessibility options will go here */}
          </section>
          
          {/* Preferences section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Preferences</h2>
            {/* Preferences options will go here */}
          </section>
        </div>
      </main>
    </div>
  );
}