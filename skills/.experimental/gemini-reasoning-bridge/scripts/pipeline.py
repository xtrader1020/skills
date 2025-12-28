"""
Gemini Reasoning Bridge 2.0 Pipeline

This module implements the modular, schema-first pipeline based on the
Hardened Legal Toolchain and Contractor Model. It orchestrates the flow
from raw data to verified, traceable output using the Producer-Critic topology.
"""

import json
import hashlib
from typing import List, Dict, Any
from dataclasses import dataclass
import yaml

import dspy

from signatures import (
    EvidenceManager,
    ContextGardener,
    StructuralDrafter,
    SocraticCritic,
    ProgrammingAgent
)


@dataclass
class PipelineConfig:
    """Configuration for the reasoning bridge pipeline."""
    
    def __init__(self, config_path: str = "config.yml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def get_node_config(self, node_name: str) -> Dict[str, Any]:
        """Get configuration for a specific node."""
        return self.config.get(node_name, {})


class ReasoningBridge:
    """
    Main orchestrator for the Gemini Reasoning Bridge 2.0 pipeline.
    
    Implements the Producer-Critic topology with persona isolation and
    the Zero-Hallucination Protocol enforced via the CCC Hard Gate.
    """
    
    def __init__(self, config_path: str = "config.yml"):
        self.config = PipelineConfig(config_path)
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all DSPy modules with appropriate configurations."""
        # Evidence Manager (Gemini 3 Pro)
        evidence_config = self.config.get_node_config('evidence_manager')
        self.evidence_manager = dspy.ChainOfThought(EvidenceManager)
        
        # Context Gardener (Gemini 3 Pro)
        gardener_config = self.config.get_node_config('context_gardener')
        self.context_gardener = dspy.ChainOfThought(ContextGardener)
        
        # Structural Drafter
        drafter_config = self.config.get_node_config('structural_drafter')
        self.drafter = dspy.ChainOfThought(StructuralDrafter)
        
        # Socratic Critic (GPT-5.2)
        critic_config = self.config.get_node_config('socratic_critic')
        self.critic = dspy.ChainOfThought(SocraticCritic)
        
        # Programming Agent (Qwen3)
        builder_config = self.config.get_node_config('sovereign_builder')
        self.builder = dspy.ChainOfThought(ProgrammingAgent)
    
    def _calculate_text_hash(self, content: str) -> str:
        """Calculate SHA-256 hash for content versioning."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _calculate_ccc_metric(self, claim_ledger: Dict, sentence_map: List[Dict]) -> Dict:
        """
        Calculate the Claim-Citation Coverage (CCC) Metric.
        
        CCC = V / |U|
        where V = claims with valid source:page:line pinpoints
              |U| = total factual assertions
        """
        total_claims = len([c for c in claim_ledger.get('claims', []) 
                           if c.get('claim_type') == 'factual'])
        
        valid_claims = len([c for c in claim_ledger.get('claims', [])
                           if c.get('claim_type') == 'factual' 
                           and c.get('has_valid_pinpoint', False)])
        
        ratio = valid_claims / total_claims if total_claims > 0 else 0.0
        
        return {
            'V': valid_claims,
            'U': total_claims,
            'ratio': ratio,
            'threshold': self.config.get_node_config('socratic_critic').get('ccc_threshold', 0.95)
        }
    
    def process_haystack(self, raw_haystack: str) -> Dict[str, Any]:
        """
        Process raw input through the complete pipeline.
        
        Pipeline stages:
        1. Evidence Manager: Normalize raw data
        2. Context Gardener: Rank and filter evidence
        3. Structural Drafter: Generate narrative with trace maps
        4. Socratic Critic: Audit and validate
        5. [Optional] Revision loop if audit fails
        
        Args:
            raw_haystack: Raw source data (up to 2M tokens)
        
        Returns:
            Complete pipeline output including audit report
        """
        # Stage 1: Evidence Manager
        print("Stage 1: Evidence Manager - Normalizing haystack...")
        evidence_result = self.evidence_manager(raw_haystack=raw_haystack)
        normalized_evidence = self._parse_evidence(evidence_result.normalized_evidence)
        
        # Stage 2: Context Gardener
        print("Stage 2: Context Gardener - Ranking evidence by signal-to-noise...")
        gardener_result = self.context_gardener(
            raw_evidence_items=json.dumps(normalized_evidence)
        )
        ranked_evidence = self._parse_evidence(gardener_result.ranked_evidence)
        
        # Stage 3: Structural Drafter
        print("Stage 3: Structural Drafter - Generating narrative...")
        draft_result = self.drafter(
            context=json.dumps({
                'evidence': ranked_evidence,
                'mandate': 'All claims must have evidence pinpoints'
            })
        )
        draft_data = self._parse_draft(draft_result.draft_narrative)
        
        # Stage 4: Socratic Critic with CCC Hard Gate
        print("Stage 4: Socratic Critic - Executing Logic Inversion...")
        max_revisions = self.config.config['pipeline']['max_revision_cycles']
        
        for revision_cycle in range(max_revisions):
            audit_result = self.critic(
                claim_ledger=json.dumps(draft_data['claim_ledger']),
                sentence_map=json.dumps(draft_data['sentence_map'])
            )
            audit_report = self._parse_audit_report(audit_result.audit_report)
            
            # Check CCC Hard Gate
            ccc_metric = self._calculate_ccc_metric(
                draft_data['claim_ledger'],
                draft_data['sentence_map']
            )
            
            if ccc_metric['ratio'] >= ccc_metric['threshold']:
                audit_report['audit_status'] = 'PASS'
                print(f"✓ CCC Gate PASSED: {ccc_metric['ratio']:.2%} >= {ccc_metric['threshold']:.0%}")
                break
            else:
                audit_report['audit_status'] = 'FAIL'
                print(f"✗ CCC Gate FAILED: {ccc_metric['ratio']:.2%} < {ccc_metric['threshold']:.0%}")
                
                if revision_cycle < max_revisions - 1:
                    print(f"  Triggering revision cycle {revision_cycle + 1}/{max_revisions}...")
                    # Revise draft based on audit guidance
                    draft_result = self._revise_draft(
                        draft_data,
                        audit_report,
                        ranked_evidence
                    )
                    draft_data = self._parse_draft(draft_result)
                else:
                    print(f"  Maximum revision cycles reached. Returning failed audit.")
            
            audit_report['ccc_metric'] = ccc_metric
        
        return {
            'evidence': ranked_evidence,
            'draft': draft_data,
            'audit_report': audit_report,
            'status': audit_report['audit_status']
        }
    
    def generate_code(self, spec_md: str, architecture_ledger: Dict) -> str:
        """
        Generate code using the Sovereign Builder with spec-first protocol.
        
        Args:
            spec_md: The approved specification document
            architecture_ledger: The architectural decisions ledger
        
        Returns:
            Generated implementation code
        """
        # Verify spec hash
        spec_hash = self._calculate_text_hash(spec_md)
        
        if not self._verify_spec_hash(spec_hash, architecture_ledger):
            raise ValueError(
                "Spec hash verification failed. "
                "Code generation blocked by Spec-First Protocol."
            )
        
        print("Sovereign Builder: Generating implementation...")
        result = self.builder(
            spec_md=spec_md,
            architecture_ledger=json.dumps(architecture_ledger)
        )
        
        return result.implementation_code
    
    def _verify_spec_hash(self, spec_hash: str, architecture_ledger: Dict) -> bool:
        """Verify spec hash against architecture ledger."""
        active_spec = architecture_ledger.get('active_spec', {})
        expected_hash = active_spec.get('spec_hash', '')
        return spec_hash == expected_hash
    
    def _parse_evidence(self, evidence_json: str) -> List[Dict]:
        """Parse evidence from JSON string."""
        try:
            return json.loads(evidence_json)
        except json.JSONDecodeError:
            # Fallback: treat as array with single item
            return [{'content': evidence_json}]
    
    def _parse_draft(self, draft_json: str) -> Dict:
        """Parse draft output from JSON string."""
        try:
            return json.loads(draft_json)
        except json.JSONDecodeError:
            # Fallback: create basic structure
            return {
                'narrative': draft_json,
                'sentence_map': [],
                'claim_ledger': {'claims': []}
            }
    
    def _parse_audit_report(self, audit_json: str) -> Dict:
        """Parse audit report from JSON string."""
        try:
            return json.loads(audit_json)
        except json.JSONDecodeError:
            return {'audit_status': 'FAIL', 'error': 'Invalid audit report format'}
    
    def _revise_draft(self, draft_data: Dict, audit_report: Dict, 
                     evidence: List[Dict]) -> str:
        """Revise draft based on audit feedback."""
        revision_context = {
            'evidence': evidence,
            'previous_draft': draft_data,
            'audit_feedback': audit_report.get('revision_guidance', []),
            'unsupported_claims': audit_report.get('logic_inversion_results', {})
                                           .get('unsupported_claims', [])
        }
        
        result = self.drafter(context=json.dumps(revision_context))
        return result.draft_narrative


def main():
    """Example usage of the Reasoning Bridge pipeline."""
    # Initialize pipeline
    bridge = ReasoningBridge("config.yml")
    
    # Example: Process research data
    haystack = """
    Research findings indicate that temperature affects model behavior.
    Study A (2024, page 42) found that temperature=1.0 increases diversity.
    Study B (2024, page 15) confirmed similar results with GPT models.
    """
    
    result = bridge.process_haystack(haystack)
    
    print("\n" + "="*60)
    print("PIPELINE RESULTS")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Evidence items: {len(result['evidence'])}")
    print(f"CCC Ratio: {result['audit_report'].get('ccc_metric', {}).get('ratio', 0):.2%}")
    print("\nAudit Report:")
    print(json.dumps(result['audit_report'], indent=2))


if __name__ == "__main__":
    main()
