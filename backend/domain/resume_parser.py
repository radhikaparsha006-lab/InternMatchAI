"""
AI Resume / Profile Extraction Service.
Extracts structured sections from resume text: Education, Skills, Projects, and Experience.
Allows students to review, edit, and confirm before saving.
"""

import re
from typing import Dict, Any, List
from backend.domain.skill_normalizer import SkillNormalizer

class ResumeParser:
    @staticmethod
    def parse_text(text: str) -> Dict[str, Any]:
        """
        Parses raw resume text into structured fields:
        - full_name (heuristic from header)
        - education (degree, major, graduation year, gpa)
        - skills (canonical skills extracted using SkillNormalizer)
        - projects (extracted project headings and descriptions)
        - raw_summary
        """
        if not text:
            return {
                "full_name": "",
                "headline": "",
                "education_degree": "",
                "education_major": "",
                "graduation_year": None,
                "gpa": None,
                "skills": [],
                "projects": [],
                "bio": ""
            }

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # 1. Name heuristic: first non-empty line if short
        full_name = lines[0] if lines and len(lines[0].split()) <= 4 else "Applicant"

        # 2. Extract Skills
        extracted_skills = SkillNormalizer.extract_from_text(text)

        # 3. Extract Education Degree & Major
        degree = ""
        major = ""
        grad_year = None
        gpa = None

        degree_patterns = [
            (r"\b(bachelor(?:'s)?(?:\s+of\s+science)?|b\.?s\.?|b\.?e\.?|b\.?tech)\b", "Bachelor of Science"),
            (r"\b(master(?:'s)?(?:\s+of\s+science)?|m\.?s\.?|m\.?tech)\b", "Master of Science"),
            (r"\b(ph\.?d\.?|doctorate)\b", "Ph.D.")
        ]
        text_lower = text.lower()
        for pat, deg_name in degree_patterns:
            if re.search(pat, text_lower):
                degree = deg_name
                break

        major_patterns = [
            r"computer science", r"software engineering", r"data science", 
            r"information technology", r"electrical engineering", r"robotics",
            r"mathematics", r"statistics"
        ]
        for m_pat in major_patterns:
            if re.search(rf"\b{m_pat}\b", text_lower):
                major = m_pat.title()
                break

        # Graduation year pattern
        year_match = re.search(r"\b(202[4-9]|203[0-5])\b", text)
        if year_match:
            try:
                grad_year = int(year_match.group(1))
            except ValueError:
                pass

        # GPA pattern (e.g. 3.8/4.0 or GPA: 3.75)
        gpa_match = re.search(r"\b(?:gpa|cgpa)?:?\s*([2-4]\.\d{1,2})\b(?:\s*/\s*4(?:\.0)?)?", text_lower)
        if gpa_match:
            try:
                gpa = float(gpa_match.group(1))
            except ValueError:
                pass

        # 4. Extract Projects
        projects = []
        proj_section_match = re.search(
            r"(?:project\s+experience|academic\s+projects|personal\s+projects|projects)[\s:]*\n([\s\S]*?)(?=(?:\n\s*(?:work\s+experience|experience|education|skills|certifications|awards)\b|$))",
            text,
            re.IGNORECASE
        )
        if proj_section_match:
            proj_text = proj_section_match.group(1)
            # Split by double newline or bullet points with optional indentation
            proj_blocks = [b.strip() for b in re.split(r"\n\s*\n|\n\s*(?=[•\-\*]\s+[A-Z])", proj_text) if b.strip()]
            for i, block in enumerate(proj_blocks[:4]):
                first_line = block.split("\n")[0].strip("•-* ")
                block_skills = SkillNormalizer.extract_from_text(block)
                projects.append({
                    "id": f"parsed_proj_{i+1}",
                    "title": first_line[:60] if first_line else f"Project {i+1}",
                    "description": block[:300],
                    "technologies": block_skills,
                    "github_url": "",
                    "live_url": ""
                })

        return {
            "full_name": full_name,
            "headline": f"{major or 'CS'} Student" + (f" | Class of {grad_year}" if grad_year else ""),
            "education_degree": degree or "Bachelor of Science",
            "education_major": major or "Computer Science",
            "graduation_year": grad_year or 2026,
            "gpa": gpa,
            "skills": [{"skill_name": s, "proficiency_level": "intermediate", "provenance": "resume_extracted"} for s in extracted_skills],
            "projects": projects,
            "bio": text[:400].strip()
        }
