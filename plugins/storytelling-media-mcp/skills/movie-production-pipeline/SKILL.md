---
name: movie-production-pipeline
description: "Iterative multi-agent workflow for turning a director's brief, movie bible, or chapter outline into structured movie production artifacts. Use when the user wants Codex to run staged agent-like movie development: brief ingestion, research, chapter structuring, screenplay drafting, continuity harmonization, visual prompt planning, Veo/Nano Banana generation planning, or iterative review gates before moving between stages."
---

# Movie Production Pipeline

Run a gated, multi-agent movie development workflow. The user owns creative approval. Do not move from one stage to the next until the user gives explicit approval such as "approved", "continue", "move on", or an equivalent instruction.

## Operating Rules

1. Start by locating the movie project directory and primary brief. If unclear, ask for the path.
2. Create or reuse `production/` inside the movie project for generated artifacts.
   - If an output file already exists, read it first and either update it intentionally or create a timestamped draft under the same stage directory. Never overwrite prior approved artifacts silently.
   - If the user asks for planning only or says not to edit files, return the stage plan and proposed artifact contents in the response without writing files.
3. Treat each stage as a review gate:
   - run the stage,
   - write artifacts,
   - summarize decisions and open questions,
   - ask for user feedback,
   - iterate until approved.
4. Use sub-agents for the first analytical pass of each stage when the user has explicitly asked for this skill or multi-agent execution and sub-agent tools are available. In Codex sessions with `spawn_agent`, use `explorer` for analysis-only passes and `worker` only for disjoint file-writing assignments. If sub-agent tools are unavailable, state that limitation and perform the first-pass roles locally.
5. Do not duplicate sub-agent work locally. Integrate their outputs, resolve conflicts, and mark assumptions.
6. Preserve rights and sensitivity concerns. Flag copyrighted source-universe issues, real-world political sensitivity, and procedural weaponization risk.
7. Keep generated tactical material cinematic and non-instructional. Avoid step-by-step weapon construction, drone weaponization procedures, or operational evasion instructions.
8. Prefer structured files over prose-only outputs.

## Stage Gates

Use these stages in order unless the user explicitly jumps to a later stage:

1. **Ingest & Normalize**
   - Inputs: director's brief, screenplay bible, existing notes.
   - Outputs: `production/01_ingest/brief_summary.md`, `brief_structure.json`, `open_questions.md`, `early_risks.md`, `approval_packet.md`.
   - Goal: identify story spine, character anchors, locations, themes, constraints, and missing data.

2. **Research & Sensitivity**
   - Outputs: `production/02_research/research_notes.md`, `sensitivity_notes.md`, `authenticity_checklist.md`.
   - Goal: ground geography, culture, language, production realism, and legal/sensitivity risks.

3. **Chapter Architecture**
   - Outputs: `production/03_chapters/chapters.json`, `chapter_beats.md`, `approval_packet.md`.
   - Goal: lock chapter-level purpose, emotional movement, visual palette, continuity anchors, and transition logic.

4. **Screenplay Development**
   - Outputs per approved chapter: `production/04_screenplay/chapter_##.md`, plus `dialogue_notes.md`.
   - Goal: draft cinematic scenes with language labels, character-specific voice, action constraints, and production-aware beats.

5. **Continuity & Tone Harmonization**
   - Outputs: `production/05_continuity/continuity_report.md`, `revision_plan.md`, updated screenplay files if approved.
   - Goal: audit character, geography, time, wardrobe, language, tactical realism, emotional flow, and visual continuity.

6. **Visual & Media Generation Plan**
   - Outputs: `production/06_visuals/character_refs.md`, `shot_prompts.json`, `video_manifest.json`, `stitch_plan.md`.
   - Goal: produce Nano Banana image prompts, Veo clip prompts, reference-image strategy, clip durations, and FFmpeg stitching plan.

## Sub-Agent Use

Read `references/stage-contracts.md` before spawning sub-agents. It defines each sub-agent's responsibility, prompt shape, expected output, and write restrictions.

Spawn sub-agents only for bounded first-pass work. Typical pattern:

- Stage 1: Structure Analyst + Character Anchor Analyst.
- Stage 2: Research Analyst + Sensitivity/Legal Analyst.
- Stage 3: Chapter Architect + Visual Geography Analyst.
- Stage 4: Dialogue/Voice Analyst + Action/Scene Analyst.
- Stage 5: Continuity Auditor + Tone Auditor.
- Stage 6: Visual Prompt Planner + Video Assembly Planner.

The main agent must synthesize all sub-agent output into one coherent approval packet.

## Feedback Loop

End every stage response with:

- generated files,
- key decisions,
- risks or unresolved questions,
- concrete recommendation,
- a direct request for approval or revision feedback.

Do not start the next stage in the same turn unless the user already approved that transition.

## Artifact Conventions

Use Markdown for human review and JSON for machine handoff. Use stable keys:

- `title`
- `logline`
- `characters`
- `chapters`
- `locations`
- `visual_language`
- `language_protocol`
- `constraints`
- `open_questions`
- `approval_status`

For exact Stage 1 schemas and templates, read `references/stage-contracts.md`.

When working inside a private movie project, do not push generated artifacts unless the user asks.
