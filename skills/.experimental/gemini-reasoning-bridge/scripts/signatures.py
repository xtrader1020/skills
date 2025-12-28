"""
DSPy Signatures for Gemini Reasoning Bridge 2.0

This module defines the programmatic prompts for the Producer-Critic topology
using DSPy's signature system with explicit InputFields and OutputFields.
"""

import dspy


class EvidenceManager(dspy.Signature):
    """
    <role>You are the Evidence Manager (Gemini 3 Pro).</role>
    <instructions>
    1. Normalize raw source data into the EvidenceItem_v1 schema.
    2. Assign a SHA-256 text_hash to every artifact for versioning.
    3. Use 'Anchor & Pivot' for multimodal inputs: identify 14 anchor points in images before processing.
    </instructions>
    """
    raw_haystack = dspy.InputField(desc="The 2M token context window or research files.")
    normalized_evidence = dspy.OutputField(desc="List of EvidenceItem_v1 objects with stable IDs and hashes.")


class StructuralDrafter(dspy.Signature):
    """
    <role>You are the Structural Drafter.</role>
    <instructions>
    1. Synthesize the narrative based on normalized evidence.
    2. Output a SentenceRow_v1 trace map linking every claim to an evidence_id.
    3. MANDATE: Do not include claims without an EvidenceStore pinpoint.
    </instructions>
    """
    context = dspy.InputField(desc="Normalized EvidenceItems and project state.")
    draft_narrative = dspy.OutputField(desc="The generated text incorporating SentenceRow trace maps.")


class SocraticCritic(dspy.Signature):
    """
    <role>You are the Socratic Critic (GPT-5.2 Logic Governor).</role>
    <instructions>
    1. Execute a Logic Inversion pass (The Anti-Thesis Method) on the draft.
    2. Independently calculate the Claim-Citation Coverage (CCC) Metric: V / |U|.
    3. V = unique claims with valid source:page:line pinpoints.
    4. |U| = total factual assertions in draft.
    5. GATE: If CCC < 0.95, set audit_status to FAIL and trigger REVISE loop.
    </instructions>
    """
    claim_ledger = dspy.InputField(desc="The list of claims used by the Drafter.")
    sentence_map = dspy.InputField(desc="The SentenceRow_v1 trace map from the Drafter.")
    audit_report = dspy.OutputField(desc="AuditReport_v1 JSON containing binary status and coverage ratio.")


class ProgrammingAgent(dspy.Signature):
    """
    <role>You are the Sovereign Builder (Devstral-2/Qwen3 pair).</role>
    <instructions>
    1. HARD PROTOCOL: spec.md must be provided as input - no code generation without approved spec.
    2. Verify spec_hash matches the architecture_ledger before proceeding.
    3. Generate deterministic, zero-randomness code (temperature=0.0).
    4. Follow the "Spec-First" Protocol for all implementations.
    </instructions>
    """
    spec_md = dspy.InputField(desc="The approved specification document with verified spec_hash.")
    architecture_ledger = dspy.InputField(desc="The architectural decisions ledger for validation.")
    implementation_code = dspy.OutputField(desc="The generated code with full traceability to spec.")


class ContextGardener(dspy.Signature):
    """
    <role>You are the Context Gardener (Gemini 3 Pro Triage Agent).</role>
    <instructions>
    1. Rank evidence by Signal-to-Noise ratio before handoff to Drafter.
    2. Apply "Anchor & Pivot" methodology to identify key information points.
    3. Filter low-quality or redundant evidence to optimize context usage.
    4. Maintain evidence provenance for audit trail.
    </instructions>
    """
    raw_evidence_items = dspy.InputField(desc="Unranked evidence from Evidence Manager.")
    ranked_evidence = dspy.OutputField(desc="Signal-ranked evidence with quality scores and filtering metadata.")
