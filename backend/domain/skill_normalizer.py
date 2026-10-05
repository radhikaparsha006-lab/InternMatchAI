"""
Skill Normalization Service.
Resolves variants to canonical forms, extracts skills from unstructured text,
and classifies competencies by domain category.
"""

import re
from typing import List, Set, Dict, Any
from backend.domain.taxonomy import (
    get_canonical_skill, 
    get_skill_metadata, 
    ALIAS_TO_CANONICAL,
    SKILL_TAXONOMY
)

class SkillNormalizer:
    @staticmethod
    def normalize(skill_name: str) -> str:
        """
        Normalizes a skill name. If recognized in the taxonomy, returns
        its canonical name; otherwise returns a cleaned, title-cased representation.
        """
        if not skill_name:
            return ""
        canonical = get_canonical_skill(skill_name)
        if canonical:
            return canonical
        return skill_name.strip()

    @staticmethod
    def normalize_list(skills: List[str]) -> List[str]:
        """Normalizes a list of skills, deduplicating while preserving canonical order."""
        seen: Set[str] = set()
        normalized_result: List[str] = []
        for s in skills:
            norm = SkillNormalizer.normalize(s)
            if norm and norm.lower() not in seen:
                seen.add(norm.lower())
                normalized_result.append(norm)
        return normalized_result

    @staticmethod
    def extract_from_text(text: str) -> List[str]:
        """
        Extracts known canonical skills mentioned in unstructured text (e.g., resume, job description).
        Uses word-boundary aware phrase matching to avoid false positives (e.g. 'go' in 'good').
        """
        if not text:
            return []
        
        extracted: Set[str] = set()
        text_lower = text.lower()

        # Sort aliases by length descending so longer compound terms match first
        sorted_aliases = sorted(ALIAS_TO_CANONICAL.keys(), key=lambda x: len(x), reverse=True)

        for alias in sorted_aliases:
            # Word boundary regex, handling symbols like c++, c#, .js, etc.
            escaped_alias = re.escape(alias)
            # If the alias contains symbols, customize boundary
            if any(ch in alias for ch in "+#./"):
                pattern = rf"(?:^|[\s,;:(])({escaped_alias})(?:$|[\s,;:)])"
            else:
                pattern = rf"\b{escaped_alias}\b"

            if re.search(pattern, text_lower):
                canonical = ALIAS_TO_CANONICAL[alias]
                extracted.add(canonical)

        return sorted(list(extracted))

    @staticmethod
    def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
        """Groups a list of skills by their taxonomy category."""
        categories: Dict[str, List[str]] = {
            "Languages": [],
            "Frameworks": [],
            "Databases": [],
            "DevOps & Cloud": [],
            "Data & AI": [],
            "Software Engineering": [],
            "Soft Skills": [],
            "Other": []
        }

        for s in skills:
            meta = get_skill_metadata(s)
            if meta and meta.get("category") in categories:
                categories[meta["category"]].append(s)
            else:
                categories["Other"].append(s)

        return {k: v for k, v in categories.items() if v}
