"use client";

import { useEffect, useState } from "react";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { StudentData, StudentSkill } from "@/lib/types";
import {
  User,
  BookOpen,
  Plus,
  Trash2,
  FileText,
  Sparkles,
  ShieldCheck,
  CheckCircle,
  AlertCircle,
  Briefcase,
  Layers,
} from "lucide-react";

export default function ProfilePage() {
  const [student, setStudent] = useState<StudentData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string>("");
  const [newSkillName, setNewSkillName] = useState<string>("");
  const [resumeText, setResumeText] = useState<string>("");
  const [parsingResume, setParsingResume] = useState<boolean>(false);
  const [parsedPreview, setParsedPreview] = useState<any | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    headline: "",
    education_degree: "",
    education_major: "",
    graduation_year: 2026,
    gpa: 3.75,
    bio: "",
    location: "",
    remote_preference: "flexible" as any,
    preferred_roles: [] as string[],
  });

  useEffect(() => {
    loadProfile();
  }, []);

  async function loadProfile() {
    try {
      setLoading(true);
      const res = await api.getProfile(DEMO_STUDENT_ID);
      setStudent(res);
      if (res.profile) {
        setFormData({
          headline: res.profile.headline || "",
          education_degree: res.profile.education_degree || "",
          education_major: res.profile.education_major || "",
          graduation_year: res.profile.graduation_year || 2026,
          gpa: res.profile.gpa || 3.75,
          bio: res.profile.bio || "",
          location: res.profile.location || "",
          remote_preference: res.profile.remote_preference || "flexible",
          preferred_roles: res.profile.preferred_roles || [],
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleSaveProfile(e: React.FormEvent) {
    e.preventDefault();
    try {
      setSaving(true);
      await api.updateProfile(DEMO_STUDENT_ID, formData);
      setSaveMessage("Profile changes saved successfully!");
      setTimeout(() => setSaveMessage(""), 3500);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  }

  async function handleAddSkill(e: React.FormEvent) {
    e.preventDefault();
    if (!newSkillName.trim()) return;
    try {
      await api.addSkill(DEMO_STUDENT_ID, newSkillName);
      setNewSkillName("");
      loadProfile();
    } catch (err) {
      console.error(err);
    }
  }

  async function handleDeleteSkill(skillName: string) {
    try {
      await api.deleteSkill(DEMO_STUDENT_ID, skillName);
      loadProfile();
    } catch (err) {
      console.error(err);
    }
  }

  async function handleParseResume() {
    if (!resumeText.trim()) return;
    try {
      setParsingResume(true);
      const parsed = await api.parseResume(resumeText);
      setParsedPreview(parsed);
    } catch (err) {
      console.error(err);
    } finally {
      setParsingResume(false);
    }
  }

  async function handleConfirmParsedResume() {
    if (!parsedPreview) return;
    try {
      // 1. Update Profile Fields
      await api.updateProfile(DEMO_STUDENT_ID, {
        headline: parsedPreview.headline,
        education_degree: parsedPreview.education_degree,
        education_major: parsedPreview.education_major,
        graduation_year: parsedPreview.graduation_year,
        gpa: parsedPreview.gpa,
        bio: parsedPreview.bio,
      });

      // 2. Add Extracted Skills
      for (const sk of parsedPreview.skills) {
        await api.addSkill(DEMO_STUDENT_ID, sk.skill_name, sk.proficiency_level);
      }

      setParsedPreview(null);
      setResumeText("");
      setSaveMessage("Resume data reviewed and imported into your profile!");
      setTimeout(() => setSaveMessage(""), 4000);
      loadProfile();
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) {
    return <div className="p-8 text-center text-slate-500 animate-pulse">Loading profile data...</div>;
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between pb-6 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">Student Profile & Competencies</h1>
          <p className="text-sm text-slate-500 mt-1">
            Maintain your verified skills, education history, and AI resume extraction review.
          </p>
        </div>
        {saveMessage && (
          <span className="text-xs font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg flex items-center gap-1.5 animate-in fade-in">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>{saveMessage}</span>
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Profile Details Form */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
          <div className="flex items-center gap-2 pb-4 border-b border-slate-100">
            <User className="w-5 h-5 text-indigo-600" />
            <h2 className="text-base font-bold text-slate-900">Academic & Career Profile</h2>
          </div>

          <form onSubmit={handleSaveProfile} className="space-y-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                Headline
              </label>
              <input
                type="text"
                value={formData.headline}
                onChange={(e) => setFormData({ ...formData, headline: e.target.value })}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Degree
                </label>
                <input
                  type="text"
                  value={formData.education_degree}
                  onChange={(e) => setFormData({ ...formData, education_degree: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Major
                </label>
                <input
                  type="text"
                  value={formData.education_major}
                  onChange={(e) => setFormData({ ...formData, education_major: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Graduation Year
                </label>
                <input
                  type="number"
                  value={formData.graduation_year}
                  onChange={(e) => setFormData({ ...formData, graduation_year: parseInt(e.target.value) || 2026 })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Cumulative GPA
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.gpa}
                  onChange={(e) => setFormData({ ...formData, gpa: parseFloat(e.target.value) || 3.0 })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Location
                </label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                  Remote Preference
                </label>
                <select
                  value={formData.remote_preference}
                  onChange={(e) => setFormData({ ...formData, remote_preference: e.target.value as any })}
                  className="w-full px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none bg-white"
                >
                  <option value="flexible">Flexible / Any</option>
                  <option value="remote_only">Remote Only</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="onsite_only">Onsite Only</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                Bio & Career Objectives
              </label>
              <textarea
                rows={3}
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                className="w-full p-3.5 rounded-xl border border-slate-200 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-md transition disabled:bg-slate-300"
            >
              {saving ? "Saving Changes..." : "Save Profile Updates"}
            </button>
          </form>
        </div>

        {/* Right Column: Verified Skills & Provenance */}
        <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <h2 className="text-base font-bold text-slate-900">Verified Skills</h2>
            </div>
            <span className="text-xs text-slate-400 font-bold">{student?.skills.length || 0} Total</span>
          </div>

          {/* Add Skill Input */}
          <form onSubmit={handleAddSkill} className="flex gap-2">
            <input
              type="text"
              placeholder="e.g. Docker, TypeScript"
              value={newSkillName}
              onChange={(e) => setNewSkillName(e.target.value)}
              className="flex-1 px-3 py-1.5 rounded-lg border border-slate-200 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
            <button
              type="submit"
              className="px-3 py-1.5 bg-indigo-600 text-white text-xs font-bold rounded-lg hover:bg-indigo-500 transition shrink-0"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </form>

          {/* Skills List with Provenance Badges */}
          <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
            {student?.skills.map((s) => (
              <div
                key={s.canonical_name}
                className="flex items-center justify-between p-2.5 rounded-lg border border-slate-100 bg-slate-50/60 hover:bg-slate-50 transition"
              >
                <div>
                  <span className="text-xs font-bold text-slate-800 block">{s.canonical_name}</span>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span
                      className={`text-[9px] font-bold uppercase px-1.5 py-0.2 rounded ${
                        s.provenance === "interview_verified"
                          ? "bg-emerald-100 text-emerald-800"
                          : s.provenance === "learning_progress"
                          ? "bg-indigo-100 text-indigo-800"
                          : s.provenance === "resume_extracted"
                          ? "bg-sky-100 text-sky-800"
                          : "bg-slate-200 text-slate-700"
                      }`}
                    >
                      {s.provenance.replace("_", " ")}
                    </span>
                    <span className="text-[10px] text-slate-400">• {s.proficiency_level}</span>
                  </div>
                </div>

                <button
                  onClick={() => handleDeleteSkill(s.canonical_name)}
                  className="text-slate-400 hover:text-rose-600 p-1 transition"
                  title="Remove skill"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* AI Resume Analyzer Studio (Review / Confirm Workflow) */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              <h2 className="text-lg font-bold text-slate-900">AI Resume Parser & Review Studio</h2>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Extracts competencies with human-in-the-loop review. Parsed information must be reviewed before saving into your authoritative profile.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500">
            Paste Resume Plain Text (or summary document)
          </label>
          <textarea
            rows={5}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume content here including Education, Technical Skills, and Projects..."
            className="w-full p-4 rounded-xl border border-slate-200 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          />

          <button
            onClick={handleParseResume}
            disabled={parsingResume || resumeText.trim().length < 20}
            className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold rounded-xl shadow-md transition disabled:bg-slate-300 flex items-center gap-2"
          >
            {parsingResume ? (
              <span>Extracting structured data...</span>
            ) : (
              <>
                <FileText className="w-4 h-4 text-indigo-400" />
                <span>Parse Resume for Review</span>
              </>
            )}
          </button>
        </div>

        {/* Structured Review & Confirmation Preview */}
        {parsedPreview && (
          <div className="bg-indigo-50/50 rounded-2xl border border-indigo-200 p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between pb-3 border-b border-indigo-200">
              <span className="text-xs font-bold text-indigo-900 uppercase tracking-wider">
                Extracted Information Preview (Student Review)
              </span>
              <span className="text-xs text-slate-500">Inspect & Confirm</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="bg-white p-3 rounded-xl border border-indigo-100">
                <span className="text-[10px] text-slate-400 uppercase font-bold block">Degree & Major</span>
                <span className="font-bold text-slate-800">
                  {parsedPreview.education_degree} in {parsedPreview.education_major}
                </span>
                <span className="text-[10px] text-slate-500 block mt-0.5">
                  Class of {parsedPreview.graduation_year} • GPA: {parsedPreview.gpa || "N/A"}
                </span>
              </div>

              <div className="bg-white p-3 rounded-xl border border-indigo-100 md:col-span-2">
                <span className="text-[10px] text-slate-400 uppercase font-bold block">
                  Identified Canonical Skills ({parsedPreview.skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {parsedPreview.skills.map((s: any) => (
                    <span
                      key={s.skill_name}
                      className="bg-indigo-50 text-indigo-700 text-[11px] font-semibold px-2 py-0.5 rounded border border-indigo-200"
                    >
                      {s.skill_name}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-2 flex justify-end gap-3">
              <button
                onClick={() => setParsedPreview(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition"
              >
                Discard
              </button>
              <button
                onClick={handleConfirmParsedResume}
                className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg shadow-sm transition flex items-center gap-2"
              >
                <CheckCircle className="w-3.5 h-3.5" />
                <span>Confirm & Import to Profile</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
