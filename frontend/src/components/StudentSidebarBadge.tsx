"use client";

import { useEffect, useState } from "react";
import { ShieldCheck } from "lucide-react";
import { api, DEMO_STUDENT_ID } from "@/lib/api";

function getInitials(name: string): string {
  if (!name) return "ST";
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "ST";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

export default function StudentSidebarBadge() {
  const [studentName, setStudentName] = useState<string>("Alex Chen");
  const [headline, setHeadline] = useState<string>("CS Junior • Class of '26");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 1. Initial fetch from API / DB
    async function loadInitialProfile() {
      try {
        const student = await api.getProfile(DEMO_STUDENT_ID);
        if (student?.full_name) {
          setStudentName(student.full_name);
        }
        if (student?.profile?.headline) {
          setHeadline(student.profile.headline);
        } else if (student?.profile?.education_major) {
          setHeadline(`${student.profile.education_major} • Class of '26`);
        }
      } catch (err) {
        console.error("Failed to load student for sidebar badge:", err);
      } finally {
        setLoading(false);
      }
    }

    loadInitialProfile();

    // 2. Event listener for real-time immediate updates across the entire SPA
    function handleProfileUpdated(event: Event) {
      const customEvent = event as CustomEvent<{ full_name?: string; headline?: string }>;
      if (customEvent.detail?.full_name) {
        setStudentName(customEvent.detail.full_name);
      }
      if (customEvent.detail?.headline) {
        setHeadline(customEvent.detail.headline);
      }
    }

    window.addEventListener("student-profile-updated", handleProfileUpdated);
    return () => {
      window.removeEventListener("student-profile-updated", handleProfileUpdated);
    };
  }, []);

  const initials = getInitials(studentName);

  return (
    <div className="p-4 border-t border-slate-800 bg-slate-950/40">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-sm shadow transition-all duration-300">
          {initials}
        </div>
        <div className="flex-1 min-w-0">
          <p
            id="sidebar-student-name"
            className="text-sm font-medium text-white truncate transition-all duration-300"
            title={studentName}
          >
            {studentName}
          </p>
          <p className="text-xs text-slate-400 truncate" title={headline}>
            {headline}
          </p>
        </div>
      </div>
      <div className="mt-3 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 px-2 py-1 rounded">
        <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
        <span>Ready for Backend Roles</span>
      </div>
    </div>
  );
}
