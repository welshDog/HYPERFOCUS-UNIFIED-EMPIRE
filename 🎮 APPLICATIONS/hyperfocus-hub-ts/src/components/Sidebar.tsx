import { useState } from "react";
import { Link } from "react-router-dom";
import { Brain } from "lucide-react";
import { cn } from "@/lib/utils";
import { navigationItems } from "./navigation-items";

export const Sidebar = () => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div 
      className={cn(
        "fixed left-0 top-0 h-screen z-40 flex flex-col transition-all duration-300 ease-in-out bg-white dark:bg-gray-900 border-r dark:border-gray-800",
        isHovered ? "w-64" : "w-20"
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex flex-col flex-1 p-4">
        <div className="flex items-center mb-8">
          <Link to="/" className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-primary" />
            <span 
              className={cn(
                "font-semibold text-xl transition-all duration-300",
                isHovered ? "opacity-100 ml-2" : "opacity-0 w-0 overflow-hidden"
              )}
            >
              HyperStudy
            </span>
          </Link>
        </div>

        <nav className="flex-1">
          <ul className="space-y-2">
            {navigationItems.map((item) => (
              <li key={item.href}>
                <Link
                  to={item.href}
                  className={cn(
                    "flex items-center px-2 py-2 rounded-lg transition-colors",
                    "hover:bg-gray-100 dark:hover:bg-gray-800",
                    "text-gray-700 dark:text-gray-200"
                  )}
                >
                  <item.icon className="h-5 w-5" />
                  <span
                    className={cn(
                      "ml-3 transition-all duration-300",
                      isHovered ? "opacity-100" : "opacity-0 w-0 overflow-hidden"
                    )}
                  >
                    {item.name}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </div>
  );
};