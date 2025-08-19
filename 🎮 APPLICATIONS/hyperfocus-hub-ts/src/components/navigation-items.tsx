import { Home, Brain, BookOpen, Users, User, Settings, LineChart } from "lucide-react";
import { LucideIcon } from "lucide-react";

export interface NavigationItem {
  name: string;
  href: string;
  icon: LucideIcon;
}

export const navigationItems: NavigationItem[] = [
  {
    name: "Home",
    href: "/",
    icon: Home,
  },
  {
    name: "Learn",
    href: "/learn",
    icon: BookOpen,
  },
  {
    name: "Train",
    href: "/train",
    icon: Brain,
  },
  {
    name: "Social",
    href: "/social",
    icon: Users,
  },
  {
    name: "Profile",
    href: "/profile",
    icon: User,
  },
  {
    name: "Analytics",
    href: "/analytics",
    icon: LineChart,
  },
  {
    name: "Settings",
    href: "/settings",
    icon: Settings,
  },
];