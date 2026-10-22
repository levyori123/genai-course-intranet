# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Gen AI Course Intranet (Hebrew University)

Password-protected course info hub (syllabus, schedule, lecture materials, announcements, staff) for students, with staff editing content in Django admin. English only.

## Status
No code yet — the repo contains only this file. The agreed plan is in the Obsidian KB (`Gen AI Intranet/Roadmap.md`, `Architecture.md`, `Data Model.md`). Update this file with real commands and structure once the project is scaffolded.

## Planned stack (decided — see ADRs in the KB)
- Django + SQLite, server-rendered templates, single app `course`; project package `config`.
- No Node/JS build step (Node isn't installed): plain templates + one hand-written CSS file.
- Access: `SitePasswordMiddleware` gates everything behind a shared `SITE_PASSWORD` (session flag `site_access`); `/enter/`, `/admin/`, `/static/` and logged-in staff are exempt. Staff edit via `/admin` with personal accounts. Uploaded media is served through a gated view, never publicly.
- Staff-entered Markdown is rendered with `markdown` and sanitized with `nh3`.
- Config from env: `SECRET_KEY`, `SITE_PASSWORD`, `DEBUG`, `ALLOWED_HOSTS`. `whitenoise` + `gunicorn` for production.
- Python 3.15 is the installed interpreter; confirm the pinned Django supports it, otherwise use `py -3.13`.

Planned commands (once scaffolded): `python manage.py migrate`, `python manage.py seed_demo`, `python manage.py runserver`, `python manage.py test` (single test: `python manage.py test course.tests.test_middleware.SitePasswordTests.test_redirects_anonymous`).

## Workflow rules (from the project owner)
1. **Models:** plan with Opus 5.5 (`claude-opus-5-5`); execute/implement with Sonnet 5.5 (`claude-sonnet-5-5`), e.g. by delegating implementation to subagents with `model: sonnet`.
2. **Testing:** after finishing writing code, run tests on the new code **and** regression tests (the full suite).
3. **Security review:** after the tests pass, run a security review using the `security-review` skill.
4. **Commit:** at the end of every action that changes code, make a git commit.
5. **Document:** at the end of every agent run, record every update you made in Obsidian (see below).
6. **Git/GitHub:** the project is a git repo with a GitHub remote and two branches — `main` and `dev`. Do day-to-day work and commits on `dev`; `main` receives merges from `dev`.

Order after a code change: write code → tests + regression → `security-review` → commit (on `dev`) → Obsidian update.

## Knowledge base: Obsidian
The project's knowledge base lives in the Obsidian vault (`C:\dev\courses\course_projects_obsidian`, via the `obsidian` MCP server) under `Gen AI Intranet/`. Entry point: `Gen AI Intranet/00 Home.md`. Read it at the start of a session to pick up context.

Keep it current as you work — it is the source of truth for project context:
- **Every session with changes:** append to `Dev Log/YYYY-MM-DD.md` (what changed, why, what's next) and link it from `00 Home`.
- **Roadmap:** tick off / add items in `Roadmap.md`; update `status` and "Current status" in `00 Home`.
- **Decisions:** new significant choice → new `Decisions/ADR-NNN <title>.md` (context, decision, why, consequences).
- **Models/architecture changes:** update `Data Model.md` / `Architecture.md` to match the code.
- **Questions for the user:** add to `Open Questions.md`; tick when resolved.
- Bump the `updated:` frontmatter on notes you edit. Use `[[wikilinks]]` between notes.
