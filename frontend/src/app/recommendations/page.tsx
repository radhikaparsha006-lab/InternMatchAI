"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { RecommendationResponse, RecommendationItem } from "@/lib/types";
import {
  Sparkles,
  Filter,
  CheckCircle,
  HelpCircle,
  ArrowRight,
  Bookmark,
  MapPin,
  Clock,
  DollarSign,
  Info,
  ChevronDown,
} from "lucide-react";

export default function RecommendationsPage() {
  const [model, setModel] = useState<"hybrid" | "baseline_tfidf" | "semantic_dense">("hybrid");
  const [selectedRole, setSelectedRole] = useState<string>("All");
  const [data, setData] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeModalItem, setActiveModalItem] = useState<RecommendationItem | null>(null);
  const [savedStatusMap, setSavedStatusMap] = useState<Record<string, string>>({});

  useEffect(() => {
    loadRecommendations();
  }, [model]);

  async function loadRecommendations() {
    try {
      setLoading(true);
      setError(null);
      const res = await api.getRecommendations(DEMO_STUDENT_ID, model);
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load recommendations");
    } finally {
      setLoading(false);
    }
  }

  async function handleSaveInternship(internshipId: string) {
    try {
      await api.upsertApplication(DEMO_STUDENT_ID, internshipId, "saved", "Saved from recommendations");
      setSavedStatusMap((prev) => ({ ...prev, [internshipId]: "Saved!" }));
      setTimeout(() => {
        setSavedStatusMap((prev) => ({ ...prev, [internshipId]: "" }));
      }, 3000);
    } catch (err) {
      console.error(err);
    }
  }

  const filteredItems = (data?.items || []).filter((item) => {
    if (selectedRole === "All") return true;
    return item.internship.role_category.toLowerCase().includes(selectedRole.toLowerCase());
  });

  const roles = ["All", "Backend", "Frontend", "Full Stack", "Data Science", "Machine Learning", "DevOps"];

  return (
    <div className="space-y-8">
      {/* Header & Model Control Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">
            Personalized Internship Recommendations
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Explainable matching grounded in your verified skills, academic background, and portfolio evidence.
          </p>
        </div>

        {/* Algorithm Switcher */}
        <div className="flex items-center gap-2 bg-slate-100 p-1.5 rounded-xl border border-slate-200 text-xs font-semibold self-start md:self-auto">
          <button
            onClick={() => setModel("hybrid")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              model === "hybrid"
                ? "bg-white text-indigo-700 shadow-sm font-bold"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Hybrid Model (Default)
          </button>
          <button
            onClick={() => setModel("semantic_dense")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              model === "semantic_dense"
                ? "bg-white text-indigo-700 shadow-sm font-bold"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Semantic Dense
          </button>
          <button
            onClick={() => setModel("baseline_tfidf")}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              model === "baseline_tfidf"
                ? "bg-white text-indigo-700 shadow-sm font-bold"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Baseline TF-IDF
          </button>
        </div>
      </div>

      {/* Role Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-bold text-slate-400 mr-2 uppercase tracking-wider flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" />
          Role:
        </span>
        {roles.map((r) => (
          <button
            key={r}
            onClick={() => setSelectedRole(r)}
            className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition ${
              selectedRole === r
                ? "bg-indigo-600 text-white shadow-sm"
                : "bg-white text-slate-600 hover:bg-slate-100 border border-slate-200"
            }`}
          >
            {r}
          </button>
        ))}
      </div>

      {/* Model Information Notice */}
      <div className="bg-indigo-50/70 border border-indigo-200/60 rounded-xl p-4 flex items-start gap-3 text-xs text-indigo-900">
        <Info className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Active Ranking Strategy: </span>
          {model === "hybrid" && (
            <span>
              <strong>Hybrid Ranker</strong> synthesizes Required Skills (35%), Dense Semantic Similarity (25%), Project Tech Stack Relevance (15%), Preferred Skills (10%), Education Compatibility (10%), and Role Preferences (5%).
            </span>
          )}
          {model === "semantic_dense" && (
            <span>
              <strong>Semantic Dense Matcher</strong> compares high-dimensional token representations enriched by taxonomy metadata to match broader conceptual competencies.
            </span>
          )}
          {model === "baseline_tfidf" && (
            <span>
              <strong>Baseline Model</strong> uses standard term frequency–inverse document frequency (TF-IDF) and cosine similarity across student and job descriptions.
            </span>
          )}
        </div>
      </div>

      {/* Recommendation Cards Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
          <div className="h-64 bg-slate-200 rounded-xl"></div>
          <div className="h-64 bg-slate-200 rounded-xl"></div>
        </div>
      ) : filteredItems.length === 0 ? (
        <div className="bg-white rounded-xl border border-slate-200 p-12 text-center">
          <p className="text-slate-500 font-medium">No opportunities matching the selected filter.</p>
          <button
            onClick={() => setSelectedRole("All")}
            className="mt-3 text-xs text-indigo-600 font-bold hover:underline"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredItems.map((item) => (
            <div
              key={item.internship_id}
              className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between"
            >
              <div>
                {/* Header with Match Score */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                      {item.internship.company}
                    </span>
                    <h3 className="text-lg font-bold text-slate-900 leading-snug hover:text-indigo-600 transition">
                      <Link href={`/internships/${item.internship_id}`}>{item.internship.title}</Link>
                    </h3>
                  </div>

                  <button
                    onClick={() => setActiveModalItem(item)}
                    className="flex flex-col items-center justify-center px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-700 hover:bg-emerald-100 transition shrink-0"
                    title="Click to view explainable score breakdown"
                  >
                    <span className="text-base font-black leading-none">{item.match_score}</span>
                    <span className="text-[10px] font-bold uppercase tracking-wider mt-0.5">/ 100</span>
                  </button>
                </div>

                {/* Metadata Pills */}
                <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 mb-4">
                  <span className="flex items-center gap-1 bg-slate-50 px-2 py-1 rounded border border-slate-100">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    {item.internship.location}
                  </span>
                  {item.internship.is_remote && (
                    <span className="bg-indigo-50 text-indigo-700 font-semibold px-2 py-1 rounded border border-indigo-100">
                      Remote Friendly
                    </span>
                  )}
                  {item.internship.stipend && (
                    <span className="flex items-center gap-1 bg-slate-50 px-2 py-1 rounded border border-slate-100">
                      <DollarSign className="w-3.5 h-3.5 text-slate-400" />
                      {item.internship.stipend}
                    </span>
                  )}
                  <span className="flex items-center gap-1 bg-slate-50 px-2 py-1 rounded border border-slate-100">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    {item.internship.duration_weeks} Weeks
                  </span>
                </div>

                {/* Grounded Explanation */}
                <div className="bg-slate-50/80 rounded-lg p-3.5 border border-slate-100 text-xs text-slate-700 space-y-2 mb-4">
                  <div className="flex items-center gap-1.5 text-slate-900 font-bold">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                    <span>Why This Fits You:</span>
                  </div>
                  <p className="leading-relaxed">{item.explanation}</p>
                </div>

                {/* Required Skills Badges */}
                <div className="space-y-1.5">
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                    Core Technologies
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {item.internship.required_skills.map((skill) => {
                      const isMatched = item.matched_required_skills.includes(skill);
                      return (
                        <span
                          key={skill}
                          className={`text-xs px-2.5 py-0.5 rounded-md font-medium flex items-center gap-1 ${
                            isMatched
                              ? "bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold"
                              : "bg-slate-100 text-slate-600 border border-slate-200"
                          }`}
                        >
                          {isMatched && <CheckCircle className="w-3 h-3 text-emerald-600" />}
                          {skill}
                        </span>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                <button
                  onClick={() => handleSaveInternship(item.internship_id)}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:text-indigo-600 hover:bg-slate-50 rounded-lg border border-slate-200 transition"
                >
                  <Bookmark className="w-3.5 h-3.5" />
                  <span>{savedStatusMap[item.internship_id] || "Save"}</span>
                </button>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setActiveModalItem(item)}
                    className="text-xs font-semibold text-slate-600 hover:text-slate-900 px-2 py-1.5"
                  >
                    Breakdown
                  </button>
                  <Link
                    href={`/internships/${item.internship_id}`}
                    className="inline-flex items-center gap-1 px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg shadow-sm transition"
                  >
                    <span>Inspect Gaps</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Explainability Breakdown Modal */}
      {activeModalItem && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-5 animate-in fade-in zoom-in-95">
            <div className="flex items-start justify-between pb-3 border-b border-slate-100">
              <div>
                <span className="text-xs font-bold uppercase text-indigo-600">Explainable Match Breakdown</span>
                <h3 className="text-lg font-bold text-slate-900">{activeModalItem.internship.title}</h3>
                <p className="text-xs text-slate-500">{activeModalItem.internship.company}</p>
              </div>
              <button
                onClick={() => setActiveModalItem(null)}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold p-1"
              >
                ✕
              </button>
            </div>

            {/* Overall Score */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-slate-500 uppercase">Composite Match Score</span>
                <p className="text-xs text-slate-500 mt-0.5">Calculated by formulaic multi-attribute weights</p>
              </div>
              <div className="text-2xl font-black text-emerald-600">
                {activeModalItem.match_score} <span className="text-sm text-slate-400">/ 100</span>
              </div>
            </div>

            {/* Factor Scores */}
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Skills Alignment (35% weight)</span>
                  <span>{activeModalItem.breakdown.skills_score}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-600 rounded-full"
                    style={{ width: `${activeModalItem.breakdown.skills_score}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Project Portfolio Evidence (15% weight)</span>
                  <span>{activeModalItem.breakdown.projects_score}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 rounded-full"
                    style={{ width: `${activeModalItem.breakdown.projects_score}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Education & Degree Match (10% weight)</span>
                  <span>{activeModalItem.breakdown.education_score}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-sky-500 rounded-full"
                    style={{ width: `${activeModalItem.breakdown.education_score}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                  <span>Preferences (Remote & Roles) (5% weight)</span>
                  <span>{activeModalItem.breakdown.preferences_score}%</span>
                </div>
                <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-amber-500 rounded-full"
                    style={{ width: `${activeModalItem.breakdown.preferences_score}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Explanation Quote */}
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100 text-xs text-slate-600">
              <span className="font-bold text-slate-800">Verifiable Rationale: </span>
              {activeModalItem.explanation}
            </div>

            <div className="pt-2 flex justify-end gap-3">
              <button
                onClick={() => setActiveModalItem(null)}
                className="px-4 py-2 bg-slate-100 text-slate-700 text-xs font-bold rounded-lg hover:bg-slate-200 transition"
              >
                Close
              </button>
              <Link
                href={`/roadmap/${activeModalItem.internship_id}`}
                className="px-4 py-2 bg-indigo-600 text-white text-xs font-bold rounded-lg hover:bg-indigo-500 transition"
              >
                Start Preparation
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
