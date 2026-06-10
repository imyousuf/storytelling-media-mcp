# Stage Contracts

Use these contracts to spawn sub-agents for first-pass stage work. Sub-agents should not write outside their assigned stage directory unless explicitly instructed.

## Common Sub-Agent Prompt Requirements

Every sub-agent prompt should include:

- project path,
- source brief path,
- current stage number,
- exact files or directories it may write,
- expected output format,
- instruction not to revert or overwrite unrelated work,
- reminder that other agents may be working in parallel.

Use `explorer` agents for analysis-only passes. Use `worker` agents only when assigning disjoint files to write. If running in Codex with sub-agent tools, call `spawn_agent` for each independent first-pass role. Do not wait immediately unless the main task is blocked; continue any non-overlapping local setup, then synthesize completed outputs.

## Stage 1: Ingest & Normalize

### Structure Analyst

Role: identify the story's structure and convert the brief into durable schema fields.

Suggested prompt:

```text
Analyze the director's brief at <brief-path> for Stage 1 of the movie pipeline. You are responsible only for structure analysis. Do not edit files unless asked. Return: story spine, logline, chapter list, locations, central themes, production constraints, and missing information. Be concise but specific.
```

Expected output:

- story spine in 5-8 bullets,
- chapter table,
- missing data list,
- recommended schema fields.

### Character Anchor Analyst

Role: extract character continuity constraints.

Suggested prompt:

```text
Analyze the director's brief at <brief-path> for Stage 1 of the movie pipeline. You are responsible only for character anchoring. Do not edit files unless asked. Return a character table with role, voice, emotional function, visual continuity, key relationships, continuity risks, and portrayal anti-patterns. Be concise but specific.
```

Expected output:

- character table with role, voice, emotional function, visual continuity, relationships,
- conflict/chemistry notes,
- risks of inconsistent portrayal.

## Stage 1 Artifact Templates

### `brief_summary.md`

Use this structure:

```md
# Brief Summary

## Source
- Project:
- Primary brief:
- Stage:

## Story Spine

## Logline

## Core Themes

## Chapter Overview

## Character Anchors

## Location And Visual Anchors

## Production Constraints

## Main Assumptions
```

### `brief_structure.json`

Use this exact top-level schema. Use empty arrays or `null` where information is unavailable; do not invent certainty.

```json
{
  "title": "",
  "source_files": [],
  "logline": "",
  "story_spine": [],
  "themes": [],
  "characters": [
    {
      "name": "",
      "role": "",
      "rank_or_designation": "",
      "persona_traits": [],
      "voice": "",
      "visual_continuity": "",
      "emotional_function": "",
      "relationships": [],
      "portrayal_risks": []
    }
  ],
  "chapters": [
    {
      "number": 1,
      "title": "",
      "plot_points": [],
      "locations": [],
      "visual_palette": "",
      "emotional_movement": "",
      "continuity_anchors": []
    }
  ],
  "locations": [
    {
      "name": "",
      "type": "",
      "chapters": [],
      "visual_features": [],
      "environmental_mechanics": []
    }
  ],
  "visual_language": {
    "style_comps": [],
    "palette_rules": [],
    "camera_rules": [],
    "weather_rules": []
  },
  "language_protocol": [],
  "combat_constraints": [],
  "media_generation_constraints": [],
  "rights_and_sensitivity_flags": [],
  "open_questions": [],
  "approval_status": "draft"
}
```

### `open_questions.md`

Group questions by:

- Creative approvals
- Character details
- Research needs
- Rights/sensitivity
- Production/media-generation constraints

### `early_risks.md`

Record first-pass issues before Stage 2:

- copyrighted source-universe or adaptation-rights risks,
- real-world political, ethnic, or naming sensitivity,
- safety concerns around combat, weapons, drones, or operational tactics,
- likely factual checks,
- recommended mitigation.

### `approval_packet.md`

Use this structure:

```md
# Stage 1 Approval Packet

## Generated Files

## Key Decisions

## Recommended Direction

## Risks To Resolve

## Open Questions

## Approval Request
Please approve Stage 1 or provide revisions. I will not begin Stage 2 until you approve.
```

## Stage 2: Research & Sensitivity

### Geography & Culture Research Analyst

Role: ground locations, terrain, weather, language, and cultural details.

Expected output:

- authenticity notes by location,
- language/dialect handling notes,
- visual-environment details,
- research questions requiring verification.

### Sensitivity & Legal Analyst

Role: flag risks before writing scenes or generating media.

Expected output:

- copyrighted-source/franchise concerns,
- real-world political or ethnic sensitivity notes,
- defamation or naming risks,
- safety boundaries for tactical content,
- suggested fictionalization changes.

### Screenplay Discipline Planner

Role: convert research and sensitivity findings into enforceable screenplay-writing rules before chapter architecture.

Before producing this pass, read `screenplay-discipline.md`.

Expected output:

- scene contract fields required for Stage 3,
- POV and information-release rules,
- dialogue and language-tag discipline,
- action prose constraints,
- continuity ledger requirements,
- draft pass order,
- chapter architecture checks that must be satisfied before Stage 4.

## Stage 3: Chapter Architecture

### Chapter Architect

Role: turn the brief into a locked chapter design.

Expected output:

- chapter objective,
- emotional movement,
- conflict escalation,
- required character appearances,
- transition in/out,
- scene contract coverage,
- information-release and POV plan,
- approval questions.

### Visual Geography Analyst

Role: make locations usable for screenplay and media generation.

Expected output:

- location continuity map,
- weather/time-of-day plan,
- palette and camera behavior by chapter,
- repeated visual motifs.

## Stage 4: Screenplay Development

### Dialogue & Voice Analyst

Role: prepare dialogue rules before drafting.

Expected output:

- voice rules per character,
- sample safe dialogue snippets,
- language/subtitle labels,
- dialogue anti-patterns to avoid.

### Action & Scene Mechanics Analyst

Role: prepare cinematic action constraints.

Expected output:

- scene mechanics,
- non-superhero action constraints,
- weather/tactical realism notes,
- safety boundary notes for weapons, drones, and combat.

## Stage 5: Continuity & Tone Harmonization

### Continuity Auditor

Role: audit all approved stage artifacts or screenplay files.

Expected output:

- contradictions,
- missing setup/payoff,
- location/time continuity issues,
- wardrobe/prop continuity,
- required revisions.

### Tone Auditor

Role: ensure the film feels like the approved brief.

Expected output:

- tone drift,
- over-exposition,
- character voice breaks,
- melodrama or trope risk,
- recommended line/scene adjustments.

## Stage 6: Visual & Media Generation Plan

### Visual Prompt Planner

Role: create image prompt strategy for Nano Banana and character/location references.

Expected output:

- character reference prompt plan,
- location reference prompt plan,
- shot prompt schema,
- negative prompts,
- continuity controls.

### Video Assembly Planner

Role: plan Veo clips and stitching.

Expected output:

- clip list,
- per-clip prompt inputs,
- first/last-frame needs,
- duration and aspect ratio,
- audio notes,
- FFmpeg stitch order,
- known API or model constraints.
