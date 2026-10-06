"""
InternMatch AI – Verification Script for Student Name Editing & Persistence.
Tests:
1. Fetching initial profile (Alex Chen).
2. Updating full_name to 'Rahul Kumar' via PUT /api/profile/student_demo_01.
3. Verifying GET /api/profile/student_demo_01 returns 'Rahul Kumar'.
4. Verifying GET /api/dashboard/student_demo_01 reflects 'Rahul Kumar'.
5. Verifying direct database query on 'students' table confirms 'Rahul Kumar'.
6. Updating full_name back to 'Alex Chen' or keeping as 'Rahul Kumar'.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx
from sqlalchemy import select

from backend.database.connection import AsyncSessionLocal
from backend.database.models import StudentModel

async def verify_name_editing_flow():
    base_url = "http://127.0.0.1:8000"
    print("=" * 60)
    print("VERIFYING STUDENT NAME EDITING & PERSISTENCE")
    print("=" * 60)

    async with httpx.AsyncClient(base_url=base_url, timeout=10.0) as client:
        # Step 1: Check Current Profile
        print("\n[Step 1] Querying current profile from API...")
        res = await client.get("/api/profile/student_demo_01")
        assert res.status_code == 200, f"Failed GET /api/profile: {res.text}"
        current_profile = res.json()
        initial_name = current_profile["full_name"]
        print(f" -> Current Name: '{initial_name}'")

        # Step 2: Edit Name to 'Rahul Kumar'
        print("\n[Step 2] Sending PUT /api/profile/student_demo_01 with 'Rahul Kumar'...")
        update_payload = {
            "full_name": "Rahul Kumar",
            "headline": "Full-Stack AI Engineer",
            "education_degree": "Bachelor of Science",
            "education_major": "Computer Science",
            "graduation_year": 2026,
            "gpa": 3.85,
            "bio": "Passionate developer exploring distributed systems and AI.",
            "location": "San Francisco, CA",
            "remote_preference": "flexible",
            "preferred_roles": ["Backend Engineer", "AI Engineer"],
            "preferred_industries": ["Artificial Intelligence", "Cloud"]
        }
        put_res = await client.put("/api/profile/student_demo_01", json=update_payload)
        assert put_res.status_code == 200, f"Failed PUT /api/profile: {put_res.text}"
        put_data = put_res.json()
        print(f" -> PUT response: {put_data}")
        assert put_data["full_name"] == "Rahul Kumar", "Expected full_name 'Rahul Kumar' in response"

        # Step 3: Fetch Profile again to verify API persistence
        print("\n[Step 3] Fetching profile to verify persistence across requests...")
        get_res2 = await client.get("/api/profile/student_demo_01")
        assert get_res2.status_code == 200
        get_data2 = get_res2.json()
        print(f" -> Fetched Profile full_name: '{get_data2['full_name']}'")
        assert get_data2["full_name"] == "Rahul Kumar", "Profile full_name did not persist!"

        # Step 4: Verify Dashboard greeting reflects 'Rahul Kumar'
        print("\n[Step 4] Fetching dashboard to verify app-wide student greeting...")
        dash_res = await client.get("/api/dashboard/student_demo_01")
        assert dash_res.status_code == 200
        dash_data = dash_res.json()
        dash_student_name = dash_data["student"]["full_name"]
        print(f" -> Dashboard student full_name: '{dash_student_name}'")
        assert dash_student_name == "Rahul Kumar", "Dashboard did not reflect updated name!"

        # Step 5: Direct Database Query check
        print("\n[Step 5] Direct Database inspection on 'students' table...")
        async with AsyncSessionLocal() as session:
            db_student = await session.get(StudentModel, "student_demo_01")
            assert db_student is not None
            print(f" -> DB Student Record: id='{db_student.id}', full_name='{db_student.full_name}'")
            assert db_student.full_name == "Rahul Kumar", "Database record does not match!"

        print("\n" + "=" * 60)
        print("SUCCESS: Student name editing, API, and DB persistence 100% verified!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(verify_name_editing_flow())
