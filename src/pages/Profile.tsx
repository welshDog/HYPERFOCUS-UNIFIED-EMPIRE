import { Sidebar } from "@/components/Sidebar";
import { ProfileCustomization } from "@/components/ProfileCustomization";

export default function Profile() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <ProfileCustomization />
      </main>
    </div>
  );
}