"""
ESCO and O*NET inspired standardized skills taxonomy, alias dictionary,
category classifications, and prerequisite relationships.
"""

from typing import Dict, List, Optional, Set

SKILL_TAXONOMY: Dict[str, dict] = {
    # --- Programming Languages ---
    "Python": {
        "category": "Languages",
        "aliases": ["python", "python3", "py", "python 3"],
        "description": "High-level programming language widely used in backend, data science, and AI.",
        "prerequisites": []
    },
    "JavaScript": {
        "category": "Languages",
        "aliases": ["javascript", "js", "ecmascript", "es6", "es2015"],
        "description": "Dynamic scripting language essential for modern web development.",
        "prerequisites": []
    },
    "TypeScript": {
        "category": "Languages",
        "aliases": ["typescript", "ts"],
        "description": "Typed superset of JavaScript providing static typing and scalability.",
        "prerequisites": ["JavaScript"]
    },
    "Java": {
        "category": "Languages",
        "aliases": ["java", "jdk", "jvm"],
        "description": "Class-based object-oriented programming language popular in enterprise backends.",
        "prerequisites": ["Object-Oriented Programming (OOP)"]
    },
    "C++": {
        "category": "Languages",
        "aliases": ["c++", "cpp", "cplusplus"],
        "description": "High-performance systems programming language.",
        "prerequisites": []
    },
    "SQL": {
        "category": "Languages",
        "aliases": ["sql", "structured query language", "ansi sql"],
        "description": "Domain-specific language for querying and managing relational databases.",
        "prerequisites": []
    },
    "Go": {
        "category": "Languages",
        "aliases": ["go", "golang"],
        "description": "Statically typed, compiled language developed by Google for concurrent services.",
        "prerequisites": []
    },

    # --- Frameworks & Libraries ---
    "React": {
        "category": "Frameworks",
        "aliases": ["react", "react.js", "reactjs"],
        "description": "Declarative component-based frontend library for web user interfaces.",
        "prerequisites": ["JavaScript", "HTML/CSS"]
    },
    "Next.js": {
        "category": "Frameworks",
        "aliases": ["next.js", "nextjs", "next"],
        "description": "React framework for server-side rendering, static site generation, and full-stack apps.",
        "prerequisites": ["React", "TypeScript"]
    },
    "FastAPI": {
        "category": "Frameworks",
        "aliases": ["fastapi", "fast-api"],
        "description": "Modern, high-performance Python web framework for building REST APIs with ASGI.",
        "prerequisites": ["Python", "REST APIs"]
    },
    "Node.js": {
        "category": "Frameworks",
        "aliases": ["node.js", "nodejs", "node"],
        "description": "V8 JavaScript runtime environment for building server-side applications.",
        "prerequisites": ["JavaScript"]
    },
    "Express.js": {
        "category": "Frameworks",
        "aliases": ["express", "express.js", "expressjs"],
        "description": "Minimal and flexible Node.js web application framework.",
        "prerequisites": ["Node.js"]
    },
    "Django": {
        "category": "Frameworks",
        "aliases": ["django", "django rest framework", "drf"],
        "description": "Batteries-included high-level Python web framework.",
        "prerequisites": ["Python", "SQL"]
    },
    "Tailwind CSS": {
        "category": "Frameworks",
        "aliases": ["tailwind", "tailwindcss", "tailwind-css"],
        "description": "Utility-first CSS framework for rapid UI styling.",
        "prerequisites": ["HTML/CSS"]
    },
    "HTML/CSS": {
        "category": "Frameworks",
        "aliases": ["html", "css", "html5", "css3", "html/css"],
        "description": "Foundational markup and styling languages of the World Wide Web.",
        "prerequisites": []
    },

    # --- Databases ---
    "PostgreSQL": {
        "category": "Databases",
        "aliases": ["postgresql", "postgres", "psql"],
        "description": "Powerful, open source object-relational database system.",
        "prerequisites": ["SQL"]
    },
    "MongoDB": {
        "category": "Databases",
        "aliases": ["mongodb", "mongo", "nosql"],
        "description": "Document-oriented NoSQL database used for high-volume unstructured storage.",
        "prerequisites": []
    },
    "Redis": {
        "category": "Databases",
        "aliases": ["redis", "in-memory cache", "key-value store"],
        "description": "In-memory data structure store used as a database, cache, and message broker.",
        "prerequisites": []
    },
    "Supabase": {
        "category": "Databases",
        "aliases": ["supabase"],
        "description": "Open source Firebase alternative built on PostgreSQL with Auth, Storage, and Realtime.",
        "prerequisites": ["PostgreSQL"]
    },

    # --- DevOps & Cloud ---
    "Docker": {
        "category": "DevOps & Cloud",
        "aliases": ["docker", "containerization", "containers", "dockerfile"],
        "description": "Platform for developing, shipping, and running applications in lightweight containers.",
        "prerequisites": []
    },
    "Git": {
        "category": "DevOps & Cloud",
        "aliases": ["git", "github", "gitlab", "version control", "vcs"],
        "description": "Distributed version control system for tracking changes in source code.",
        "prerequisites": []
    },
    "AWS": {
        "category": "DevOps & Cloud",
        "aliases": ["aws", "amazon web services", "s3", "ec2", "lambda"],
        "description": "Comprehensive cloud computing platform by Amazon.",
        "prerequisites": []
    },
    "CI/CD": {
        "category": "DevOps & Cloud",
        "aliases": ["ci/cd", "continuous integration", "github actions", "gitlab ci", "jenkins"],
        "description": "Automated pipeline for building, testing, and deploying software.",
        "prerequisites": ["Git"]
    },
    "Linux": {
        "category": "DevOps & Cloud",
        "aliases": ["linux", "bash", "unix", "shell scripting"],
        "description": "Open source operating system and command line scripting environment.",
        "prerequisites": []
    },

    # --- Data & AI ---
    "Machine Learning": {
        "category": "Data & AI",
        "aliases": ["machine learning", "ml", "statistical learning"],
        "description": "Subset of AI focused on training statistical models from data.",
        "prerequisites": ["Python", "Linear Algebra"]
    },
    "Pandas": {
        "category": "Data & AI",
        "aliases": ["pandas"],
        "description": "Fast, powerful Python data analysis and manipulation library.",
        "prerequisites": ["Python"]
    },
    "NumPy": {
        "category": "Data & AI",
        "aliases": ["numpy"],
        "description": "Fundamental package for scientific computing with Python.",
        "prerequisites": ["Python"]
    },
    "PyTorch": {
        "category": "Data & AI",
        "aliases": ["pytorch", "torch"],
        "description": "Optimized deep learning tensor library based on Python and Torch.",
        "prerequisites": ["Python", "Machine Learning"]
    },
    "TensorFlow": {
        "category": "Data & AI",
        "aliases": ["tensorflow", "tf", "keras"],
        "description": "End-to-end open source platform for machine learning.",
        "prerequisites": ["Python", "Machine Learning"]
    },
    "Scikit-Learn": {
        "category": "Data & AI",
        "aliases": ["scikit-learn", "sklearn"],
        "description": "Simple and efficient tools for predictive data analysis and machine learning in Python.",
        "prerequisites": ["Python", "NumPy"]
    },
    "Natural Language Processing (NLP)": {
        "category": "Data & AI",
        "aliases": ["nlp", "natural language processing", "text processing"],
        "description": "Branch of AI that gives computers the ability to understand text and spoken words.",
        "prerequisites": ["Machine Learning", "Python"]
    },

    # --- Software Engineering ---
    "REST APIs": {
        "category": "Software Engineering",
        "aliases": ["rest", "rest api", "restful", "rest apis", "api design"],
        "description": "Architectural style for designing networked web application interfaces.",
        "prerequisites": []
    },
    "Object-Oriented Programming (OOP)": {
        "category": "Software Engineering",
        "aliases": ["oop", "object-oriented programming", "object oriented"],
        "description": "Programming paradigm based on the concept of objects and classes.",
        "prerequisites": []
    },
    "Data Structures & Algorithms": {
        "category": "Software Engineering",
        "aliases": ["dsa", "data structures", "algorithms", "problem solving"],
        "description": "Fundamental principles of organizing data and implementing efficient procedures.",
        "prerequisites": []
    },
    "System Design": {
        "category": "Software Engineering",
        "aliases": ["system design", "distributed systems", "software architecture", "scalability"],
        "description": "Process of defining the architecture, components, and interfaces for scalable systems.",
        "prerequisites": ["REST APIs", "SQL"]
    },
    "Automated Testing": {
        "category": "Software Engineering",
        "aliases": ["testing", "unit testing", "pytest", "jest", "integration testing"],
        "description": "Practices and tools to write repeatable automated test suites.",
        "prerequisites": []
    },

    # --- Soft Skills ---
    "Communication": {
        "category": "Soft Skills",
        "aliases": ["communication", "verbal communication", "written communication", "presentation"],
        "description": "Effective conveyance of ideas, technical context, and project updates.",
        "prerequisites": []
    },
    "Team Collaboration": {
        "category": "Soft Skills",
        "aliases": ["teamwork", "collaboration", "cross-functional", "agile", "scrum"],
        "description": "Working constructively in team environments and agile ceremonies.",
        "prerequisites": []
    },
    "Critical Thinking": {
        "category": "Soft Skills",
        "aliases": ["critical thinking", "analytical thinking", "debugging mindset"],
        "description": "Objective analysis and evaluation of issues to form a reasoned judgment.",
        "prerequisites": []
    }
}

# Reverse index: lowercase alias -> canonical skill name
ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, meta in SKILL_TAXONOMY.items():
    ALIAS_TO_CANONICAL[canonical.lower()] = canonical
    for alias in meta["aliases"]:
        ALIAS_TO_CANONICAL[alias.lower()] = canonical

def get_canonical_skill(name: str) -> Optional[str]:
    """Resolves any variant, alias, or acronym to its canonical skill name."""
    if not name:
        return None
    cleaned = name.strip().lower()
    return ALIAS_TO_CANONICAL.get(cleaned, None)

def get_skill_metadata(canonical_name: str) -> Optional[dict]:
    """Returns category, description, and prerequisites for a canonical skill."""
    return SKILL_TAXONOMY.get(canonical_name)

def get_all_canonical_skills() -> List[str]:
    """Returns sorted list of all canonical skills in the taxonomy."""
    return sorted(list(SKILL_TAXONOMY.keys()))
