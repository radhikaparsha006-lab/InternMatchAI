"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { RoadmapResponse, RoadmapItem } from "@/lib/types";
import {
  ArrowLeft,
  CheckCircle,
  Clock,
  BookOpen,
  Code2,
  ExternalLink,
  Sparkles,
  TrendingUp,
  MessageSquare,
  ShieldCheck,
  FolderGit2,
} from "lucide-react";

export default function RoadmapPage() {
  const params = useParams();
  const id = params?.id as string;

  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [closedLoopToast, setClosedLoopToast] = useState<{
    skill: string;
    newIri?: number;
  } | null>(null);

  useEffect(() => {
    if (id) {
      loadRoadmap();
    }
  }, [id]);

  async function loadRoadmap() {
    try {
      setLoading(true);
      setError(null);
      const res = await api.getRoadmap(DEMO_STUDENT_ID, id);
      setRoadmap(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load preparation roadmap");
    } finally {
      setLoading(false);
    }
  }

  async function handleToggleItem(item: RoadmapItem) {
    if (!roadmap) return;
    const newCompleted = !item.is_completed;

    try {
      // Optimistic update
      setRoadmap({
        ...roadmap,
        items: roadmap.items.map((it) =>
          it.id === item.id ? { ...it, is_completed: newCompleted } : it
        ),
      });

      const res = await api.toggleRoadmapItem(
        DEMO_STUDENT_ID,
        id,
        item.id,
        newCompleted
      );

      // Update progress from server response
      setRoadmap((prev) =>
        prev ? { ...prev, overall_progress: res.overall_progress } : null
      );

      if (newCompleted && res.closed_loop_update) {
        setClosedLoopToast({
          skill: item.skill_name,
          newIri: res.closed_loop_update.new_iri,
        });
        setTimeout(() => setClosedLoopToast(null), 5000);
      }
    } catch (err) {
      console.error(err);
      // Reload on failure
      loadRoadmap();
    }
  }

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-28 bg-slate-200 rounded-2xl w-full"></div>
        <div className="space-y-4">
          <div className="h-40 bg-slate-200 rounded-xl"></div>
          <div className="h-40 bg-slate-200 rounded-xl"></div>
        </div>
      </div>
    );
  }

  if (error || !roadmap) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center text-red-700">
        <p className="font-semibold">{error || "Failed to load roadmap"}</p>
        <Link
          href={`/internships/${id}`}
          className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-red-700 hover:underline"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Opportunity</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Toast Notification for Closed-Loop Feedback */}
      {closedLoopToast && (
        <div className="fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-5 py-4 rounded-xl shadow-2xl border border-indigo-500/40 flex items-center gap-4 animate-in slide-in-from-bottom-5">
          <div className="w-9 h-9 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs font-bold text-white">Closed-Loop Skill Verified!</p>
            <p className="text-xs text-slate-300">
              Mastered <strong>{closedLoopToast.skill}</strong>. Added to your verified profile competencies.
              {closedLoopToast.newIri && (
                <span className="block text-emerald-400 font-semibold mt-0.5">
                  Internship Readiness Index elevated to {closedLoopToast.newIri}/100!
                </span>
              )}
            </p>
          </div>
          <button
            onClick={() => setClosedLoopToast(null)}
            className="text-slate-400 hover:text-white text-xs font-bold ml-2"
          >
            ✕
          </button>
        </div>
      )}

      {/* Back button */}
      <div>
        <Link
          href={`/internships/${id}`}
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-indigo-600 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Opportunity Details</span>
        </Link>
      </div>

      {/* Header Banner & Overall Progress */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded">
                Personalized Preparation Roadmap
              </span>
              <span className="text-xs text-slate-500">• {roadmap.role_category} Role</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-black text-slate-900">{roadmap.internship_title}</h1>
            <p className="text-sm font-medium text-slate-500 mt-1">{roadmap.company}</p>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href={`/interview/${id}`}
              className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2"
            >
              <MessageSquare className="w-4 h-4 text-emerald-400" />
              <span>Simulate Interview</span>
            </Link>
          </div>
        </div>

        {/* Progress Bar & Estimated Time */}
        <div className="bg-slate-50 p-5 rounded-xl border border-slate-200 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="w-full md:w-2/3 space-y-2">
            <div className="flex justify-between text-xs font-bold text-slate-700">
              <span className="flex items-center gap-1.5">
                <TrendingUp className="w-4 h-4 text-indigo-600" />
                <span>Roadmap Completion Progress</span>
              </span>
              <span className="text-indigo-600">{roadmap.overall_progress}%</span>
            </div>
            <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-full transition-all duration-500"
                style={{ width: `${roadmap.overall_progress}%` }}
              />
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0 text-xs text-slate-600 border-l-0 md:border-l border-slate-200 pl-0 md:pl-6 w-full md:w-auto">
            <Clock className="w-4 h-4 text-slate-400" />
            <div>
              <span className="text-slate-400 block font-medium">Estimated Preparation Effort</span>
              <span className="text-slate-900 font-bold text-sm">~{roadmap.total_estimated_hours} Hours</span>
            </div>
          </div>
        </div>
      </div>

      {/* Sequential Prerequisite Milestones */}
      <div className="space-y-4">
        <div className="flex items-center justify-between px-1">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-indigo-600" />
            <span>Prerequisite-Ordered Action Milestones</span>
          </h2>
          <span className="text-xs text-slate-500">
            Check off items as you learn to update your readiness in real time
          </span>
        </div>

        <div className="space-y-4">
          {roadmap.items.map((item, idx) => (
            <div
              key={item.id}
              className={`rounded-2xl border p-6 transition-all ${
                item.is_completed
                  ? "bg-emerald-50/40 border-emerald-200"
                  : "bg-white border-slate-200 shadow-sm hover:border-slate-300"
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Interactive Checkbox */}
                <button
                  onClick={() => handleToggleItem(item)}
                  className={`mt-1 w-6 h-6 rounded-lg flex items-center justify-center shrink-0 border transition ${
                    item.is_completed
                      ? "bg-emerald-600 border-emerald-600 text-white shadow-sm"
                      : "border-slate-300 hover:border-indigo-600 bg-white"
                  }`}
                  title={item.is_completed ? "Mark incomplete" : "Mark milestone complete"}
                >
                  {item.is_completed && <CheckCircle className="w-4 h-4" />}
                </button>

                <div className="flex-1 space-y-4 min-w-0">
                  {/* Milestone Title & Priority */}
                  <div>
                    <div className="flex flex-wrap items-center gap-2 mb-1">
                      <span className="text-[10px] font-black text-slate-400">STEP {idx + 1}</span>
                      <span
                        className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                          item.priority === "critical"
                            ? "bg-rose-100 text-rose-700 border border-rose-200"
                            : item.priority === "important"
                            ? "bg-amber-100 text-amber-700 border border-amber-200"
                            : "bg-slate-100 text-slate-600 border border-slate-200"
                        }`}
                      >
                        {item.priority}
                      </span>
                      <span className="text-xs text-slate-400">• {item.estimated_hours}h estimated</span>
                    </div>
                    <h3
                      className={`text-base font-bold ${
                        item.is_completed ? "text-slate-600 line-through" : "text-slate-900"
                      }`}
                    >
                      {item.title}
                    </h3>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      {item.learning_objectives}
                    </p>
                  </div>

                  {/* Practice Exercise */}
                  <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs text-slate-700 flex items-start gap-2">
                    <Code2 className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold text-slate-800">Hands-on Practice: </span>
                      <span>{item.practice_exercise}</span>
                    </div>
                  </div>

                  {/* Trusted Learning Resources with Verified Links */}
                  {item.trusted_resources.length > 0 && (
                    <div className="space-y-1.5 pt-1">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">
                        Trusted Official Guides & Exercises
                      </span>
                      <div className="flex flex-wrap gap-2">
                        {item.trusted_resources.map((res, rIdx) => (
                          <a
                            key={rIdx}
                            href={res.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-50/70 hover:bg-indigo-100 text-indigo-700 text-xs font-semibold border border-indigo-200/60 transition"
                          >
                            <span>{res.title}</span>
                            <span className="text-[10px] text-indigo-500 font-normal">({res.platform})</span>
                            <ExternalLink className="w-3 h-3 text-indigo-500" />
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommended Portfolio Project Card */}
      {roadmap.recommended_project && (
        <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl p-8 shadow-xl space-y-5">
          <div className="flex items-center gap-2 text-indigo-300">
            <FolderGit2 className="w-5 h-5" />
            <span className="text-xs font-bold uppercase tracking-wider">
              Recommended Portfolio Proof-of-Work
            </span>
          </div>

          <div>
            <h3 className="text-xl font-bold">{roadmap.recommended_project.title}</h3>
            <p className="text-xs text-slate-300 mt-2 leading-relaxed">
              {roadmap.recommended_project.description}
            </p>
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-800">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">
              Suggested Deliverables & Portfolio Artifacts:
            </span>
            <ul className="space-y-1.5 text-xs text-slate-300">
              {roadmap.recommended_project.deliverables.map((d, dIdx) => (
                <li key={dIdx} className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  <span>{d}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
