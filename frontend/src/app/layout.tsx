import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";
import {
  Compass,
  UserCheck,
  Briefcase,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";
import StudentSidebarBadge from "@/components/StudentSidebarBadge";

export const metadata: Metadata = {
  title: "InternMatch AI – Personalized Internship Recommendation & Readiness",
  description:
    "Explainable, adaptive, end-to-end AI platform connecting internship recommendation, skill gap analysis, personalized roadmaps, and adaptive mock interviews.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-50 text-slate-900 flex min-h-screen">
        {/* Navigation Sidebar */}
        <aside className="w-64 bg-slate-900 text-slate-200 border-r border-slate-800 flex flex-col shrink-0">
          <div className="p-6 border-b border-slate-800">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h1 className="font-bold text-white text-base leading-tight">InternMatch AI</h1>
                <p className="text-xs text-slate-400">Readiness Engine</p>
              </div>
            </Link>
          </div>

          <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
            <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Navigation
            </div>

            <Link
              href="/"
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
            >
              <Compass className="w-4 h-4 text-indigo-400" />
              <span>Dashboard Cockpit</span>
            </Link>

            <Link
              href="/recommendations"
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
            >
              <Briefcase className="w-4 h-4 text-emerald-400" />
              <span>Recommendations Hub</span>
            </Link>

            <Link
              href="/profile"
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
            >
              <UserCheck className="w-4 h-4 text-sky-400" />
              <span>Profile & Resume</span>
            </Link>

            <Link
              href="/applications"
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
            >
              <CheckCircle2 className="w-4 h-4 text-amber-400" />
              <span>Application Tracker</span>
            </Link>
          </nav>

          {/* Student Status Profile Badge */}
          <StudentSidebarBadge />
        </aside>

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          {/* Top header */}
          <header className="h-16 bg-white border-b border-slate-200 px-8 flex items-center justify-between shrink-0 shadow-sm">
            <div className="flex items-center gap-3">
              <span className="text-xs uppercase tracking-wider font-semibold bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-full border border-indigo-200">
                Closed-Loop Personalization Active
              </span>
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-600">
              <span className="flex items-center gap-1.5 text-xs text-emerald-600 font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                FastAPI Backend Connected
              </span>
              <div className="h-4 w-px bg-slate-200"></div>
              <Link
                href="/recommendations"
                className="flex items-center gap-1.5 text-xs font-semibold text-indigo-600 hover:text-indigo-700"
              >
                <span>Explore Opportunities</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </header>

          <main className="flex-1 p-8 max-w-7xl w-full mx-auto">{children}</main>
        </div>
      </body>
    </html>
  );
}
