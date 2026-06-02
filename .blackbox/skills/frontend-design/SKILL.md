---
name: frontend-design
description: Deterministic frontend design skill spec for building distinctive, non-generic user interfaces with explicit visual rationale, strict structure, and hard anti-slop guardrails.
---

# Frontend Design Next-Gen Spec

Use this file as the reusable prompt artifact for agents in this workspace. It captures the architectural direction, anti-slop constraints, and rollout plan in a form that can be loaded into an agent prompt later.

<architectural_teardown>
Deconstruct the core logic of the original tool. What is the fundamental mechanism it uses to solve its problem?

The original frontend-design skill is not a deterministic compiler. It is a prompt-driven steering layer that nudges a model toward distinctive UI output by combining a short trigger description with a long instruction body. Its core mechanism is instruction shaping: choose a visual direction, apply aesthetic heuristics, and ask the model to synthesize working frontend code that feels intentional.

Its strength is breadth. It can guide layout, typography, color, motion, and overall tone without needing a custom runtime. Its weakness is that the mechanism is still linguistic. The skill relies on the model following prose constraints rather than a stricter execution pipeline, so consistency depends on prompt quality and model compliance rather than enforced state.
</architectural_teardown>

<bottleneck_analysis>
Identify where this tool relies on "hope." Where does it use loose text parsing, single-dimensional evaluation metrics, or generic Markdown instead of mathematical constraints, rigid API boundaries, or AST-aware logic?

The weak points are all places where the skill assumes intent will be honored because it was stated clearly.

It relies on natural-language triggering, which makes both under-triggering and over-triggering possible.
It uses subjective phrases like bold, refined, memorable, and distinctive, which create direction but not measurable compliance.
It encodes anti-generic guidance as prose, so banned defaults can be reintroduced by a model that partially ignores the brief.
It does not validate the resulting DOM, CSS, or component graph against a constraint set.
It does not enforce palette roles, typography roles, motion roles, or layout topology through a schema.
It does not separate concept selection from generation in a way that can be audited.

The result is a skill that can strongly influence style, but cannot guarantee that the output is non-generic, structurally rich, and faithful to a chosen design identity.
</bottleneck_analysis>

<upgrade_protocol>
Propose a next-generation architecture. How do we replace its loose workflows with strict state machines? If it's a backend system, how do we structure it (e.g., highly optimized FastAPI polling logic, isolated execution environments)? If it's a frontend tool, how do we enforce dynamic, high-end styling constraints (vanilla JS/HTML5 combined with strict CSS variable matrices) to avoid generic UI output?

The upgraded design should behave like a stateful compiler for UI direction rather than a freeform prompt.

Use a strict state machine with these stages:
1. Brief intake and normalization.
2. Visual archetype selection from a bounded catalog.
3. Design rationale emission.
4. Token matrix compilation.
5. DOM skeleton generation.
6. CSS application.
7. Validation.
8. Repair or regeneration.
9. Finalization.

Each stage should require structured output before the next stage can begin. If a required field is missing, the system should halt and request completion instead of guessing.

For a frontend-oriented implementation, the generated artifact should be constrained by an explicit design contract:
- Use a typed token matrix for color, spacing, motion, radius, elevation, and typography.
- Require a non-trivial DOM hierarchy before styling begins.
- Treat the layout as named regions with explicit relationships, not a flat stack of cards.
- Separate concept selection from rendering so the visual direction can be audited before code is emitted.
- Run hard validation against banned defaults, contrast thresholds, palette roles, and layout richness.

Implement an anti-slop aesthetic guardrail. The system must formulate its visual identity, color theory, and structural constraints in a <design_rationale> block, explicitly banning common default libraries and pushing for complex, opinionated DOM structures before generating any CSS or HTML.

<design_rationale>
Visual identity: the brief must choose one explicit aesthetic family before output begins. The system should commit to a named direction such as editorial precision, industrial utility, luxury restraint, kinetic maximalism, or sculptural minimalism. The identity must define the intended emotional response and the single most memorable visual signature.

Color theory: the rationale must assign roles to background, surface, text, accent, emphasis, and warning colors. Every color token must have a purpose. The system should avoid default gradients and generic white-canvas dashboards unless the brief explicitly requests them.

Structural constraints: the design must define a layered DOM topology with named regions, secondary surfaces, and deliberate hierarchy. The layout should feel composed, not assembled from common dashboard blocks. The system should reject shallow grids that look like stock UI kits.

Forbidden defaults: explicitly ban generic system font stacks, overused product fonts, cookie-cutter card grids, framework-default component libraries, and bland purple-on-white aesthetics unless the user request specifically demands them.
</design_rationale>
</upgrade_protocol>

<execution_roadmap>
Break down the new architecture into 3 specific, verifiable development phases.

Phase 1: Define the contract.
Create the skill schema, the allowed aesthetic families, the design_rationale format, and the banned-default registry. Verification succeeds when the skill rejects incomplete briefs and every brief maps to a structured visual plan.

Phase 2: Build the compiler and validator.
Implement the deterministic pipeline that converts a brief into tokens, structure, and styling constraints. Verification succeeds when sample briefs produce structured outputs that pass hard checks for fonts, palettes, motion rules, and DOM depth.

Phase 3: Run evals and hardening.
Create realistic test prompts, score outputs against the constraint set, and iterate until the generated UIs are consistently distinctive and non-generic. Verification succeeds when repeated runs stay within the design contract while still producing visually varied results.
</execution_roadmap>
