import { Sidebar } from "@/components/Sidebar";

export default function Learn() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-4xl font-bold mb-8">Learn</h1>
        <div className="grid gap-6">
          {/* Course dashboard will go here */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Your Courses</h2>
            {/* Course grid will go here */}
          </section>
          
          {/* Recommended courses section */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold">Recommended for You</h2>
            {/* Recommended courses grid will go here */}
          </section>
        </div>
      </main>
    </div>
  );
}