import { ChevronRight } from "lucide-react";
import { LucideIcon } from "lucide-react";

interface SettingsItemProps {
  icon: LucideIcon;
  label: string;
  onClick?: () => void;
  iconColor?: string;
}

export function SettingsItem({ icon: Icon, label, onClick, iconColor = "text-gray-600" }: SettingsItemProps) {
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
    >
      <div className="flex items-center space-x-4">
        <div className={`rounded-full p-2 ${iconColor}`}>
          <Icon className="h-5 w-5" />
        </div>
        <span className="text-sm font-medium">{label}</span>
      </div>
      <ChevronRight className="h-5 w-5 text-gray-400" />
    </button>
  );
}