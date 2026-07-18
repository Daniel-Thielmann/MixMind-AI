"use client";

import { useCallback } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  BarChart3,
  History,
  Heart,
  Settings,
  CreditCard,
  Key,
  LogOut,
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { UserAvatar } from "./UserAvatar";
import { PlanBadge } from "./PlanBadge";

export function UserDropdown() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleNavigation = useCallback(
    (path: string) => {
      router.push(path);
    },
    [router]
  );

  if (!user) return null;

  const menuItems = [
    { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
    { label: "My Analyses", icon: BarChart3, path: "/dashboard/analyses" },
    { label: "History", icon: History, path: "/dashboard/history" },
    { label: "Favorites", icon: Heart, path: "/dashboard/favorites" },
  ];

  const bottomItems = [
    { label: "Settings", icon: Settings, path: "/dashboard/settings" },
    { label: "Billing", icon: CreditCard, path: "/dashboard/billing" },
    { label: "API Keys", icon: Key, path: "/dashboard/api-keys" },
  ];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50"
        >
          <UserAvatar name={user.name} image={user.image} />
        </motion.button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-60">
        <div className="px-3 py-3">
          <div className="flex items-center gap-3">
            <UserAvatar name={user.name} image={user.image} />
            <div className="flex flex-col gap-0.5">
              <p className="text-sm font-medium text-text leading-none">{user.name}</p>
              <p className="text-xs text-text-secondary truncate max-w-[10rem]">{user.email}</p>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-2">
            <PlanBadge plan={user.plan} />
            <span className="text-xs text-text-tertiary">
              {user.aiCreditsUsed} / {user.aiCreditsLimit} credits
            </span>
          </div>
        </div>

        <DropdownMenuSeparator />

        <DropdownMenuLabel>Navigation</DropdownMenuLabel>
        {menuItems.map((item) => (
          <DropdownMenuItem key={item.path} onClick={() => handleNavigation(item.path)}>
            <item.icon className="h-4 w-4" />
            {item.label}
          </DropdownMenuItem>
        ))}

        <DropdownMenuSeparator />

        {bottomItems.map((item) => (
          <DropdownMenuItem key={item.path} onClick={() => handleNavigation(item.path)}>
            <item.icon className="h-4 w-4" />
            {item.label}
          </DropdownMenuItem>
        ))}

        <DropdownMenuSeparator />

        <DropdownMenuItem
          onClick={() => logout()}
          className="text-danger hover:text-danger hover:bg-danger/10 focus-visible:text-danger focus-visible:bg-danger/10"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
