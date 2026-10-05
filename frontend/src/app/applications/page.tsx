"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { ApplicationItem } from "@/lib/types";
import {
  CheckCircle2,
  Clock,
  ArrowRight,
  BookOpen,
  Filter,
  FileText,
  AlertCircle,
  Plus,
} from "lucide-react";

export default function ApplicationsPage() {
  const [applications, setApplications] = useState<ApplicationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedFilter, setSelectedFilter] = useState<string>("All");
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  useEffect(() => {
    loadApplications();
  }, []);

  async function loadApplications() {
    try {
      setLoading(true);
      const res = await api.getApplications(DEMO_STUDENT_ID);
      setApplications(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(app: ApplicationItem, newStatus: string) {
    try {
      setUpdatingId(app.internship_id);
      await api.upsertApplication(DEMO_STUDENT_ID, app.internship_id, newStatus, app.notes);
      setApplications((prev) =>
        prev.map((a) => (a.internship_id === app.internship_id ? { ...a, status: newStatus as any } : a))
      );
    } catch (err) {
      console.error(err);
    } finally {
      setUpdatingId(null);
    }
  }

  const statuses = [
    "All",
    "saved",
    "planning_to_apply",
    "applied",
    "assessment",
    "interview",
    "offer",
    "rejected",
  ];

  const filtered = applications.filter((a) => {
    if (selectedFilter === "All") return true;
    return a.status === selectedFilter;
  });

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">Application Tracker</h1>
          <p className="text-sm text-slate-500 mt-1">
            Track your internship opportunities across the complete application and interview lifecycle.
          </p>
        </div>

        <Link
          href="/recommendations"
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-sm transition self-start sm:self-auto"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Discover New Roles</span>
        </Link>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-bold text-slate-400 mr-2 uppercase tracking-wider flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" />
          Status:
        </span>
        {statuses.map((st) => (
          <button
            key={st}
            onClick={() => setSelectedFilter(st)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold capitalize transition ${
              selectedFilter === st
                ? "bg-indigo-600 text-white shadow-sm"
                : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
            }`}
          >
            {st.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Applications List */}
      {loading ? (
        <div className="p-8 text-center text-slate-500 animate-pulse">Loading tracked applications...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
          <FileText className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No applications in this category</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Browse recommendations and save roles or log applications to organize your preparation pipeline.
          </p>
          <div className="pt-2">
            <Link
              href="/recommendations"
              className="inline-flex items-center gap-1 text-xs font-bold text-indigo-600 hover:underline"
            >
              <span>Explore Recommendations Hub</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((app) => (
            <div
              key={app.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm hover:border-slate-300 transition flex flex-col md:flex-row md:items-center justify-between gap-6"
            >
              <div className="space-y-2 min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded">
                    {app.role_category}
                  </span>
                  <span className="text-xs text-slate-400">• {app.location} {app.is_remote ? "(Remote)" : ""}</span>
                  {app.deadline && (
                    <span className="text-xs text-slate-500 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      Deadline: {app.deadline}
                    </span>
                  )}
                </div>

                <h3 className="text-lg font-bold text-slate-900 leading-snug">
                  <Link href={`/internships/${app.internship_id}`} className="hover:text-indigo-600">
                    {app.title}
                  </Link>
                </h3>
                <p className="text-xs font-medium text-slate-500">{app.company}</p>

                {app.notes && (
                  <p className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100 max-w-xl">
                    <span className="font-bold text-slate-700">Notes: </span>
                    {app.notes}
                  </p>
                )}
              </div>

              {/* Status Selector & Actions */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 shrink-0">
                <select
                  value={app.status}
                  disabled={updatingId === app.internship_id}
                  onChange={(e) => handleStatusChange(app, e.target.value)}
                  className={`text-xs font-bold px-3 py-2 rounded-xl border focus:ring-2 focus:ring-indigo-500 focus:outline-none capitalize transition ${
                    app.status === "offer"
                      ? "bg-emerald-50 text-emerald-800 border-emerald-300"
                      : app.status === "interview"
                      ? "bg-sky-50 text-sky-800 border-sky-300"
                      : app.status === "applied"
                      ? "bg-indigo-50 text-indigo-800 border-indigo-300"
                      : "bg-slate-50 text-slate-700 border-slate-200"
                  }`}
                >
                  <option value="saved">Saved</option>
                  <option value="planning_to_apply">Planning to Apply</option>
                  <option value="applied">Applied</option>
                  <option value="assessment">Technical Assessment</option>
                  <option value="interview">Interviewing</option>
                  <option value="offer">Offer Received</option>
                  <option value="rejected">Rejected</option>
                  <option value="withdrawn">Withdrawn</option>
                </select>

                <Link
                  href={`/roadmap/${app.internship_id}`}
                  className="px-3 py-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 text-xs font-bold rounded-xl border border-indigo-200/60 transition flex items-center gap-1.5"
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>Preparation Roadmap</span>
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
