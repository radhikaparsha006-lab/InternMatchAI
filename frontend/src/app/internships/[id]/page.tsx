"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { Internship, SkillGapResponse } from "@/lib/types";
import {
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  MapPin,
  Clock,
  DollarSign,
  Calendar,
  BookOpen,
  MessageSquare,
  Bookmark,
  Target,
  ExternalLink,
} from "lucide-react";

export default function InternshipDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;

  const [internship, setInternship] = useState<Internship | null>(null);
  const [skillGap, setSkillGap] = useState<SkillGapResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<string>("");

  useEffect(() => {
    if (id) {
      loadData();
    }
  }, [id]);

  async function loadData() {
    try {
      setLoading(true);
      setError(null);
      const [internRes, gapRes] = await Promise.all([
        api.getInternship(id),
        api.getSkillGap(DEMO_STUDENT_ID, id),
      ]);
      setInternship(internRes);
      setSkillGap(gapRes);
    } catch (err: any) {
      setError(err?.message || "Failed to load internship details");
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    try {
      await api.upsertApplication(DEMO_STUDENT_ID, id, "saved", "Saved from detail studio");
      setSaveStatus("Saved to Applications!");
      setTimeout(() => setSaveStatus(""), 3000);
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-8 w-40 bg-slate-200 rounded"></div>
        <div className="h-64 bg-slate-200 rounded-2xl"></div>
        <div className="h-96 bg-slate-200 rounded-2xl"></div>
      </div>
    );
  }

  if (error || !internship || !skillGap) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center text-red-700">
        <p className="font-semibold">{error || "Internship not found"}</p>
        <Link
          href="/recommendations"
          className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-red-700 hover:underline"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Recommendations</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Back button */}
      <div>
        <Link
          href="/recommendations"
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-indigo-600 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Opportunities</span>
        </Link>
      </div>

      {/* Role Header Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded">
                {internship.role_category}
              </span>
              {internship.is_remote && (
                <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                  Remote Position
                </span>
              )}
            </div>
            <h1 className="text-2xl md:text-3xl font-black text-slate-900">{internship.title}</h1>
            <p className="text-base font-medium text-slate-600 mt-1">{internship.company}</p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleSave}
              className="px-4 py-2 text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-xl border border-slate-200 flex items-center gap-2 transition"
            >
              <Bookmark className="w-4 h-4" />
              <span>{saveStatus || "Save Opportunity"}</span>
            </button>
            <Link
              href={`/roadmap/${id}`}
              className="px-5 py-2 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl shadow-md transition flex items-center gap-2"
            >
              <BookOpen className="w-4 h-4" />
              <span>Personalized Prep Roadmap</span>
            </Link>
          </div>
        </div>

        {/* Metadata Details Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-slate-100 text-xs">
          <div>
            <span className="text-slate-400 block font-medium">Location</span>
            <span className="text-slate-800 font-bold flex items-center gap-1 mt-0.5">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              {internship.location}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Duration</span>
            <span className="text-slate-800 font-bold flex items-center gap-1 mt-0.5">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              {internship.duration_weeks} Weeks
            </span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Stipend</span>
            <span className="text-slate-800 font-bold flex items-center gap-1 mt-0.5">
              <DollarSign className="w-3.5 h-3.5 text-slate-400" />
              {internship.stipend || "Competitive"}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Application Deadline</span>
            <span className="text-slate-800 font-bold flex items-center gap-1 mt-0.5">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              {internship.application_deadline || "Open until filled"}
            </span>
          </div>
        </div>
      </div>

      {/* Target-Specific Skill Gap Studio */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5 text-indigo-600" />
              <h2 className="text-xl font-bold text-slate-900">Target-Specific Skill Gap Analysis</h2>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Your verified skills contrasted against employer requirements for this exact role.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-slate-50 p-3 rounded-xl border border-slate-200">
            <div>
              <span className="text-[10px] font-bold uppercase text-slate-400 block">Required Skills Match</span>
              <span className="text-2xl font-black text-slate-900">{skillGap.coverage_percentage}%</span>
            </div>
            <div className="h-8 w-px bg-slate-200"></div>
            <div>
              <span className="text-[10px] font-bold uppercase text-slate-400 block">Gap Severity</span>
              <span className="text-xs font-bold text-indigo-700">{skillGap.severity}</span>
            </div>
          </div>
        </div>

        {/* Matched Competencies */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Already Possessed & Verified Skills ({skillGap.matched_skills.required.length})</span>
          </h3>
          <div className="flex flex-wrap gap-2">
            {skillGap.matched_skills.required.map((s) => (
              <span
                key={s}
                className="bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-semibold px-3 py-1 rounded-lg flex items-center gap-1.5"
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                {s}
              </span>
            ))}
            {skillGap.matched_skills.preferred.map((s) => (
              <span
                key={s}
                className="bg-emerald-50/60 text-emerald-700 border border-emerald-100 text-xs font-medium px-3 py-1 rounded-lg flex items-center gap-1.5"
              >
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                {s} (Preferred)
              </span>
            ))}
          </div>
        </div>

        {/* Categorized Gap Buckets */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          {/* Critical Gaps */}
          <div className="bg-rose-50/60 border border-rose-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-2 text-rose-800">
              <AlertTriangle className="w-4 h-4" />
              <h4 className="text-xs font-bold uppercase tracking-wider">Critical Gaps (Priority 1)</h4>
            </div>
            <p className="text-xs text-rose-700/80">
              Explicitly required skills missing from your profile. Must be addressed before applying.
            </p>
            <div className="space-y-2 pt-1">
              {skillGap.gaps.critical.length === 0 ? (
                <p className="text-xs text-emerald-700 font-semibold">No critical gaps! You meet all required skills.</p>
              ) : (
                skillGap.gaps.critical.map((g) => (
                  <div key={g.skill_name} className="bg-white p-3 rounded-lg border border-rose-200/80 shadow-2xs">
                    <span className="text-xs font-bold text-rose-900 block">{g.skill_name}</span>
                    <span className="text-[11px] text-slate-500 block mt-0.5">{g.reason}</span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Important Gaps */}
          <div className="bg-amber-50/60 border border-amber-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-2 text-amber-800">
              <Sparkles className="w-4 h-4" />
              <h4 className="text-xs font-bold uppercase tracking-wider">Important Gaps (Priority 2)</h4>
            </div>
            <p className="text-xs text-amber-700/80">
              Preferred qualifications that distinguish competitive candidates during technical screens.
            </p>
            <div className="space-y-2 pt-1">
              {skillGap.gaps.important.length === 0 ? (
                <p className="text-xs text-slate-500 italic">No secondary gaps listed.</p>
              ) : (
                skillGap.gaps.important.map((g) => (
                  <div key={g.skill_name} className="bg-white p-3 rounded-lg border border-amber-200/80 shadow-2xs">
                    <span className="text-xs font-bold text-amber-900 block">{g.skill_name}</span>
                    <span className="text-[11px] text-slate-500 block mt-0.5">{g.reason}</span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Useful Gaps */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-2 text-slate-700">
              <CheckCircle2 className="w-4 h-4 text-slate-400" />
              <h4 className="text-xs font-bold uppercase tracking-wider">Useful Tools (Priority 3)</h4>
            </div>
            <p className="text-xs text-slate-500">
              Complementary ecosystem tools and best practices expected in this role category.
            </p>
            <div className="space-y-2 pt-1">
              {skillGap.gaps.useful.map((g) => (
                <div key={g.skill_name} className="bg-white p-3 rounded-lg border border-slate-200 shadow-2xs">
                  <span className="text-xs font-bold text-slate-800 block">{g.skill_name}</span>
                  <span className="text-[11px] text-slate-500 block mt-0.5">{g.reason}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Action Call to Action */}
        <div className="pt-4 flex flex-wrap items-center justify-between gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
          <div>
            <span className="text-xs font-bold text-slate-800 block">Ready to eliminate these gaps?</span>
            <p className="text-xs text-slate-500 mt-0.5">
              Generate your prerequisite-sequenced roadmap with verified resources and portfolio projects.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href={`/interview/${id}`}
              className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 text-xs font-bold rounded-lg transition flex items-center gap-1.5"
            >
              <MessageSquare className="w-3.5 h-3.5" />
              <span>Simulate Interview</span>
            </Link>
            <Link
              href={`/roadmap/${id}`}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg shadow-sm transition flex items-center gap-1.5"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Generate Roadmap</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Full Description & Education Criteria */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
        <div>
          <h3 className="text-base font-bold text-slate-900 mb-2">Role Overview & Responsibilities</h3>
          <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">{internship.description}</p>
        </div>

        {internship.education_requirement && (
          <div className="pt-4 border-t border-slate-100">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
              Education & Academic Eligibility
            </h4>
            <p className="text-xs text-slate-700">{internship.education_requirement}</p>
          </div>
        )}

        {internship.source_url && (
          <div className="pt-2">
            <a
              href={internship.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-600 hover:underline"
            >
              <span>View Source Posting</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
