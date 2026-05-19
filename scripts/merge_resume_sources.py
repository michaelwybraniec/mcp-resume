#!/usr/bin/env python3
"""One-off merge: rnd resume variants -> mcp-resume/data/resume.json (facts only)."""

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RND = Path(__file__).resolve().parents[2] / "rnd" / "resume"

product = json.loads((RND / "resume-product.json").read_text(encoding="utf-8"))
mike = json.loads((RND / "resume-mike.json").read_text(encoding="utf-8"))
mcp = json.loads((ROOT / "data" / "resume.json").read_text(encoding="utf-8"))

merged = copy.deepcopy(product)

# basics
merged["basics"]["label"] = (
    "Product Engineer · Software Architecture · Data & AI · AWP Creator · AIE_C"
)
merged["basics"]["summary"] = product["basics"]["summary"]
merged["basics"]["phone"] = mike["basics"].get("phone") or product["basics"].get("phone")
merged["basics"]["url"] = mike["basics"].get("url") or product["basics"].get("url")
merged["basics"]["location"] = mike["basics"].get("location") or product["basics"].get("location")
merged["basics"]["profiles"] = copy.deepcopy(mike["basics"]["profiles"])

# work: ONE-FRONT from mike (Product Engineer + AWP), rest from product
for i, w in enumerate(merged.get("work", [])):
    mike_work = next(
        (mw for mw in mike.get("work", []) if mw.get("name") == w.get("name")),
        None,
    )
    if mike_work and w.get("name") == "ONE-FRONT":
        merged["work"][i] = copy.deepcopy(mike_work)

# skills: union by name
def merge_skill_groups(base_list, extra_list):
    by_name = {s["name"]: copy.deepcopy(s) for s in base_list}
    for s in extra_list:
        name = s["name"]
        if name not in by_name:
            by_name[name] = copy.deepcopy(s)
            continue
        existing_kw = set(by_name[name].get("keywords", []))
        for kw in s.get("keywords", []):
            if kw not in existing_kw:
                by_name[name]["keywords"].append(kw)
    return list(by_name.values())

# Prefer product base; enrich from mike
merged["skills"] = merge_skill_groups(product.get("skills", []), mike.get("skills", []))
# Order: pillars first
priority = [
    "AI TECH LEAD",
    "AI, Agents & MCP Servers",
    "Data Engineering",
    "Core Expertise",
    "Languages & API Standards",
]
ordered = []
seen = set()
for pname in priority:
    for s in merged["skills"]:
        if s["name"] == pname and pname not in seen:
            ordered.append(s)
            seen.add(pname)
for s in merged["skills"]:
    if s["name"] not in seen:
        ordered.append(s)
        seen.add(s["name"])
merged["skills"] = ordered

# certificates from mcp (same 37, keep mcp order)
merged["certificates"] = copy.deepcopy(mcp.get("certificates", []))

# references from product (rich metadata)
merged["references"] = copy.deepcopy(product.get("references", []))

# carry other sections from product if present
for key in ("education", "projects", "volunteer", "awards", "publications", "interests"):
    if key in product and product[key]:
        merged[key] = copy.deepcopy(product[key])
    elif key in mcp and mcp.get(key):
        merged[key] = copy.deepcopy(mcp[key])

merged["languages"] = copy.deepcopy(
    product.get("languages") or mike.get("languages") or mcp.get("languages", [])
)

merged["meta"] = {
    "sourceVersion": "unified-2026-05",
    "sources": [
        "rnd/resume/resume-product.json (primary)",
        "rnd/resume/resume-mike.json (profiles, ONE-FRONT, skills)",
        "mcp-resume/data/resume.json (certificates)",
    ],
    "careerPillars": [
        {
            "id": "software_engineering",
            "title": "Software Engineering",
            "summary": (
                "Full-stack development and software architecture across Vue, React, Nuxt, "
                "Node.js, Laravel, and AWS. Roles include ONE-FRONT, SanteVet, Interpol/Ripjar, "
                "Lead Space, Hydrogen-Rempla, and earlier delivery roles."
            ),
        },
        {
            "id": "product",
            "title": "Product",
            "summary": (
                "Product Engineer work bridging discovery, backlog, stakeholders, and delivery. "
                "Cross-functional leadership at ONE-FRONT and SanteVet; product collaboration on "
                "Lead Space (pharma partnering platform)."
            ),
        },
        {
            "id": "data",
            "title": "Data Engineering & Analytics",
            "summary": (
                "Data analysis, pipelines, Elasticsearch/SQL graph tooling, BI and QuickBooks "
                "integrations, Calvin Klein & Tommy Hilfiger production planning, and co-development "
                "of the Universal Data Cleaning Pipeline with AIE_C (Barcelona)."
            ),
        },
        {
            "id": "ai",
            "title": "AI & Agentic Systems",
            "summary": (
                "MCP servers, LLM-integrated platforms, Agentic Workflow Protocol (AWP), AI Act "
                "compliance framing, and agentic development workflows. Open R&D at one-front.com/en/rnd."
            ),
        },
    ],
}

out = ROOT / "data" / "resume.json"
out.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Wrote {out}")
print("work[0] position:", merged["work"][0]["position"])
print("profiles:", len(merged["basics"]["profiles"]))
print("skills:", len(merged["skills"]))
print("certs:", len(merged["certificates"]))
print("refs:", len(merged["references"]))
