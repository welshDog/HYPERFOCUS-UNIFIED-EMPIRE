import { useState } from "react";
import { Brain, GraduationCap, Home, Trophy, Users } from "lucide-react";
import { cn } from "@/lib/utils";

const menuItems = [
  { icon: Home, label: "Home", href: "/" },
  { icon: Brain, label: "Brain Training", href: "/brain-training" },
  { icon: GraduationCap, label: "Courses", href: "/courses" },
  { icon: Users, label: "Community", href: "/community" },
  { icon: Trophy, label: "Achievements", href: "/achievements" },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className={cn(
        "h-screen bg-white border-r border-gray-200 transition-all duration-300",
        collapsed ? "w-20" : "w-64"
      )}
    >
      <div className="flex flex-col h-full">
        <div className="p-4 border-b border-gray-200">
          <h1 className={cn("font-bold text-primary", collapsed ? "text-sm" : "text-xl")}>
            {collapsed ? "HS" : "Hyperfocus Studios"}
          </h1>
        </div>
        
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => (
              <li key={item.label}>
                <a
                  href={item.href}
                  className="flex items-center p-2 text-gray-700 rounded-lg hover:bg-primary hover:text-white transition-colors"
                >
                  <item.icon className="w-6 h-6" />
                  {!collapsed && <span className="ml-3">{item.label}</span>}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-4 text-gray-500 hover:text-primary transition-colors"
        >
          {collapsed ? "→" : "←"}
        </button>
      </div>
    </div>
  );
}