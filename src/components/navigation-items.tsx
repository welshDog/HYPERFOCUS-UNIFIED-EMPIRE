import { Home, Brain, BookOpen, Users, User, Settings, LineChart } from "lucide-react";

export const navigationItems = [
  {
    name: "Home",
    path: "/",
    href: "/",
    icon: Home,
  },
  {
    name: "Learn",
    path: "/learn",
    href: "/learn",
    icon: BookOpen,
  },
  {
    name: "Train",
    path: "/train",
    href: "/train",
    icon: Brain,
  },
  {
    name: "Social",
    path: "/social",
    href: "/social",
    icon: Users,
  },
  {
    name: "Profile",
    path: "/profile",
    href: "/profile",
    icon: User,
  },
  {
    name: "Analytics",
    path: "/analytics",
    href: "/analytics",
    icon: LineChart,
  },
  {
    name: "Settings",
    path: "/settings",
    href: "/settings",
    icon: Settings,
  },
];