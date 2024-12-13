import { useState } from "react";
import { Brain, GraduationCap, Home, Trophy, Users, LogOut, Settings, LineChart } from "lucide-react";
import { cn } from "@/lib/utils";
import { supabase } from "@/integrations/supabase/client";
import { useNavigate, useLocation } from "react-router-dom";
import { toast } from "sonner";

const menuItems = [
  { icon: Home, label: "Home", href: "/" },
  { icon: GraduationCap, label: "Learn", href: "/learn" },
  { icon: Brain, label: "Train", href: "/train" },
  { icon: Users, label: "Community", href: "/social" },
  { icon: Trophy, label: "Profile", href: "/profile" },
  { icon: Settings, label: "Settings", href: "/settings" },
  { icon: LineChart, label: "Analytics", href: "/analytics" },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await supabase.auth.signOut();
      toast.success("Logged out successfully");
      navigate("/auth");
    } catch (error) {
      console.error("Error logging out:", error);
      toast.error("Error logging out");
    }
  };

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
                  className={cn(
                    "flex items-center p-2 text-gray-700 rounded-lg transition-colors",
                    location.pathname === item.href
                      ? "bg-primary text-white"
                      : "hover:bg-primary hover:text-white"
                  )}
                >
                  <item.icon className="w-6 h-6" />
                  {!collapsed && <span className="ml-3">{item.label}</span>}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <button
            onClick={handleLogout}
            className="flex items-center w-full p-2 text-gray-700 rounded-lg hover:bg-primary hover:text-white transition-colors"
          >
            <LogOut className="w-6 h-6" />
            {!collapsed && <span className="ml-3">Logout</span>}
          </button>
        </div>

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