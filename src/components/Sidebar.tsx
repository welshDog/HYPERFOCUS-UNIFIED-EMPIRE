import { Link, useLocation } from "react-router-dom";
import { Brain, Home, BarChart2, User, Users, Dumbbell } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";

export function Sidebar() {
  const location = useLocation();
  const [isHovered, setIsHovered] = useState(false);
  
  useEffect(() => {
    const container = document.querySelector('.content-container');
    if (container) {
      container.classList.toggle('sidebar-expanded', isHovered);
    }
  }, [isHovered]);
  
  const navigation = [
    { name: "Home", href: "/", icon: Home },
    { name: "Analytics", href: "/analytics", icon: BarChart2 },
    { name: "Train", href: "/train", icon: Dumbbell },
    { name: "Learn", href: "/learn", icon: Brain },
    { name: "Social", href: "/social", icon: Users },
    { name: "Profile", href: "/profile", icon: User },
  ];

  return (
    <div 
      className={cn(
        "fixed left-0 top-0 h-full z-50 flex flex-col transition-all duration-300 ease-in-out bg-white",
        isHovered ? "w-64" : "w-20"
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="flex grow flex-col gap-y-5 overflow-y-auto px-6 pb-4 border-r h-full">
        <div className="flex h-16 shrink-0 items-center">
          <Link to="/" className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-primary" />
            <span className={cn(
              "text-xl font-display font-bold gradient-text transition-opacity duration-200",
              isHovered ? "opacity-100" : "opacity-0"
            )}>
              HyperFocus
            </span>
          </Link>
        </div>
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <li key={item.name}>
                      <Link
                        to={item.href}
                        className={cn(
                          "group flex gap-x-3 rounded-md p-2 text-sm leading-6",
                          isActive
                            ? "bg-primary/10 text-primary font-semibold"
                            : "text-muted-foreground hover:bg-accent hover:text-foreground"
                        )}
                        title={item.name}
                      >
                        <item.icon
                          className={cn(
                            "h-6 w-6 shrink-0",
                            isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
                          )}
                          aria-hidden="true"
                        />
                        <span className={cn(
                          "transition-opacity duration-200",
                          isHovered ? "opacity-100" : "opacity-0"
                        )}>
                          {item.name}
                        </span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}