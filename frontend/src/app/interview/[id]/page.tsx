"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, DEMO_STUDENT_ID } from "@/lib/api";
import { StartInterviewResponse, InterviewQuestion, SubmitAnswerResponse } from "@/lib/types";
import {
  ArrowLeft,
  MessageSquare,
  Sparkles,
  Send,
  CheckCircle2,
  AlertCircle,
  Award,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  RefreshCw,
} from "lucide-react";

export default function MockInterviewPage() {
  const params = useParams();
  const id = params?.id as string;

  const [session, setSession] = useState<StartInterviewResponse | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<InterviewQuestion | null>(null);
  const [studentAnswer, setStudentAnswer] = useState<string>("");
  const [evalResult, setEvalResult] = useState<SubmitAnswerResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      initInterview();
    }
  }, [id]);

  async function initInterview() {
    try {
      setLoading(true);
      setError(null);
      setEvalResult(null);
      setStudentAnswer("");
      const res = await api.startInterview(DEMO_STUDENT_ID, id);
      setSession(res);
      setCurrentQuestion(res.first_question);
    } catch (err: any) {
      setError(err?.message || "Failed to initialize mock interview session");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitAnswer() {
    if (!session || !currentQuestion || !studentAnswer.trim()) return;

    try {
      setSubmitting(true);
      setError(null);
      const res = await api.submitInterviewAnswer(
        session.session_id,
        currentQuestion.question_number,
        studentAnswer
      );
      setEvalResult(res);
    } catch (err: any) {
      setError(err?.message || "Failed to evaluate answer");
    } finally {
      setSubmitting(false);
    }
  }

  function handleNextQuestion() {
    if (!evalResult?.next_question) return;
    setCurrentQuestion(evalResult.next_question);
    setStudentAnswer("");
    setEvalResult(null);
  }

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse max-w-3xl mx-auto">
        <div className="h-8 w-40 bg-slate-200 rounded"></div>
        <div className="h-48 bg-slate-200 rounded-2xl"></div>
        <div className="h-64 bg-slate-200 rounded-2xl"></div>
      </div>
    );
  }

  if (error && !session) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-8 text-center text-red-700 max-w-2xl mx-auto">
        <p className="font-semibold">{error}</p>
        <button
          onClick={initInterview}
          className="mt-4 px-4 py-2 bg-red-600 text-white text-xs font-bold rounded-lg hover:bg-red-700"
        >
          Retry Session
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-3xl mx-auto">
      {/* Back button */}
      <div>
        <Link
          href={`/roadmap/${id}`}
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-indigo-600 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Preparation Roadmap</span>
        </Link>
      </div>

      {/* Interview Studio Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded">
            <MessageSquare className="w-4 h-4" />
            <span>Adaptive Mock Interview Studio</span>
          </div>
          <span className="text-xs text-slate-400 font-medium">Text-Based Technical Simulator</span>
        </div>

        <div>
          <h1 className="text-2xl font-black text-slate-900">{session?.role_title}</h1>
          <p className="text-xs text-slate-500 mt-1">
            Questions are generated from the target role&apos;s required competencies and your profile skill gaps. Difficulty adapts based on your previous answers.
          </p>
        </div>
      </div>

      {/* Session Complete View */}
      {evalResult?.session_complete ? (
        <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl p-8 shadow-xl text-center space-y-6">
          <div className="w-16 h-16 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto border border-emerald-500/30">
            <Award className="w-8 h-8" />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-black">Interview Session Complete!</h2>
            <p className="text-sm text-slate-300 max-w-lg mx-auto">
              You completed all questions in this mock interview. Your performance has been factored into your Internship Readiness Index.
            </p>
          </div>

          <div className="bg-white/10 max-w-xs mx-auto p-4 rounded-xl border border-white/10">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300 block">
              Average Interview Performance
            </span>
            <span className="text-4xl font-extrabold text-emerald-400 mt-1 block">
              {evalResult.average_session_score ?? evalResult.overall_score} / 100
            </span>
          </div>

          <div className="pt-4 flex flex-wrap justify-center gap-4">
            <button
              onClick={initInterview}
              className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold rounded-xl border border-slate-700 transition flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Restart Interview</span>
            </button>
            <Link
              href="/"
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2"
            >
              <span>Return to Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      ) : (
        /* Active Question & Answer Box */
        <div className="space-y-6">
          {currentQuestion && (
            <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-5">
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-slate-400 uppercase tracking-wider">
                  QUESTION {currentQuestion.question_number} OF 3
                </span>
                <div className="flex items-center gap-2">
                  <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200">
                    {currentQuestion.category}
                  </span>
                  <span
                    className={`px-2 py-0.5 rounded border uppercase text-[10px] ${
                      currentQuestion.difficulty === "hard"
                        ? "bg-rose-50 text-rose-700 border-rose-200"
                        : currentQuestion.difficulty === "medium"
                        ? "bg-amber-50 text-amber-700 border-amber-200"
                        : "bg-emerald-50 text-emerald-700 border-emerald-200"
                    }`}
                  >
                    {currentQuestion.difficulty}
                  </span>
                </div>
              </div>

              <div>
                <span className="text-xs font-semibold text-indigo-600 block mb-1">
                  Testing competency: {currentQuestion.tested_skill}
                </span>
                <h2 className="text-lg font-bold text-slate-900 leading-snug">
                  {currentQuestion.question_text}
                </h2>
              </div>

              {/* Answer Input */}
              {!evalResult && (
                <div className="space-y-4 pt-2">
                  <label htmlFor="answer-input" className="block text-xs font-bold uppercase tracking-wider text-slate-500">
                    Your Response
                  </label>
                  <textarea
                    id="answer-input"
                    rows={6}
                    value={studentAnswer}
                    onChange={(e) => setStudentAnswer(e.target.value)}
                    placeholder="Provide a thorough technical explanation. Explain core mechanisms, architectural tradeoffs, and practical experience..."
                    className="w-full p-4 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition resize-y"
                  />

                  <div className="flex items-center justify-between pt-2">
                    <span className="text-xs text-slate-400">
                      {studentAnswer.split(/\s+/).filter(Boolean).length} words
                    </span>
                    <button
                      onClick={handleSubmitAnswer}
                      disabled={submitting || studentAnswer.trim().length < 10}
                      className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-300 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2"
                    >
                      {submitting ? (
                        <span>Evaluating response...</span>
                      ) : (
                        <>
                          <span>Submit for Rubric Evaluation</span>
                          <Send className="w-3.5 h-3.5" />
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Feedback & Scorecard */}
          {evalResult && (
            <div className="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6 animate-in fade-in">
              <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Rubric Evaluation Scorecard
                </span>
                <span className="text-base font-extrabold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-lg border border-emerald-200">
                  {evalResult.overall_score} / 100
                </span>
              </div>

              {/* Multi-criteria scores */}
              <div className="grid grid-cols-3 gap-3">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-center">
                  <span className="text-[10px] font-bold text-slate-400 uppercase block">Correctness</span>
                  <span className="text-lg font-black text-slate-800">{evalResult.correctness_score}%</span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-center">
                  <span className="text-[10px] font-bold text-slate-400 uppercase block">Technical Depth</span>
                  <span className="text-lg font-black text-slate-800">{evalResult.technical_depth_score}%</span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-center">
                  <span className="text-[10px] font-bold text-slate-400 uppercase block">Clarity</span>
                  <span className="text-lg font-black text-slate-800">{evalResult.clarity_score}%</span>
                </div>
              </div>

              {/* Feedback Summary */}
              <div className="bg-indigo-50/60 p-4 rounded-xl border border-indigo-100 text-xs text-indigo-900 space-y-1">
                <span className="font-bold block">Evaluator Feedback:</span>
                <p className="leading-relaxed">{evalResult.feedback}</p>
              </div>

              {/* Model Highlights */}
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 text-xs text-slate-700 space-y-1">
                <span className="font-bold text-slate-900 block">Exemplary Discussion Points:</span>
                <p className="leading-relaxed">{evalResult.model_answer_highlights}</p>
              </div>

              {/* Closed-loop verified indicator */}
              {evalResult.overall_score >= 70 && (
                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 p-3 rounded-xl">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>
                    Great performance! {currentQuestion?.tested_skill} verified in your profile competencies.
                  </span>
                </div>
              )}

              {/* Next Question CTA */}
              <div className="pt-2 flex justify-end">
                {evalResult.next_question ? (
                  <button
                    onClick={handleNextQuestion}
                    className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2"
                  >
                    <span>Proceed to Next Question</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                ) : (
                  <button
                    onClick={() => setEvalResult({ ...evalResult, session_complete: true })}
                    className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl shadow-md transition flex items-center gap-2"
                  >
                    <span>View Final Session Score</span>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
