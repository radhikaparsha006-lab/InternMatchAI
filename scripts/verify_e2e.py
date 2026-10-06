"""
End-to-End System Verification Script for InternMatch AI.
Simulates the complete student journey across all core capabilities.
"""

import asyncio
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.database.connection import init_db, AsyncSessionLocal
from backend.database.repository import DataRepository

async def run_e2e_verification():
    print("=" * 80)
    print("INTERNMATCH AI – END-TO-END VERIFICATION SUITE")
    print("=" * 80)

    # 1. Initialize Database & Seed
    await init_db()
    async with AsyncSessionLocal() as session:
        repo = DataRepository(session)
        await repo.seed_initial_data_if_needed()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Health Check
        print("\n[Step 1] Checking API Health...")
        health_res = await client.get("/api/health")
        assert health_res.status_code == 200
        print(f" -> PASS: Health check responded: {health_res.json()}")

        # Step 2: Fetch Student Profile
        print("\n[Step 2] Fetching initial profile for 'Alex Chen'...")
        prof_res = await client.get("/api/profile/student_demo_01")
        assert prof_res.status_code == 200
        student_data = prof_res.json()
        print(f" -> PASS: Student loaded: {student_data['full_name']} ({student_data['profile']['headline']})")
        print(f"    Initial verified skills: {[s['canonical_name'] for s in student_data['skills']]}")

        # Step 3: AI Resume Parsing & Extraction Workflow
        print("\n[Step 3] Testing AI Resume Parsing workflow...")
        sample_resume = """
        Alex Chen
        Junior Computer Science Student, graduation year 2026. GPA: 3.75.
        Technical Skills: Python, SQL, Git, Linux, Docker, REST APIs.
        Built automated REST API with Python and Flask.
        """
        parse_res = await client.post("/api/resume/parse", json={"resume_text": sample_resume})
        assert parse_res.status_code == 200
        parsed = parse_res.json()
        print(f" -> PASS: Resume parsed. Extracted {len(parsed['skills'])} skills: {[s['skill_name'] for s in parsed['skills']]}")

        # Step 4: Compare Recommendation Models
        print("\n[Step 4] Evaluating Staged Recommendations...")
        models = ["baseline_tfidf", "semantic_dense", "hybrid"]
        top_picks = {}
        for m in models:
            rec_res = await client.get(f"/api/recommendations/student_demo_01?model={m}")
            assert rec_res.status_code == 200
            data = rec_res.json()
            top = data["items"][0]
            top_picks[m] = top
            print(f" -> PASS [{m.upper()}]: Top match '{top['internship']['title']}' (Score: {top['match_score']}/100)")
            if m == "hybrid":
                print(f"    Breakdown: {top['breakdown']}")
                print(f"    Explanation: {top['explanation']}")

        target_intern_id = "intern_01"  # CloudScale Systems Backend Intern

        # Step 5: Skill Gap Analysis
        print(f"\n[Step 5] Analyzing Target-Specific Skill Gaps for '{target_intern_id}'...")
        gap_res = await client.get(f"/api/skill-gap/student_demo_01/{target_intern_id}")
        assert gap_res.status_code == 200
        gap_data = gap_res.json()
        print(f" -> PASS: Coverage: {gap_data['coverage_percentage']}%, Severity: {gap_data['severity']}")
        print(f"    Critical Gaps: {[g['skill_name'] for g in gap_data['gaps']['critical']]}")
        print(f"    Important Gaps: {[g['skill_name'] for g in gap_data['gaps']['important']]}")

        # Step 6: Preparation Roadmap Generation
        print(f"\n[Step 6] Generating Prerequisite-Ordered Roadmap...")
        road_res = await client.get(f"/api/roadmap/student_demo_01/{target_intern_id}")
        assert road_res.status_code == 200
        road_data = road_res.json()
        print(f" -> PASS: Roadmap generated with {len(road_data['items'])} milestones (~{road_data['total_estimated_hours']} hours)")
        for idx, item in enumerate(road_data["items"]):
            print(f"    Step {idx+1}: [{item['priority'].upper()}] {item['title']} (Est: {item['estimated_hours']}h)")
            if item["trusted_resources"]:
                print(f"      Resource: {item['trusted_resources'][0]['title']} -> {item['trusted_resources'][0]['url']}")

        # Step 7: Initial Internship Readiness Index (IRI)
        print(f"\n[Step 7] Checking Initial Internship Readiness Index (IRI)...")
        iri_res_1 = await client.get(f"/api/readiness/student_demo_01/{target_intern_id}")
        assert iri_res_1.status_code == 200
        initial_iri = iri_res_1.json()
        print(f" -> PASS: Initial IRI = {initial_iri['overall_iri']}/100")
        print(f"    Components: {initial_iri['components']}")

        # Step 8: Closed-Loop Milestone Completion
        print(f"\n[Step 8] Completing Roadmap Milestone (Closed-Loop Feedback)...")
        first_item = road_data["items"][0]
        toggle_res = await client.post(
            f"/api/roadmap/student_demo_01/{target_intern_id}/item/{first_item['id']}/toggle",
            json={"is_completed": True}
        )
        assert toggle_res.status_code == 200
        toggle_data = toggle_res.json()
        print(f" -> PASS: Milestone marked complete. Overall roadmap progress: {toggle_data['overall_progress']}%")
        print(f"    Closed-loop response: {toggle_data.get('closed_loop_update')}")

        # Step 9: Verify Profile Skill Update with Provenance
        print(f"\n[Step 9] Verifying Student Profile Competency Provenance...")
        prof_res_2 = await client.get("/api/profile/student_demo_01")
        student_data_2 = prof_res_2.json()
        new_skill = next((s for s in student_data_2["skills"] if s["canonical_name"] == first_item["skill_name"]), None)
        assert new_skill is not None
        print(f" -> PASS: Skill '{new_skill['canonical_name']}' verified on profile! Provenance: '{new_skill['provenance']}'")

        # Step 10: Adaptive Mock Interview Simulation
        print(f"\n[Step 10] Simulating Adaptive Mock Interview...")
        start_res = await client.post(
            "/api/interview/start",
            json={"student_id": "student_demo_01", "target_internship_id": target_intern_id}
        )
        assert start_res.status_code == 200
        interview_sess = start_res.json()
        q1 = interview_sess["first_question"]
        print(f" -> PASS: Session created ({interview_sess['session_id']})")
        print(f"    Q1: {q1['question_text']}")

        # Submit answer
        student_answer = """
        FastAPI utilizes the Depends function for dependency injection. When interacting with relational
        database sessions like PostgreSQL or SQLAlchemy, Depends yields a database session scoped per HTTP request.
        The finally block guarantees that the connection is closed or rolled back if an error occurs.
        """
        ans_res = await client.post(
            "/api/interview/submit-answer",
            json={
                "session_id": interview_sess["session_id"],
                "question_number": q1["question_number"],
                "student_answer": student_answer
            }
        )
        assert ans_res.status_code == 200
        eval_data = ans_res.json()
        print(f" -> PASS: Answer evaluated! Score: {eval_data['overall_score']}/100")
        print(f"    Rubric: Correctness={eval_data['correctness_score']}%, Depth={eval_data['technical_depth_score']}%, Clarity={eval_data['clarity_score']}%")
        print(f"    Feedback: {eval_data['feedback']}")
        print(f"    Next Question Difficulty: {eval_data.get('next_question', {}).get('difficulty', 'completed')}")

        # Step 11: Re-evaluate Readiness Index (IRI) post-learning & interview
        print(f"\n[Step 11] Checking Post-Preparation Internship Readiness Index (IRI)...")
        iri_res_2 = await client.get(f"/api/readiness/student_demo_01/{target_intern_id}")
        assert iri_res_2.status_code == 200
        final_iri = iri_res_2.json()
        print(f" -> PASS: Final IRI = {final_iri['overall_iri']}/100 (Baseline: {initial_iri['overall_iri']}/100)")
        assert final_iri["overall_iri"] >= initial_iri["overall_iri"]

        # Step 12: Save Application to Tracker
        print(f"\n[Step 12] Logging Target Internship in Application Tracker...")
        app_res = await client.post(
            "/api/applications/student_demo_01",
            json={"internship_id": target_intern_id, "status": "applied", "notes": "Applied after completing FastAPI prep."}
        )
        assert app_res.status_code == 200
        print(f" -> PASS: {app_res.json()['message']}")

        # Step 13: Dashboard Aggregation Verification
        print(f"\n[Step 13] Verifying Cockpit Dashboard Summary...")
        dash_res = await client.get("/api/dashboard/student_demo_01")
        assert dash_res.status_code == 200
        dash = dash_res.json()
        print(f" -> PASS: Dashboard active readiness: {dash['active_readiness']['overall_iri']}/100")
        print(f"    Applications pipeline: {dash['applications_pipeline']}")

    print("\n" + "=" * 80)
    print("ALL 13 END-TO-END VERIFICATION STEPS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_e2e_verification())
