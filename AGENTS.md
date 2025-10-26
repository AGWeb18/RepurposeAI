# RepurposeAI Agent Guidelines

## Scope
These guidelines apply to the entire repository.

## Architecture Principles
- Keep FastAPI endpoints thin; route orchestration only. Push business logic, heuristics, and data shaping into service modules under `app/services`.
- Service layers should stay framework-agnostic and pure-Python so that background workers or CLIs can reuse them without importing FastAPI.
- Prefer declarative, well-typed models. Use Pydantic models for external I/O surfaces and dataclasses (or typed functions) for internal helpers when that keeps logic clearer.
- When adding new channels or scheduling heuristics, update the relevant schemas, services, and evergreen calendar helpers together to maintain end-to-end flow coverage.

## Feature Expectations
- Optimise for "sticky" creator workflows: batching, evergreen scheduling, voice personalisation, and analytics hooks should remain first-class concerns.
- Add idempotent operations where possible (e.g., avoid double-scheduling, allow safe retries).
- Expose configuration flags via schemas instead of hard-coding values so that future UI or agent layers can toggle behaviours.

## Testing & Quality
- Provide unit coverage for new behaviours using the patterns in `tests/test_repurpose_flow.py`; keep tests deterministic and in-memory.
- If external dependencies are unavailable in CI, mark tests with skips and document the rationale in the test module docstring.
- Run `pytest` (or the most targeted subset) before opening a PR and include the exact command and status in the summary.

## Documentation & PRs
- Update `README.md` or create `docs/` notes when you introduce notable capabilities or workflow changes.
- PR descriptions should summarise customer-facing value first, then implementation details, and always include the test command matrix.
- Keep changelog-style bullets concise and outcome oriented.

Following these guardrails will help keep RepurposeAI focussed on automating creator repurposing with clarity and maintainability.
