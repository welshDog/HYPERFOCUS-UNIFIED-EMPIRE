import { cn } from "@/lib/utils";
import { Brain } from "lucide-react";
import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { navigationItems } from "./navigation-items";

export const Sidebar = () => {
  const [isHovered, setIsHovered] = useState(false);
  const location = useLocation();

  return (
    <div 
      className={cn(
        "fixed left-0 top-0 h-full z-40 flex flex-col transition-all duration-300 ease-in-out bg-white border-r shadow-sm",
        isHovered ? "w-64" : "w-20"
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="flex grow flex-col gap-y-5 overflow-y-auto px-6 pb-4 h-full">
        <div className="flex h-16 shrink-0 items-center">
          <Link to="/" className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-primary" />
            <span className={cn("font-semibold text-xl transition-opacity", 
              isHovered ? "opacity-100" : "opacity-0 w-0"
            )}>
              HyperStudy
            </span>
          </Link>
        </div>
        
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigationItems.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={cn(
                        location.pathname === item.href
                          ? "bg-gray-50 text-primary"
                          : "text-gray-700 hover:text-primary hover:bg-gray-50",
                        "group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-all duration-300"
                      )}
                    >
                      <item.icon className="h-6 w-6 shrink-0" aria-hidden="true" />
                      <span className={cn("transition-opacity", 
                        isHovered ? "opacity-100" : "opacity-0 w-0"
                      )}>
                        {item.name}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};