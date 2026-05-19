"""
Resume data service for context retrieval and data processing
"""

import json
from difflib import SequenceMatcher
from typing import Dict, Any, List, Tuple
from services.fallback_resume import fallback_service
from services.resume_grounding import finalize_context, debug_log

_RECOMMENDATION_TARGETS = ("recommendation", "recommended", "recommends")


def _is_recommendation_word(word: str) -> bool:
    """Return True if a single word is a close enough match to any recommendation-related term."""
    if len(word) < 5:
        return False
    for target in _RECOMMENDATION_TARGETS:
        if SequenceMatcher(None, word, target).ratio() >= 0.62:
            return True
    return False


def _looks_like_recommendation_query(message_lower: str) -> bool:
    """Detect recommendation queries including severe typos (e.g. 'recmeneded')."""
    stems = ("recom", "recm", "reference", "endorsement", "testimonial")
    if any(s in message_lower for s in stems):
        return True
    return any(_is_recommendation_word(w) for w in message_lower.split())


class ResumeService:
    """Handles resume data retrieval and context generation"""

    @staticmethod
    def _format_recommendations(recs: List[Dict[str, Any]]) -> str:
        if not recs:
            return "No recommendations or references found in the resume."
        lines = [f"Recommendations and References — total: {len(recs)}\n"]
        for i, rec in enumerate(recs, 1):
            if isinstance(rec, str):
                lines.append(f"{i}. \"{rec.strip()}\"")
                continue
            text = rec.get("reference") or rec.get("text") or rec.get("content") or ""
            name = rec.get("name", "")
            position = rec.get("position", "")
            header = f"{i}. {name}" + (f" ({position})" if position else "")
            if text:
                lines.append(f"{header}\n   \"{text.strip()}\"")
            else:
                lines.append(header)
        return "\n\n".join(lines)

    @staticmethod
    def _format_certificates(certs: List[Dict[str, Any]]) -> str:
        if not certs:
            return "No certificates listed in the resume."
        lines = ["Professional Certificates:"]
        for cert in certs:
            name = cert.get("name", "")
            date = cert.get("date", "")
            url = cert.get("url", "")
            line = f"- {name}"
            if date:
                line += f" ({date})"
            if url:
                line += f" — {url}"
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _format_profiles(profiles: List[Dict[str, Any]], website: str = "") -> str:
        lines = ["Professional links and profiles:"]
        if website:
            lines.append(f"- Website: {website}")
        for p in profiles:
            network = p.get("network", "Profile")
            url = p.get("url", "")
            if url:
                lines.append(f"- {network}: {url}")
        return "\n".join(lines) if len(lines) > 1 else "No profile links found."

    @staticmethod
    def _format_career_pillars(pillars: List[Dict[str, Any]]) -> str:
        if not pillars:
            return ""
        lines = ["Career pillars:"]
        for pillar in pillars:
            title = pillar.get("title", "")
            summary = pillar.get("summary", "")
            if title and summary:
                lines.append(f"- **{title}**: {summary}")
        return "\n".join(lines)

    @staticmethod
    def _skill_keywords(skills: Dict[str, Any], *key_parts: str) -> List[str]:
        """Collect keywords from skill groups whose normalized key contains any part."""
        out: List[str] = []
        for key, vals in skills.items():
            if not isinstance(vals, list):
                continue
            if any(part in key for part in key_parts):
                out.extend(vals)
        return list(dict.fromkeys(out))

    @staticmethod
    def _format_skills_context(data: Dict[str, Any]) -> str:
        """Structured skills context so data/product/AI are visible to the LLM (not buried in JSON)."""
        skills = data.get("skills", {})
        lines = [
            "Skills overview (four domains — include all relevant areas in your answer):",
            "",
            ResumeService._format_career_pillars(data.get("career_pillars", [])),
            "",
            "### Data engineering & analytics",
            "Keywords: " + ", ".join(ResumeService._skill_keywords(skills, "data"))
            if ResumeService._skill_keywords(skills, "data")
            else "(see experience)",
        ]

        data_roles = []
        for exp in data.get("experience", []):
            blob = f"{exp.get('position', '')} {exp.get('description', '')}".lower()
            if any(
                t in blob
                for t in (
                    "data analyst",
                    "data analysis",
                    "elasticsearch",
                    "graph",
                    "quickbooks",
                    "bi",
                    "reporting",
                    "pipeline",
                    "etl",
                )
            ):
                data_roles.append(
                    f"- {exp.get('position')} @ {exp.get('company')}: "
                    f"{(exp.get('description') or '')[:220]}"
                )
        if data_roles:
            lines.extend(["", "Data-related experience:", *data_roles[:5]])

        sections = [
            (
                "### Software engineering (full-stack & architecture)",
                ResumeService._skill_keywords(
                    skills, "frontend", "backend", "core", "mobile", "languages"
                ),
            ),
            (
                "### Product & delivery",
                ResumeService._skill_keywords(skills, "project", "tech_lead"),
            ),
            (
                "### AI & agentic systems",
                ResumeService._skill_keywords(skills, "ai", "agent", "mcp"),
            ),
            (
                "### Cloud, DevOps, security & QA",
                ResumeService._skill_keywords(
                    skills, "serverless", "cloud", "devops", "security", "quality", "monitoring"
                ),
            ),
        ]
        for heading, keywords in sections:
            if keywords:
                lines.extend(["", heading, ", ".join(keywords[:30])])

        lines.extend(
            [
                "",
                "Instruction: Summarize only skills and experience listed above. "
                "Include data/analytics where listed (e.g. Calvin Klein, Interpol/Elasticsearch, "
                "BI/QuickBooks, AIE_C pipeline). Do not add technologies not named above.",
            ]
        )
        return "\n".join(lines)

    @staticmethod
    def _resolve_context(user_message: str, history: List[Dict] = None) -> Tuple[str, str]:
        """Return (context_body, route_name) before grounding footer."""
        message_lower = user_message.lower()
        data = fallback_service.get_full_resume()

        if any(word in message_lower for word in ["certificate", "certification", "credential"]):
            return ResumeService._format_certificates(data.get("certificates", [])), "certificates"

        if any(
            word in message_lower
            for word in ["link", "github", "linkedin", "website", "medium", "spotify", "profile link", "my links", "social"]
        ):
            personal = data.get("personal", {})
            return (
                ResumeService._format_profiles(
                    personal.get("profiles", []),
                    personal.get("website", ""),
                ),
                "profiles",
            )

        if any(
            word in message_lower
            for word in ["data", "analytics", "pipeline", "etl", "elasticsearch", "bi"]
        ):
            return ResumeService._data_engineering_context(data), "data"

        if any(
            word in message_lower
            for word in ["product", "awp", "agentic", "mcp", "ai act", "product engineer"]
        ):
            return ResumeService._product_ai_context(data), "product_ai"

        if any(word in message_lower for word in ["experience", "work", "job", "career"]):
            return (
                f"Work Experience:\n{json.dumps(fallback_service.get_experience(), indent=2)}",
                "experience",
            )

        if any(word in message_lower for word in ["skill", "technology", "programming", "tech"]):
            return ResumeService._format_skills_context(data), "skills"

        if any(word in message_lower for word in ["search", "find"]):
            words = message_lower.split()
            search_terms = [
                word
                for word in words
                if len(word) > 3 and word not in ["search", "find", "about", "with"]
            ]
            if search_terms:
                search_query = " ".join(search_terms[:3])
                results = fallback_service.search_resume(search_query)
                return f"Search Results:\n{json.dumps(results, indent=2)}", "search"

        if _looks_like_recommendation_query(message_lower):
            recs = data.get("recommendations", [])
            # If the user is asking specifically "who" recommended, return names-focused context
            name_phrases = ("who ", "list name", "name", "names", "show me", "précis", "precis")
            wants_names = any(p in message_lower for p in name_phrases)
            if wants_names:
                names = [
                    rec.get("name") for rec in recs if isinstance(rec, dict) and rec.get("name")
                ]
                if names:
                    return (
                        "Names of people who recommended Michael Wybraniec:\n"
                        + "\n".join(f"- {name}" for name in names),
                        "reference_names",
                    )
            return (
                ResumeService._format_recommendations(recs),
                "recommendations",
            )

        # No route matched the current message — check recent conversation for topic clues
        # so follow-up questions like "what did they say?" still get the right context.
        if history:
            recent_text = " ".join(
                m.get("content", "")
                for m in history[-6:]
                if m.get("role") in ("user", "assistant")
            ).lower()
            if _looks_like_recommendation_query(recent_text):
                recs = data.get("recommendations", [])
                return ResumeService._format_recommendations(recs), "recommendations"
            if any(w in recent_text for w in ["certificate", "certification", "credential"]):
                return ResumeService._format_certificates(data.get("certificates", [])), "certificates"
            if any(w in recent_text for w in ["experience", "work", "job", "career"]):
                return (
                    f"Work Experience:\n{json.dumps(fallback_service.get_experience(), indent=2)}",
                    "experience",
                )
            if any(w in recent_text for w in ["skill", "technology", "programming", "tech"]):
                return ResumeService._format_skills_context(data), "skills"

        return ResumeService._build_default_summary(data), "default"

    @staticmethod
    def _build_default_summary(data: Dict[str, Any]) -> str:
        personal = data.get("personal", {})
        name = personal.get("name", "Michael Wybraniec")
        title = personal.get("title", "")
        summary_text = personal.get("summary", "")

        pillars_block = ResumeService._format_career_pillars(data.get("career_pillars", []))
        experience = data.get("experience", [])
        recent_roles = ", ".join(
            f"{e.get('position', '')} @ {e.get('company', '')}"
            for e in experience[:3]
            if e.get("position")
        )

        profiles = personal.get("profiles", [])
        link_bits = [p.get("url") for p in profiles if p.get("url")][:4]
        if personal.get("website") and personal["website"] not in link_bits:
            link_bits.insert(0, personal["website"])
        links_line = ", ".join(link_bits) if link_bits else "see profile links section"

        cert_count = len(data.get("certificates", []))
        rec_count = len(data.get("recommendations", []))

        parts = [
            f"{name} — {title}",
            "",
            summary_text[:600] + ("..." if len(summary_text) > 600 else ""),
            "",
            pillars_block,
            "",
            f"Recent roles: {recent_roles}" if recent_roles else "",
            f"Profiles: {links_line}",
            f"Certificates on file: {cert_count} | Recommendations: {rec_count}",
            "",
            "Ask about: work experience, skills, certificates, recommendations, links, "
            "data/analytics, product/AWP, or AI/agentic work.",
        ]
        return "\n".join(p for p in parts if p)

    @staticmethod
    def _data_engineering_context(data: Dict[str, Any]) -> str:
        skills = data.get("skills", {})
        data_keywords = []
        for key, vals in skills.items():
            if any(
                term in key
                for term in ("data", "backend", "monitoring", "serverless", "languages")
            ):
                if isinstance(vals, list):
                    data_keywords.extend(vals[:12])

        data_roles = []
        for exp in data.get("experience", []):
            pos = (exp.get("position") or "").lower()
            desc = (exp.get("description") or "").lower()
            if any(
                t in pos or t in desc
                for t in ("data", "analyst", "elasticsearch", "bi", "graph", "quickbooks")
            ):
                data_roles.append(
                    f"{exp.get('position')} @ {exp.get('company')}: "
                    f"{exp.get('description', '')[:200]}"
                )

        pillars = ResumeService._format_career_pillars(data.get("career_pillars", []))
        return "\n\n".join(
            filter(
                None,
                [
                    "Data engineering & analytics context:",
                    pillars,
                    "Relevant roles:\n" + "\n".join(f"- {r}" for r in data_roles[:5])
                    if data_roles
                    else "",
                    "Related skills:\n"
                    + ", ".join(list(dict.fromkeys(data_keywords))[:25])
                    if data_keywords
                    else "",
                ],
            )
        )

    @staticmethod
    def _product_ai_context(data: Dict[str, Any]) -> str:
        skills = data.get("skills", {})
        product_skills = {}
        for key, vals in skills.items():
            if any(
                term in key
                for term in ("ai", "tech_lead", "project", "security", "compliance")
            ):
                product_skills[key] = vals

        one_front = next(
            (e for e in data.get("experience", []) if "ONE-FRONT" in (e.get("company") or "")),
            None,
        )
        blocks = [
            "Product & AI / agentic systems context:",
            ResumeService._format_career_pillars(data.get("career_pillars", [])),
            f"Skills:\n{json.dumps(product_skills, indent=2)}",
        ]
        if one_front:
            blocks.append(
                f"ONE-FRONT ({one_front.get('position')}):\n"
                f"{one_front.get('description', '')}\n"
                f"Highlights: {json.dumps(one_front.get('highlights', [])[:8], indent=2)}"
            )
        return "\n\n".join(blocks)

    @staticmethod
    def get_job_match_context() -> str:
        """Full skills + experience context for Smart Match job analysis."""
        data = fallback_service.get_full_resume()
        skills_block = ResumeService._format_skills_context(data)
        experience_block = f"Work Experience:\n{json.dumps(fallback_service.get_experience(), indent=2)}"
        body = f"{skills_block}\n\n---\n\n{experience_block}"
        from services.resume_grounding import finalize_context
        return finalize_context(body, "job_match", "job match analysis")

    @staticmethod
    def get_resume_context(user_message: str, history: List[Dict] = None) -> str:
        """Get relevant resume context based on user message using fallback service"""
        try:
            body, route = ResumeService._resolve_context(user_message, history=history)
            return finalize_context(body, route, user_message)
        except Exception as e:
            debug_log(
                "resume_service.py:get_resume_context",
                "context error",
                {"error": str(e)},
                "A",
            )
            return f"Error retrieving context: {str(e)}"

    @staticmethod
    def get_full_resume_data() -> Dict[str, Any]:
        """Get complete resume data"""
        return fallback_service.get_full_resume()

    @staticmethod
    def get_experience_data() -> Dict[str, Any]:
        """Get work experience data"""
        return fallback_service.get_experience()

    @staticmethod
    def get_skills_data() -> Dict[str, Any]:
        """Get skills data"""
        return fallback_service.get_skills()

    @staticmethod
    def search_resume_data(query: str) -> Dict[str, Any]:
        """Search resume data"""
        return fallback_service.search_resume(query)

    @staticmethod
    def get_recommendations_data() -> Dict[str, Any]:
        """Get recommendations data"""
        return fallback_service.get_recommendations()

    @staticmethod
    def get_certificates_data() -> Dict[str, Any]:
        """Get certificates data"""
        return fallback_service.get_certificates()

    @staticmethod
    def get_profiles_data() -> Dict[str, Any]:
        """Get profile links"""
        return fallback_service.get_profiles()
