"""
Seed data for Skills, Internships, Learning Resources, and Demo Student Profile.
"""

from datetime import date, timedelta
from typing import List, Dict, Any
from backend.domain.taxonomy import SKILL_TAXONOMY

# 25+ Rich, diverse, realistic internships
SEED_INTERNSHIPS: List[Dict[str, Any]] = [
    {
        "id": "intern_01",
        "title": "Backend Engineering Intern (Python / FastAPI)",
        "company": "CloudScale Systems",
        "role_category": "Backend",
        "location": "San Francisco, CA",
        "is_remote": True,
        "duration_weeks": 12,
        "stipend": "$45 / hr",
        "description": "Join our distributed platform team to build high-performance REST and streaming APIs using Python and FastAPI. You will collaborate on microservice architectures, PostgreSQL schema optimization, and Docker containerization.",
        "education_requirement": "Pursuing BS or MS in Computer Science, Software Engineering, or related field.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "REST APIs"],
        "preferred_skills": ["Docker", "Redis", "Git", "Automated Testing"],
        "application_deadline": (date.today() + timedelta(days=45)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.cloudscale.example.com/backend-intern"
    },
    {
        "id": "intern_02",
        "title": "Frontend Engineering Intern (React & Next.js)",
        "company": "Apex Digital Labs",
        "role_category": "Frontend",
        "location": "New York, NY",
        "is_remote": True,
        "duration_weeks": 12,
        "stipend": "$40 / hr",
        "description": "Craft responsive, accessible web interfaces for our client-facing analytics suite. Work with Next.js App Router, Tailwind CSS, TypeScript, and modern state management to deliver delightful developer and customer experiences.",
        "education_requirement": "Enrolled in Computer Science, Web Development, or equivalent technical program.",
        "required_skills": ["JavaScript", "TypeScript", "React", "Next.js", "HTML/CSS"],
        "preferred_skills": ["Tailwind CSS", "Git", "REST APIs"],
        "application_deadline": (date.today() + timedelta(days=30)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.apexdigital.example.com/frontend-intern"
    },
    {
        "id": "intern_03",
        "title": "Full Stack Software Engineering Intern",
        "company": "Nexus HealthTech",
        "role_category": "Full Stack",
        "location": "Boston, MA",
        "is_remote": False,
        "duration_weeks": 14,
        "stipend": "$38 / hr",
        "description": "Build end-to-end patient workflow tools. Work across the stack using React and TypeScript on the frontend and Node.js with PostgreSQL and Supabase on the backend. Emphasizes clean API contracts and secure data handling.",
        "education_requirement": "Undergraduate junior or senior in Computer Science or Computer Engineering.",
        "required_skills": ["JavaScript", "TypeScript", "React", "Node.js", "PostgreSQL"],
        "preferred_skills": ["Supabase", "Git", "REST APIs", "Automated Testing"],
        "application_deadline": (date.today() + timedelta(days=20)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.nexushealth.example.com/fullstack-intern"
    },
    {
        "id": "intern_04",
        "title": "Data Science & Analytics Intern",
        "company": "FinMetrics AI",
        "role_category": "Data Science",
        "location": "Chicago, IL",
        "is_remote": True,
        "duration_weeks": 10,
        "stipend": "$42 / hr",
        "description": "Analyze multi-terabyte transactional datasets to generate predictive signals and automated business intelligence reports. Heavy use of Python, Pandas, SQL, and Scikit-Learn for statistical modeling and visualization.",
        "education_requirement": "Enrolled in BS/MS/PhD in Data Science, Statistics, Mathematics, or Computer Science.",
        "required_skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn"],
        "preferred_skills": ["Machine Learning", "Git", "Communication"],
        "application_deadline": (date.today() + timedelta(days=50)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.finmetrics.example.com/data-intern"
    },
    {
        "id": "intern_05",
        "title": "Machine Learning Research Intern (NLP)",
        "company": "Cognitive Frontier",
        "role_category": "Machine Learning",
        "location": "Seattle, WA",
        "is_remote": True,
        "duration_weeks": 12,
        "stipend": "$50 / hr",
        "description": "Assist in researching and fine-tuning transformer-based NLP architectures for code generation and semantic document retrieval. Implement training loops in PyTorch, build evaluation benchmarks, and containerize pipelines in Docker.",
        "education_requirement": "Pursuing MS or PhD in Computer Science, Machine Learning, or AI.",
        "required_skills": ["Python", "PyTorch", "Machine Learning", "Natural Language Processing (NLP)"],
        "preferred_skills": ["Docker", "Linux", "Git", "Scikit-Learn"],
        "application_deadline": (date.today() + timedelta(days=35)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.cognitivefrontier.example.com/ml-intern"
    },
    {
        "id": "intern_06",
        "title": "DevOps & Cloud Infrastructure Intern",
        "company": "Vanguard Cloud Services",
        "role_category": "DevOps",
        "location": "Austin, TX",
        "is_remote": False,
        "duration_weeks": 12,
        "stipend": "$36 / hr",
        "description": "Support our reliability engineering team in managing AWS infrastructure, developing GitHub Actions CI/CD workflows, and automating Docker container deployments. You will learn production infrastructure-as-code and observability.",
        "education_requirement": "Pursuing degree in Computer Science, Information Technology, or Systems Engineering.",
        "required_skills": ["Linux", "Git", "Docker", "AWS"],
        "preferred_skills": ["CI/CD", "Python", "System Design"],
        "application_deadline": (date.today() + timedelta(days=25)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.vanguardcloud.example.com/devops-intern"
    },
    {
        "id": "intern_07",
        "title": "Junior Python Web Developer Intern",
        "company": "Beacon Analytics",
        "role_category": "Backend",
        "location": "Denver, CO",
        "is_remote": True,
        "duration_weeks": 10,
        "stipend": "$32 / hr",
        "description": "Ideal for students eager to expand their Python backend capabilities. Help develop internal dashboard APIs and ETL pipelines using Python, Django or FastAPI, and relational databases. Mentorship provided.",
        "education_requirement": "Sophomore or Junior in STEM or relevant bootcamp graduate.",
        "required_skills": ["Python", "SQL", "Git"],
        "preferred_skills": ["FastAPI", "PostgreSQL", "REST APIs", "Team Collaboration"],
        "application_deadline": (date.today() + timedelta(days=60)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.beaconanalytics.example.com/junior-backend"
    },
    {
        "id": "intern_08",
        "title": "UI/UX & Web Development Intern",
        "company": "PixelCraft Studios",
        "role_category": "Frontend",
        "location": "San Francisco, CA",
        "is_remote": True,
        "duration_weeks": 12,
        "stipend": "$35 / hr",
        "description": "Translate high-fidelity Figma mockups into interactive React applications with Tailwind CSS. Focus on fluid animations, mobile responsiveness, and clean component architecture.",
        "education_requirement": "Any degree discipline with a strong portfolio of interactive web projects.",
        "required_skills": ["JavaScript", "React", "HTML/CSS", "Tailwind CSS"],
        "preferred_skills": ["TypeScript", "Git", "Communication"],
        "application_deadline": (date.today() + timedelta(days=40)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.pixelcraft.example.com/ui-intern"
    },
    {
        "id": "intern_09",
        "title": "Enterprise Java Backend Intern",
        "company": "Kestrel Financial Software",
        "role_category": "Backend",
        "location": "Charlotte, NC",
        "is_remote": False,
        "duration_weeks": 12,
        "stipend": "$37 / hr",
        "description": "Build resilient core payment processing services using Java, Spring Boot, and PostgreSQL. Focus on concurrency, transaction isolation, and high-throughput data processing.",
        "education_requirement": "BS in Computer Science or Software Engineering.",
        "required_skills": ["Java", "SQL", "Object-Oriented Programming (OOP)"],
        "preferred_skills": ["PostgreSQL", "Git", "REST APIs", "System Design"],
        "application_deadline": (date.today() + timedelta(days=15)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.kestrel.example.com/java-intern"
    },
    {
        "id": "intern_10",
        "title": "Applied AI & Computer Vision Intern",
        "company": "HyperVision Robotics",
        "role_category": "Machine Learning",
        "location": "Pittsburgh, PA",
        "is_remote": False,
        "duration_weeks": 14,
        "stipend": "$46 / hr",
        "description": "Work with robotics sensor pipelines to deploy real-time vision algorithms. Train PyTorch models, optimize inference with C++ and Linux tools, and benchmark model accuracy.",
        "education_requirement": "MS or senior undergraduate in Robotics, ECE, or Computer Science.",
        "required_skills": ["Python", "C++", "PyTorch", "Linux"],
        "preferred_skills": ["Machine Learning", "Git", "Docker"],
        "application_deadline": (date.today() + timedelta(days=30)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.hypervision.example.com/cv-intern"
    },
    {
        "id": "intern_11",
        "title": "API Platform & Systems Intern (Go)",
        "company": "Helix Network Infrastructure",
        "role_category": "Backend",
        "location": "Sunnyvale, CA",
        "is_remote": True,
        "duration_weeks": 12,
        "stipend": "$48 / hr",
        "description": "Build high-concurrency network proxies and telemetry collectors in Go. Work with gRPC, REST APIs, Docker, and distributed key-value stores like Redis.",
        "education_requirement": "Junior/Senior in CS or equivalent with strong grasp of systems and algorithms.",
        "required_skills": ["Go", "Data Structures & Algorithms", "Linux"],
        "preferred_skills": ["Docker", "Redis", "REST APIs", "Git"],
        "application_deadline": (date.today() + timedelta(days=45)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.helixinfra.example.com/go-intern"
    },
    {
        "id": "intern_12",
        "title": "Data Engineering Intern (ETL & Pipelines)",
        "company": "Aura Data Solutions",
        "role_category": "Data Science",
        "location": "Atlanta, GA",
        "is_remote": True,
        "duration_weeks": 12,
        "stipend": "$39 / hr",
        "description": "Design and schedule automated data ingestion pipelines from diverse third-party APIs into analytical data warehouses. Master SQL data modeling, Python scripting, and PostgreSQL database performance tuning.",
        "education_requirement": "Enrolled in BS/MS program in Data Science, Computer Science, or Informatics.",
        "required_skills": ["Python", "SQL", "PostgreSQL"],
        "preferred_skills": ["Pandas", "Docker", "Git", "REST APIs"],
        "application_deadline": (date.today() + timedelta(days=28)).isoformat(),
        "source": "curated",
        "source_url": "https://careers.auradata.example.com/data-eng-intern"
    }
]

# Trusted learning resources catalog mapped to canonical skills
TRUSTED_LEARNING_RESOURCES: Dict[str, List[Dict[str, str]]] = {
    "FastAPI": [
        {
            "title": "FastAPI Official Tutorial - User Guide",
            "url": "https://fastapi.tiangolo.com/tutorial/",
            "platform": "FastAPI Official Documentation",
            "type": "Documentation & Exercises",
            "estimated_hours": "6"
        },
        {
            "title": "Build REST APIs with FastAPI & Pydantic",
            "url": "https://realpython.com/fastapi-python-web-apis/",
            "platform": "Real Python",
            "type": "In-Depth Tutorial",
            "estimated_hours": "4"
        }
    ],
    "PostgreSQL": [
        {
            "title": "PostgreSQL Tutorial - The Complete Guide",
            "url": "https://www.postgresqltutorial.com/",
            "platform": "PostgreSQL Tutorial",
            "type": "Interactive Guide",
            "estimated_hours": "8"
        },
        {
            "title": "Supabase & Postgres Database Schema Best Practices",
            "url": "https://supabase.com/docs/guides/database",
            "platform": "Supabase Docs",
            "type": "Documentation",
            "estimated_hours": "3"
        }
    ],
    "Docker": [
        {
            "title": "Docker Getting Started Guide",
            "url": "https://docs.docker.com/get-started/",
            "platform": "Docker Official Docs",
            "type": "Hands-on Workshop",
            "estimated_hours": "5"
        }
    ],
    "React": [
        {
            "title": "React Official Documentation - Learn React",
            "url": "https://react.dev/learn",
            "platform": "React Official Docs",
            "type": "Interactive Guide",
            "estimated_hours": "10"
        }
    ],
    "Next.js": [
        {
            "title": "Next.js App Router Foundations",
            "url": "https://nextjs.org/learn",
            "platform": "Vercel Learn",
            "type": "Interactive Course",
            "estimated_hours": "8"
        }
    ],
    "TypeScript": [
        {
            "title": "TypeScript Handbook for JavaScript Developers",
            "url": "https://www.typescriptlang.org/docs/handbook/intro.html",
            "platform": "TypeScript Official Docs",
            "type": "Documentation",
            "estimated_hours": "6"
        }
    ],
    "Redis": [
        {
            "title": "Redis University - Fast-Track Course",
            "url": "https://redis.io/docs/latest/develop/get-started/",
            "platform": "Redis Official Docs",
            "type": "Quickstart Guide",
            "estimated_hours": "4"
        }
    ],
    "Machine Learning": [
        {
            "title": "Scikit-Learn Machine Learning in Python",
            "url": "https://scikit-learn.org/stable/tutorial/index.html",
            "platform": "Scikit-Learn Official Docs",
            "type": "Comprehensive Tutorial",
            "estimated_hours": "12"
        }
    ],
    "PyTorch": [
        {
            "title": "PyTorch Deep Learning 60 Minute Blitz",
            "url": "https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html",
            "platform": "PyTorch Official Docs",
            "type": "Interactive Notebook Tutorial",
            "estimated_hours": "5"
        }
    ]
}

# Curated portfolio projects mapped to target role categories and skills
CURATED_PORTFOLIO_PROJECTS: Dict[str, Dict[str, Any]] = {
    "Backend": {
        "title": "Microservice REST API with FastAPI, PostgreSQL & Redis",
        "description": "Design and build a scalable RESTful API handling authenticated resources, rate limiting with Redis cache, schema validation with Pydantic, and automated database migrations.",
        "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
        "deliverables": [
            "Complete CRUD endpoints with OpenAPI schema docs",
            "Database models with constraints and indexed foreign keys",
            "Automated pytest test suite with >80% code coverage",
            "Dockerfile and docker-compose.yml for local deployment"
        ]
    },
    "Frontend": {
        "title": "Responsive Analytics Dashboard with Next.js & Tailwind CSS",
        "description": "Build a modern web application consuming REST endpoints, with dynamic charts, dark/light theme, accessible forms, and optimistic UI updates.",
        "technologies": ["TypeScript", "React", "Next.js", "Tailwind CSS"],
        "deliverables": [
            "Modular component hierarchy with TypeScript interfaces",
            "Server-side rendering and client-side reactive components",
            "Mobile-responsive grid and WCAG accessible navigation"
        ]
    },
    "Data Science": {
        "title": "Predictive Customer Churn Pipeline & Dashboard",
        "description": "Clean, explore, and model a tabular customer dataset. Engineer predictive features, train baseline and ensemble classifiers in Scikit-Learn, and visualize model metrics.",
        "technologies": ["Python", "Pandas", "NumPy", "Scikit-Learn", "SQL"],
        "deliverables": [
            "Jupyter notebook demonstrating exploratory data analysis (EDA)",
            "Cross-validated classification model comparing F1 and ROC-AUC scores",
            "Summary business insights report with actionable findings"
        ]
    },
    "Machine Learning": {
        "title": "Semantic Document Search Engine using PyTorch & Embeddings",
        "description": "Build an end-to-end vector search application extracting dense text embeddings, performing cosine similarity ranking over document corpora, and deploying via FastAPI.",
        "technologies": ["Python", "PyTorch", "Natural Language Processing (NLP)", "FastAPI", "Docker"],
        "deliverables": [
            "Embedding pipeline with tokenization and batch inference",
            "Fast cosine retrieval API endpoint with benchmark latency stats",
            "Evaluation script measuring Precision@K and MRR on test queries"
        ]
    }
}

# Initial Demo Student Profile ("Alex Chen")
DEMO_STUDENT = {
    "id": "student_demo_01",
    "email": "alex.chen@university.edu",
    "full_name": "Alex Chen",
    "profile": {
        "headline": "Junior CS Student | Aspiring Backend & Systems Engineer",
        "education_degree": "Bachelor of Science",
        "education_major": "Computer Science",
        "graduation_year": 2026,
        "gpa": 3.75,
        "bio": "Enthusiastic computer science student passionate about backend software architecture, relational databases, and high-performance web APIs. Seeking a summer backend or systems engineering internship.",
        "location": "San Francisco, CA",
        "remote_preference": "flexible",
        "preferred_roles": ["Backend", "Full Stack"],
        "preferred_industries": ["Enterprise Tech", "FinTech", "SaaS"]
    },
    "skills": [
        {"skill_name": "Python", "proficiency_level": "intermediate", "provenance": "user_provided"},
        {"skill_name": "SQL", "proficiency_level": "intermediate", "provenance": "user_provided"},
        {"skill_name": "Git", "proficiency_level": "intermediate", "provenance": "user_provided"},
        {"skill_name": "Data Structures & Algorithms", "proficiency_level": "intermediate", "provenance": "user_provided"},
        {"skill_name": "HTML/CSS", "proficiency_level": "beginner", "provenance": "user_provided"},
        {"skill_name": "REST APIs", "proficiency_level": "beginner", "provenance": "user_provided"}
    ],
    "projects": [
        {
            "id": "proj_01",
            "title": "University Course Enrollment API",
            "description": "A RESTful course registration API built with Python, SQLite, and Flask. Supports student enrollment, course capacity enforcement, and search filtering.",
            "technologies": ["Python", "SQL", "REST APIs", "Git"],
            "github_url": "https://github.com/alexchen/course-api",
            "live_url": ""
        }
    ]
}
