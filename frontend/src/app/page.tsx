"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { DashboardResponse } from "@/lib/types";
import {
  Sparkles,
  ArrowRight,
  TrendingUp,
  Target,
  BookOpen,
  MessageSquare,
  AlertCircle,
  Briefcase,
  CheckCircle,
  Layers,
} from "lucide-react";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      setLoading(true);
      setError(null);
      const res = await api.getDashboard(DEMO_STUDENT_ID);
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-28 bg-slate-200 rounded-2xl w-full"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="h-64 bg-slate-200 rounded-xl"></div>
          <div className="h-64 bg-slate-200 rounded-xl"></div>
          <div className="h-64 bg-slate-200 rounded-xl"></div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center text-red-700">
        <AlertCircle className="w-8 h-8 mx-auto mb-2 text-red-500" />
        <p className="font-semibold">{error || "Failed to load data"}</p>
        <button
          onClick={loadDashboard}
          className="mt-4 px-4 py-2 bg-red-600 text-white text-xs font-semibold rounded-lg hover:bg-red-700 transition"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  const { student, top_match, active_readiness, applications_pipeline, top_priority_gaps, recent_recommendations } = data;
  const iri = active_readiness?.overall_iri ?? 58.5;
  const targetInternId = top_match.internship_id || "intern_01";

  return (
    <div className="space-y-8">
      {/* Hero Welcome & Strategy Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-2xl p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-indigo-500/10 to-transparent pointer-events-none" />
        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-400/30 text-indigo-300 text-xs font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Closed-Loop Readiness System</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight">
            Welcome back, {student.full_name}!
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            InternMatch AI not only recommends target opportunities, but bridges your exact skill gaps
            through prerequisite learning roadmaps and adaptive mock interview evaluation.
          </p>
          <div className="pt-2 flex flex-wrap gap-4">
            <Link
              href={`/roadmap/${targetInternId}`}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg shadow-sm transition"
            >
              <BookOpen className="w-4 h-4" />
              <span>Resume Preparation Roadmap</span>
            </Link>
            <Link
              href={`/interview/${targetInternId}`}
              className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold rounded-lg border border-slate-700 transition"
            >
              <MessageSquare className="w-4 h-4 text-emerald-400" />
              <span>Take Adaptive Mock Interview</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Main Stats Cockpit: Top Match & Internship Readiness Index */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Recommendation Card */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-md">
                Top Recommendation
              </span>
              <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
                <TrendingUp className="w-3.5 h-3.5" />
                <span>{top_match.match_score}/100 Match</span>
              </div>
            </div>
            <h2 className="text-xl font-bold text-slate-900 leading-snug">{top_match.title}</h2>
            <p className="text-sm font-medium text-slate-500 mt-1">{top_match.company}</p>
            <p className="text-xs text-slate-600 mt-3 line-clamp-3 bg-slate-50 p-3 rounded-lg border border-slate-100">
              {top_match.explanation}
            </p>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
            <Link
              href={`/internships/${targetInternId}`}
              className="text-xs font-semibold text-slate-600 hover:text-slate-900"
            >
              Inspect Gap Analysis
            </Link>
            <Link
              href={`/roadmap/${targetInternId}`}
              className="inline-flex items-center gap-1 text-xs font-bold text-indigo-600 hover:text-indigo-700"
            >
              <span>View Prep Plan</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* Internship Readiness Index (IRI) Indicator */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Target Readiness
              </span>
              <span className="text-xs text-slate-400">Target Role</span>
            </div>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-4xl font-extrabold text-slate-900">{iri}</span>
              <span className="text-slate-400 text-sm font-medium">/ 100 IRI</span>
            </div>
            <p className="text-xs text-slate-500 mt-1 italic">
              Interpretable composite indicator, not a hiring probability.
            </p>

            {/* Component Progress Bars */}
            <div className="mt-5 space-y-2.5">
              <div>
                <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                  <span>Skill Coverage</span>
                  <span>{active_readiness?.components.skill_coverage ?? 50}%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-600 rounded-full transition-all"
                    style={{ width: `${active_readiness?.components.skill_coverage ?? 50}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                  <span>Roadmap Completed</span>
                  <span>{active_readiness?.components.roadmap_progress ?? 0}%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 rounded-full transition-all"
                    style={{ width: `${active_readiness?.components.roadmap_progress ?? 0}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-medium text-slate-600 mb-1">
                  <span>Mock Interview Score</span>
                  <span>{active_readiness?.components.interview_performance ?? 50}%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-sky-500 rounded-full transition-all"
                    style={{ width: `${active_readiness?.components.interview_performance ?? 50}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100">
            <Link
              href={`/roadmap/${targetInternId}`}
              className="w-full block text-center py-2 bg-slate-50 hover:bg-slate-100 text-xs font-semibold text-slate-700 rounded-lg transition"
            >
              Advance Readiness Score
            </Link>
          </div>
        </div>

        {/* Application Pipeline & Deadlines */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Application Pipeline
              </span>
              <Link href="/applications" className="text-xs font-semibold text-indigo-600 hover:underline">
                View All
              </Link>
            </div>

            <div className="grid grid-cols-2 gap-3 mt-2">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-xs text-slate-500 block">Saved</span>
                <span className="text-2xl font-bold text-slate-800">{applications_pipeline.saved}</span>
              </div>
              <div className="bg-indigo-50/50 p-3 rounded-lg border border-indigo-100/60">
                <span className="text-xs text-indigo-600 block">Applied</span>
                <span className="text-2xl font-bold text-indigo-700">{applications_pipeline.applied}</span>
              </div>
              <div className="bg-emerald-50/50 p-3 rounded-lg border border-emerald-100/60">
                <span className="text-xs text-emerald-600 block">Interviews</span>
                <span className="text-2xl font-bold text-emerald-700">{applications_pipeline.interview}</span>
              </div>
              <div className="bg-amber-50/50 p-3 rounded-lg border border-amber-100/60">
                <span className="text-xs text-amber-600 block">Offers</span>
                <span className="text-2xl font-bold text-amber-700">{applications_pipeline.offers}</span>
              </div>
            </div>

            <div className="mt-4 p-3 bg-slate-50 rounded-lg text-xs text-slate-600 border border-slate-100">
              <span className="font-semibold text-slate-700">Next Recommended Action:</span>
              <p className="mt-1">
                Complete the FastAPI milestone in your roadmap to close the critical skill gap for CloudScale Systems.
              </p>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100">
            <Link
              href="/applications"
              className="w-full block text-center py-2 bg-indigo-50 hover:bg-indigo-100 text-xs font-semibold text-indigo-700 rounded-lg transition"
            >
              Open Application Tracker
            </Link>
          </div>
        </div>
      </div>

      {/* Critical Competency Gaps & Recent Opportunities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Prioritized Competency Gaps */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Highest-Priority Skill Gaps</h3>
              <p className="text-xs text-slate-500">Skills preventing maximum readiness for top target roles</p>
            </div>
            <Target className="w-5 h-5 text-indigo-600" />
          </div>

          <div className="space-y-3 mt-4">
            {top_priority_gaps.map((gap, i) => (
              <div
                key={i}
                className="flex items-start justify-between p-3.5 rounded-lg border border-slate-100 hover:border-slate-200 bg-slate-50/50 transition"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-800">{gap.skill_name}</span>
                    <span
                      className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                        gap.priority === "critical"
                          ? "bg-rose-100 text-rose-700 border border-rose-200"
                          : "bg-amber-100 text-amber-700 border border-amber-200"
                      }`}
                    >
                      {gap.priority}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{gap.reason}</p>
                </div>
                <Link
                  href={`/roadmap/${targetInternId}`}
                  className="text-xs font-semibold text-indigo-600 hover:underline shrink-0 ml-3"
                >
                  Start Prep
                </Link>
              </div>
            ))}
          </div>
        </div>

        {/* Recommended Opportunities List */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Recommended Opportunities</h3>
              <p className="text-xs text-slate-500">Ranked by Hybrid Multi-Factor Recommendation Model</p>
            </div>
            <Link
              href="/recommendations"
              className="text-xs font-bold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
            >
              <span>Explore All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-3 mt-4">
            {recent_recommendations.map((rec) => (
              <div
                key={rec.id}
                className="flex items-center justify-between p-3.5 rounded-lg border border-slate-100 hover:border-slate-200 bg-slate-50/50 transition"
              >
                <div className="min-w-0 pr-3">
                  <Link
                    href={`/internships/${rec.id}`}
                    className="text-sm font-bold text-slate-900 hover:text-indigo-600 truncate block"
                  >
                    {rec.title}
                  </Link>
                  <p className="text-xs text-slate-500 truncate">
                    {rec.company} • {rec.location} {rec.is_remote ? "(Remote)" : ""}
                  </p>
                </div>
                <div className="flex items-center gap-3 shrink-0">
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2 py-1 rounded border border-emerald-200">
                    {rec.match_score}/100
                  </span>
                  <Link
                    href={`/internships/${rec.id}`}
                    className="p-1.5 rounded-md hover:bg-slate-200 text-slate-500 transition"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
