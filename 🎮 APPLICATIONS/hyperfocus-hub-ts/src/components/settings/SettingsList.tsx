import { 
  Lock, 
  Bell, 
  Users, 
  MessageSquare, 
  HelpCircle, 
  Mail,
  FileText,
  Settings as SettingsIcon
} from "lucide-react";
import { SettingsItem } from "./SettingsItem";

export function SettingsList() {
  const settingsItems = [
    { icon: Lock, label: "Change Password", color: "text-blue-600" },
    { icon: Bell, label: "Notifications", color: "text-orange-600" },
    { icon: Users, label: "Refer Friends & Business", color: "text-purple-600" },
    { icon: MessageSquare, label: "Third Party Applications", color: "text-green-600" },
    { icon: HelpCircle, label: "FAQ", color: "text-indigo-600" },
    { icon: Mail, label: "Contact us", color: "text-pink-600" },
    { icon: FileText, label: "Terms & Conditions", color: "text-gray-600" },
    { icon: SettingsIcon, label: "Settings", color: "text-gray-600" },
  ];

  return (
    <div className="divide-y">
      {settingsItems.map((item, index) => (
        <SettingsItem
          key={index}
          icon={item.icon}
          label={item.label}
          iconColor={item.color}
          onClick={() => console.log(`Clicked ${item.label}`)}
        />
      ))}
    </div>
  );
}