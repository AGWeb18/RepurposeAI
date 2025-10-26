# RepurposeAI

## Overview
RepurposeAI is a micro-SaaS concept designed for the 2025 creator economy. The platform transforms a single piece of long-form content—such as podcasts, videos, or blog posts—into dozens of channel-ready assets that are optimized for virality and tailored to each social platform.

## Why Now
- **Explosive creator growth:** By 2025 more than 50 million people earn a living as full-time creators, while short-form demand on platforms like YouTube and TikTok is compounding at 30% year over year.
- **Manual repurposing is a time sink:** Creators typically spend 10–15 hours every week repackaging content for different channels, leading to burnout or reliance on costly contractors.
- **Gap in multi-format tooling:** Despite the boom in AI assistants, very few tools preserve a creator's voice while generating multi-platform outputs such as TikTok clips, X threads, and LinkedIn carousels.

## Product Value
- Converts one long-form asset into dozens of ready-to-post derivatives.
- Preserves brand voice while optimizing each output for virality.
- Frees creators from repetitive editing, scripting, and formatting work.

## Market Opportunity
- AI-native content tools are expanding at roughly 40% annually as solopreneurs seek leverage without growing headcount.
- Indie makers on X highlight "long-form to shorts" automation as an accessible path to $5K MRR, and comparable products have already surpassed $10K MRR within months.
- Replaces $500–$2K per month agency fees with a scalable subscription.

## Business Model
- Subscription pricing between **$9–$29 per month** targets affordability for individual creators while supporting expansion into small teams.
- Retention is strong in this segment (estimated churn below 10%) because content repurposing is an ongoing need tied directly to revenue and audience growth.
- Achieving 500 subscribers positions RepurposeAI above **$10K in monthly recurring revenue** with organic referrals driven by improved creator output.

## Competitive Edge
- Focused on multi-format repurposing with voice consistency instead of one-off clip generators.
- Lightweight SaaS experience that matches the "AI agent" workflows creators already embrace.
- Automates the grunt work so creators can keep producing without burning out.

## Tech Stack Selection
- **Backend:** FastAPI with Pydantic for high-velocity API development and typed schemas.
- **Scheduling & Persistence:** In-memory evergreen calendar and content bank abstractions that can later plug into Redis/PostgreSQL.
- **Testing:** Pytest with FastAPI's TestClient for end-to-end flow validation.
- **Packaging:** Poetry-ready `pyproject.toml` simplifies dependency management and deployment to serverless containers.

## Sticky Feature Pillars
1. **Brand Voice Vault:** Creators can save multiple tone profiles that stamp every asset with consistent language.
2. **Evergreen Calendar:** Auto-schedules generated assets into an always-on queue, preventing feast-or-famine posting.
3. **Content Bank:** Archives summaries and tags for fast re-use across campaigns without re-uploading source material.
4. **Multi-Channel Blueprints:** Channel-aware templates deliver TikTok hooks, X threads, and LinkedIn carousels out of the box.

## Getting Started
1. Create a virtual environment and install dependencies (Poetry or `pip install -r requirements.txt` after exporting from Poetry).
2. Run the API locally: `uvicorn app.main:app --reload`.
3. Execute the test suite: `pytest`.
4. Explore API docs at `http://127.0.0.1:8000/docs` once the server is running.
