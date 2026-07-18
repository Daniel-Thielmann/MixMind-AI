"use client";

import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { BarChart3, Music, TrendingUp, Clock, ArrowUp, Activity } from "lucide-react";

const stats = [
  { label: "Analyses", value: "12", icon: BarChart3, change: "+3 this week" },
  { label: "Tracks", value: "24", icon: Music, change: "+5 this week" },
  { label: "Compatibility Score", value: "87%", icon: TrendingUp, change: "+2% avg" },
  { label: "Time Saved", value: "3.2h", icon: Clock, change: "This session" },
];

const recentAnalyses = [
  { name: "Starlight.mp3", bpm: "128", key: "8A", energy: "87%", date: "2h ago" },
  { name: "Deep House Session.wav", bpm: "124", key: "6A", energy: "72%", date: "5h ago" },
  { name: "Tech Set.mp3", bpm: "130", key: "10B", energy: "91%", date: "1d ago" },
];

export function DashboardContent() {
  const { user } = useAuth();

  return (
    <div className="flex-1 pt-24 pb-12">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
        >
          <h1 className="text-3xl font-bold tracking-tight text-text">
            Welcome back, {user?.name?.split(" ")[0] ?? "DJ"}
          </h1>
          <p className="mt-1 text-text-secondary">
            Here&apos;s your analysis overview.
          </p>
        </motion.div>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * i, duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
              className="group rounded-xl border border-border/50 bg-card/50 p-5 backdrop-blur-sm transition-all duration-300 hover:border-border-light hover:bg-card-hover hover:shadow-lg hover:shadow-primary/5"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">{stat.label}</span>
                <stat.icon className="h-4 w-4 text-text-tertiary group-hover:text-primary transition-colors" />
              </div>
              <p className="mt-2 text-2xl font-semibold tracking-tight text-text">{stat.value}</p>
              <div className="mt-1 flex items-center gap-1 text-xs text-success">
                <ArrowUp className="h-3 w-3" />
                {stat.change}
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.4 }}
            className="rounded-xl border border-border/50 bg-card/50 p-6 backdrop-blur-sm"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-text">Recent Analyses</h2>
              <Activity className="h-4 w-4 text-text-tertiary" />
            </div>
            <div className="mt-4 space-y-3">
              {recentAnalyses.map((track) => (
                <div
                  key={track.name}
                  className="flex items-center justify-between rounded-lg border border-border/30 bg-background/50 px-4 py-3 transition-colors hover:bg-card"
                >
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-text">{track.name}</span>
                    <span className="text-xs text-text-tertiary">{track.date}</span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-text-secondary">
                    <span>{track.bpm} BPM</span>
                    <span className="text-primary">{track.key}</span>
                    <span>{track.energy}</span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.4 }}
            className="rounded-xl border border-border/50 bg-card/50 p-6 backdrop-blur-sm"
          >
            <h2 className="text-lg font-semibold text-text">AI Credits</h2>
            <div className="mt-4 space-y-4">
              <div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-text-secondary">Used this period</span>
                  <span className="text-text font-medium">
                    {user?.aiCreditsUsed ?? 0} / {user?.aiCreditsLimit ?? 500}
                  </span>
                </div>
                <div className="mt-2 h-2 overflow-hidden rounded-full bg-card">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{
                      width: `${Math.min(((user?.aiCreditsUsed ?? 0) / (user?.aiCreditsLimit ?? 500)) * 100, 100)}%`,
                    }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="h-full rounded-full bg-gradient-to-r from-primary to-accent-blue"
                  />
                </div>
              </div>
              <p className="text-xs text-text-tertiary">
                Credits reset monthly. Upgrade to PRO for more.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
