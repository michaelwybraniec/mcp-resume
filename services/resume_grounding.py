"""Grounding helpers: keep MikeGPT answers tied to resume facts only."""

import json
import time
from typing import Any, Dict, List, Tuple

_DEBUG_LOG_PATH = "/Users/michaelwybraniec/Documents/GitHub/mcp-resume/.cursor/debug-e790a9.log"
_SESSION_ID = "e790a9"

# Often hallucinated when discussing "data engineering" — flag if absent from context
WATCH_TERMS = (
    "hadoop",
    "spark",
    "tableau",
    "databricks",
    "snowflake",
    "tensorflow",
    "pytorch",
    "keras",
)

GROUNDING_FOOTER = """
---
ACCURACY RULES (mandatory for your reply):
- Speak ONLY about Michael Wybraniec using the resume facts above.
- Do NOT invent technologies, employers, dates, certifications, projects, or quotes.
- Do NOT infer tools (e.g. Hadoop, Spark, Tableau) from job titles — only name tools listed above.
- If something is not in the resume context, say it is not listed in the resume; do not guess.
- Paraphrase is fine; fabrication is not allowed."""


def debug_log(
    location: str,
    message: str,
    data: Dict[str, Any],
    hypothesis_id: str,
    run_id: str = "pre-fix",
) -> None:
    # #region agent log
    try:
        with open(_DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "sessionId": _SESSION_ID,
                        "runId": run_id,
                        "hypothesisId": hypothesis_id,
                        "location": location,
                        "message": message,
                        "data": data,
                        "timestamp": int(time.time() * 1000),
                    }
                )
                + "\n"
            )
    except Exception:
        pass
    # #endregion


def finalize_context(context: str, route: str, user_message: str) -> str:
    """Append grounding footer and log context metadata."""
    ctx_lower = context.lower()
    watch_in_context = {t: t in ctx_lower for t in WATCH_TERMS}
    debug_log(
        "resume_grounding.py:finalize_context",
        "context prepared for LLM",
        {
            "route": route,
            "user_message_preview": user_message[:80],
            "context_chars": len(context),
            "watch_terms_in_context": watch_in_context,
        },
        "B",
    )
    return context + GROUNDING_FOOTER


def find_ungrounded_terms(response: str, context: str) -> List[str]:
    """Terms in response that are monitored and missing from context."""
    resp = response.lower()
    ctx = context.lower()
    return [t for t in WATCH_TERMS if t in resp and t not in ctx]


def audit_response(response: str, context: str, user_message: str) -> Dict[str, Any]:
    """Log suspected hallucinations for debug verification."""
    ungrounded = find_ungrounded_terms(response, context)
    debug_log(
        "resume_grounding.py:audit_response",
        "response audited for ungrounded terms",
        {
            "user_message_preview": user_message[:80],
            "response_chars": len(response),
            "ungrounded_terms": ungrounded,
            "likely_hallucination": bool(ungrounded),
        },
        "D",
    )
    return {"ungrounded_terms": ungrounded}
