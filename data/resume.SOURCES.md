# Unified resume source (`data/resume.json`)

Generated for MikeGPT (mcp-resume). Facts only — merged from existing files.

| Section | Primary source | Notes |
|---------|----------------|-------|
| `basics.label` | Plan target | Multi-domain headline |
| `basics.summary` | `rnd/resume/resume-product.json` | Product + Data + AWP + AIE_C |
| `basics.profiles` | `rnd/resume/resume-mike.json` | LinkedIn, GitHub, Medium, Spotify |
| `basics.phone`, `location`, `url` | `resume-mike.json` | |
| `work` | `resume-product.json` | ONE-FRONT entry from `resume-mike.json` (Product Engineer / AWP) |
| `skills` | Union product + mike | Includes Data Engineering, AI TECH LEAD, Agents & MCP |
| `certificates` | `mcp-resume/data/resume.json` (prior) | 37 entries |
| `references` | `resume-product.json` | name, position, relationship, date |
| `education`, `projects`, `volunteer`, `languages` | `resume-product.json` | |
| `meta.careerPillars` | Derived from merged facts | Four pillars for AI context |

Regenerate: `python scripts/merge_resume_sources.py` from repo root.
