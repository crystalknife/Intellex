import {
  Compass,
  FileText,
  Layers,
  Newspaper,
  Search,
  Settings,
  Sparkles,
  Wifi,
} from "lucide-react";

import { ROUTES } from "@/lib/constants";

export interface NavigationItem {
  name: string;
  href: string;
  icon: React.ElementType;
  disabled?: boolean;
}

export interface NavigationSection {
  label: string;
  items: NavigationItem[];
}

export const navigationSections: NavigationSection[] = [
  {
    label: "Workspace",
    items: [
      { name: "Intelligence", href: ROUTES.intelligence, icon: Sparkles },
      { name: "Events", href: ROUTES.events, icon: Newspaper },
      { name: "Documents", href: ROUTES.documents, icon: FileText },
      { name: "Search", href: ROUTES.search, icon: Search },
    ],
  },
  {
    label: "Analysis",
    items: [
      { name: "AI Workspace", href: ROUTES.aiWorkspace, icon: Compass, disabled: true },
      { name: "Sources", href: ROUTES.sources, icon: Wifi },
      { name: "Collections", href: ROUTES.collections, icon: Layers, disabled: true },
    ],
  },
  {
    label: "System",
    items: [
      { name: "Settings", href: ROUTES.settings, icon: Settings },
    ],
  },
];
