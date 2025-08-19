import { Sidebar } from "@/components/Sidebar";
import { SettingsHeader } from "@/components/settings/SettingsHeader";
import { SettingsList } from "@/components/settings/SettingsList";

export default function Settings() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-sm my-8">
          <SettingsHeader />
          <SettingsList />
        </div>
      </main>
    </div>
  );
}