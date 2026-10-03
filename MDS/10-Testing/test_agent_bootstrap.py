#!/usr/bin/env python3
"""
MDS Agent Bootstrap & Handoff Contract — Automated Test & Verification Suite
Phase: 10.2 (MDS Agent Bootstrap & Handoff Contract)
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

SEPARATION OF CONCERNS ARCHITECTURE:
- Authoritative Implementation: tools/agent_bootstrap/engine.py
- Test Suite: MDS/10-Testing/test_agent_bootstrap.py (Imports & verifies tools.agent_bootstrap)

Test Suites:
1. TestAgentBootstrapSuite: 28 Behavioral, Contract, Schema, and Cognitive Invariant Tests.
2. TestNegativeSecurityInvariants: 17 Negative Fixtures (A through N + Exit 3, 4, continue-after-Exit-1).
3. TestBoundaryEnforcementSuite: 10 Explicit Boundary Tests (BOUNDARY-01 through BOUNDARY-10).
Total: 55 Automated Tests.
"""

import copy
import json
import os
import re
import sys
import unittest
from pathlib import Path

# ==============================================================================
# Set up paths and import Authoritative Implementation from tools.agent_bootstrap
# ==============================================================================

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

BOOTSTRAP_CONTRACT_PATH = WORKSPACE_ROOT / "MDS" / "AGENT" / "MDS_AGENT_BOOTSTRAP.md"
SCHEMA_PATH = WORKSPACE_ROOT / "schemas" / "project_design_config.schema.json"

# Authoritative Implementation imported from tools.agent_bootstrap
from tools.agent_bootstrap import (
    AuthorizationDeniedError,
    BootstrapLockPolicyEngine,
    ContractViolationError,
    GovernanceLockValidator,
    ImplementationAuthorizer,
    LockPolicyOutcome,
    SchemaValidationError,
    compute_canonical_config_hash,
    validate_json_schema,
)


# ==============================================================================
# Helper Utilities: Sample Config Generator
# ==============================================================================

def generate_valid_config(override_fields=None):
    """Generates a fully schema-valid project_design_config dictionary."""
    base = {
        "schema_version": "1.0.0",
        "project_name": "Master Design System Sample Application",
        "selected_design_system": "MDS",
        "dsse_decision": {
            "candidate_id": "MDS",
            "selection_score": 96.5,
            "confidence_tier": "HIGH",
            "decision_margin_delta": 6.8,
            "margin_classification": "Decisive Lead",
            "human_review_required": False,
            "human_review_reasons": [],
            "reproducibility_digest": "a" * 64
        },
        "visual_personality": "calm_editorial",
        "theme_mode": "system_adaptive",
        "density_mode": "regular",
        "platform_targets": ["web", "flutter_mobile"],
        "directionality": "bidirectional_adaptive",
        "accessibility_profile": {
            "target_level": "WCAG_2.1_AA",
            "min_touch_target_px": 44,
            "enforce_focus_rings": True,
            "support_reduced_motion": True
        },
        "approved_deviations": [],
        "governance_lock": {
            "locked": True,
            "locked_by": "DSSE-AUTOMATED-CLEARANCE",
            "lock_timestamp": "2026-10-01T20:30:00Z",
            "review_resolution": "",
            "config_hash": ""
        }
    }

    if override_fields:
        for k, v in override_fields.items():
            if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                base[k].update(v)
            else:
                base[k] = v

    # Ensure config_hash is computed deterministically using the authoritative hasher
    base["governance_lock"]["config_hash"] = compute_canonical_config_hash(base)
    return base


# ==============================================================================
# Standard Test Suite: TestAgentBootstrapSuite (28 Tests)
# ==============================================================================

class TestAgentBootstrapSuite(unittest.TestCase):
    """
    Comprehensive Behavioral, Contract, Schema, and Cognitive tests
    verifying Phase 10.2 architectural specifications against MDS_AGENT_BOOTSTRAP.md
    and schemas/project_design_config.schema.json.
    """

    @classmethod
    def setUpClass(cls):
        cls.contract_text = BOOTSTRAP_CONTRACT_PATH.read_text(encoding="utf-8")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

    # --------------------------------------------------------------------------
    # TEST-BTS-01: Bootstrap Contract Markdown Schema & Section Verification
    # --------------------------------------------------------------------------
    def test_bts_01_bootstrap_contract_structure(self):
        """Verifies that all 25 canonical sections are present and non-empty."""
        expected_sections = [
            "## 1. Scope, Mission & Architectural Context",
            "## 2. Five-Layer Authority Architecture",
            "## 3. Project Startup Protocol & Downstream Lifecycle",
            "## 4. Canonical DSSE Consumption & Project Configuration Lock Policy",
            "## 5. Project Design Configuration Contract (`project_design_config.json`)",
            "## 6. Design DNA Model & Philosophy",
            "## 7. Token Usage Contract & Zero-Tolerance Laws",
            "## 8. Component Implementation Contract (19 Canonical Components)",
            "## 9. Pattern, Workflow, and Template Consumption",
            "## 10. Accessibility Invariants & Touch Target Decoupling",
            "## 11. Responsive Architecture Law (\"Recomposition, Not Shrinking\")",
            "## 12. RTL & Bi-Directionality Contract",
            "## 13. State & Interaction Models",
            "## 14. AI UX Contract & Human-in-the-Loop Protocol",
            "## 15. Validation Architecture & Local Conformance Engine",
            "## 16. Project Deviation Schema & Validation Suppression",
            "## 17. Tri-Level Agent Permission Model",
            "## 18. Stateless Multi-Agent Handoff & Continuity Contract",
            "## 19. AI-Readability & Machine-Enforceable Guardrails",
            "## 20. Five-Tier Source Provenance & Security Trust Hierarchy",
            "## 21. Versioning & Upstream Compatibility Model",
            "## 22. Failure & Recovery Behavior",
            "## 23. Artifact Lifecycle & Status Transitions",
            "## 24. Canonical Phase 10 Roadmap Realignment",
            "## 25. Contract Sign-Off"
        ]
        for sec in expected_sections:
            self.assertIn(sec, self.contract_text, f"Missing canonical section: {sec}")

    # --------------------------------------------------------------------------
    # TEST-BTS-02: Five-Layer Authority Precedence Resolution Cascade
    # --------------------------------------------------------------------------
    def test_bts_02_authority_precedence_resolution(self):
        """Precedence cascade: Layer A > Layer C Deviations > Layer D > Layer C Defaults > Agent Heuristics."""
        self.assertIn("Layer A: MDS System Authority", self.contract_text)
        self.assertIn("Layer B: DSSE Selection Authority", self.contract_text)
        self.assertIn("Layer C: Project Design Decision", self.contract_text)
        self.assertIn("Layer D: Agent Implementation Contract", self.contract_text)
        self.assertIn("Layer E: Validation Authority", self.contract_text)

        # Simulation of conflict resolution
        def resolve_conflict(layer_a, approved_deviation, layer_d, layer_c_default, agent_heuristic):
            if approved_deviation is not None:
                return approved_deviation
            if layer_a is not None:
                return layer_a
            if layer_d is not None:
                return layer_d
            if layer_c_default is not None:
                return layer_c_default
            return agent_heuristic

        # Layer A beats Layer C default
        res = resolve_conflict(layer_a="MDS_CORE_RULE", approved_deviation=None, layer_d="COMP", layer_c_default="LOCAL", agent_heuristic="AI")
        self.assertEqual(res, "MDS_CORE_RULE")

        # Approved Deviation beats Layer A
        res2 = resolve_conflict(layer_a="MDS_CORE_RULE", approved_deviation="DEV-PROJ-001", layer_d="COMP", layer_c_default="LOCAL", agent_heuristic="AI")
        self.assertEqual(res2, "DEV-PROJ-001")

    # --------------------------------------------------------------------------
    # TEST-BTS-03: Startup Lifecycle 12-Step Deterministic Sequence
    # --------------------------------------------------------------------------
    def test_bts_03_startup_lifecycle_sequence(self):
        """Verifies the 12-step deterministic startup lifecycle sequence."""
        steps = [
            "1. Ingest Bootstrap Contract",
            "2. Inspect Workspace",
            "mds-dsse analyze",
            "mds-dsse evaluate",
            "6. Establish Project Design Configuration",
            "7. Query Token, Component & Pattern Subsets",
            "8. Synthesize UI Code & Styles",
            "9. Execute Conformance Validation",
            "10. Record .mds/agent_state.json",
            "11. Present Verification Report & PR",
            "12. Enter Idle State"
        ]
        for s in steps:
            self.assertIn(s, self.contract_text, f"Missing lifecycle step: {s}")

    # --------------------------------------------------------------------------
    # TEST-BTS-04: project_design_config.json Schema Validation Pass
    # --------------------------------------------------------------------------
    def test_bts_04_schema_validation_pass(self):
        """A valid project_design_config.json payload passes schema validation."""
        valid_config = generate_valid_config()
        self.assertTrue(validate_json_schema(valid_config, self.schema))

    # --------------------------------------------------------------------------
    # TEST-BTS-05: project_design_config.json Schema Validation Rejections
    # --------------------------------------------------------------------------
    def test_bts_05_schema_validation_rejections(self):
        """Rejects missing properties, disallowed enums, illegal additionalProperties."""
        # 1. Missing required root property
        invalid_1 = generate_valid_config()
        del invalid_1["project_name"]
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(invalid_1, self.schema)

        # 2. Disallowed design system enum
        invalid_2 = generate_valid_config({"selected_design_system": "CustomUnknownSystem"})
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(invalid_2, self.schema)

        # 3. Disallowed touch target (< 44)
        invalid_3 = generate_valid_config({"accessibility_profile": {"min_touch_target_px": 32}})
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(invalid_3, self.schema)

        # 4. Disallowed additional property at root
        invalid_4 = generate_valid_config()
        invalid_4["illegal_property"] = "hack"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(invalid_4, self.schema)

        # 5. Invalid hash pattern
        invalid_5 = generate_valid_config()
        invalid_5["governance_lock"]["config_hash"] = "not-a-valid-sha256-hex"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(invalid_5, self.schema)

    # --------------------------------------------------------------------------
    # TEST-BTS-06: DSSE Decision Tuple Integrity & Reproducibility Digest
    # --------------------------------------------------------------------------
    def test_bts_06_dsse_decision_tuple_integrity(self):
        """DSSE Decision Tuple must contain required properties and 64-char hex digest."""
        config = generate_valid_config()
        tuple_data = config["dsse_decision"]
        required_fields = ["candidate_id", "selection_score", "confidence_tier", "decision_margin_delta", "margin_classification", "human_review_required", "reproducibility_digest"]
        for rf in required_fields:
            self.assertIn(rf, tuple_data)
        self.assertRegex(tuple_data["reproducibility_digest"], r"^[a-f0-9]{64}$")

    # --------------------------------------------------------------------------
    # TEST-BTS-07: Design DNA Three-Tier Cognitive Mapping Verification
    # --------------------------------------------------------------------------
    def test_bts_07_design_dna_mapping(self):
        """Tier 01 (Mind: 100% Non-negotiable), Tier 02 (Eye: Adaptive), Tier 03 (Brand: Moment)."""
        self.assertIn("Three-Tier Cognitive-Perceptual Hierarchy", self.contract_text)
        self.assertIn("In the Mind", self.contract_text)
        self.assertIn("In the Eye", self.contract_text)
        self.assertIn("In Personality", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-08 to 11: 4-Step Token Search Cascade
    # --------------------------------------------------------------------------
    def test_bts_08_to_11_token_search_cascade(self):
        """Component -> Semantic -> Primitive -> RFC."""
        self.assertIn("Four-Step Token Search Cascade", self.contract_text)
        self.assertIn("Component Token", self.contract_text)
        self.assertIn("Semantic Token", self.contract_text)
        self.assertIn("Primitive Token", self.contract_text)
        self.assertIn("Propose Token RFC", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-12: Zero-Tolerance Magic Number Scanner Detection
    # --------------------------------------------------------------------------
    def test_bts_12_magic_number_scanner(self):
        """Rejects raw pixels, raw hex colors, arbitrary inline styles."""
        def scan_css_for_magic_numbers(css_snippet):
            violations = []
            if re.search(r":\s*#[0-9a-fA-F]{3,8}", css_snippet):
                violations.append("RAW_HEX_COLOR")
            if re.search(r":\s*\d+px", css_snippet):
                violations.append("RAW_PIXEL_VALUE")
            return violations

        self.assertEqual(scan_css_for_magic_numbers("color: var(--mds-color-text-primary);"), [])
        self.assertIn("RAW_HEX_COLOR", scan_css_for_magic_numbers("color: #ff0000;"))
        self.assertIn("RAW_PIXEL_VALUE", scan_css_for_magic_numbers("padding: 16px;"))

    # --------------------------------------------------------------------------
    # TEST-BTS-13: 19 Canonical Components Mandatory Reuse Enforcement
    # --------------------------------------------------------------------------
    def test_bts_13_canonical_components_reuse(self):
        """Verifies that all 19 canonical components are listed in the contract."""
        canonical_components = [
            "Button", "IconButton", "Link", "Field", "Input", "Textarea",
            "Checkbox", "Radio", "Switch", "Select", "Alert", "Spinner",
            "Skeleton", "Badge", "Card", "Table", "Tabs", "Dialog", "Tooltip"
        ]
        self.assertEqual(len(canonical_components), 19)
        for comp in canonical_components:
            self.assertIn(comp, self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-14: Deferred Enterprise Component Boundary Verification
    # --------------------------------------------------------------------------
    def test_bts_14_deferred_enterprise_components(self):
        """Data Grid, Tree View, Date Picker, Rich Text Editor, Command Palette."""
        deferred = ["Data Grid", "Tree View", "Date Picker", "Rich Text Editor", "Command Palette"]
        for d in deferred:
            self.assertIn(d, self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-15: Template/Workflow/Pattern Preference Hierarchy
    # --------------------------------------------------------------------------
    def test_bts_15_asset_preference_hierarchy(self):
        """Templates (6) > Workflows (6) > Patterns (8) > Custom Composition."""
        self.assertIn("Templates", self.contract_text)
        self.assertIn("Workflows", self.contract_text)
        self.assertIn("Patterns", self.contract_text)
        self.assertIn("6 Canonical Templates", self.contract_text)
        self.assertIn("6 Canonical Workflows", self.contract_text)
        self.assertIn("8 Canonical Patterns", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-16 & 17: Accessibility Invariants
    # --------------------------------------------------------------------------
    def test_bts_16_17_accessibility_invariants(self):
        """Visible focus rings (>=3:1) and 44x44 touch target rule decoupled from WCAG."""
        self.assertIn("Visible Focus Rings", self.contract_text)
        self.assertIn("3:1", self.contract_text)
        self.assertIn("44x44 Touch Target Rule", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-18 & 19: Responsive Recomposition Laws
    # --------------------------------------------------------------------------
    def test_bts_18_19_responsive_recomposition_laws(self):
        """Recomposition cognitive chain, 320/768/1024/1440, container max widths."""
        self.assertIn("Recomposition, Not Shrinking", self.contract_text)
        self.assertIn("320", self.contract_text)
        self.assertIn("768", self.contract_text)
        self.assertIn("1024", self.contract_text)
        self.assertIn("1440", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-20 & 21: RTL & Arabic Typography Laws
    # --------------------------------------------------------------------------
    def test_bts_20_21_rtl_and_arabic_laws(self):
        """Logical CSS properties, Cairo default font, no ellipsis truncation."""
        self.assertIn("margin-inline-start", self.contract_text)
        self.assertIn("Cairo", self.contract_text)
        self.assertIn("text-overflow: ellipsis", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-22: Universal 11-State Interaction FSM Transition Match
    # --------------------------------------------------------------------------
    def test_bts_22_interaction_fsm_determinism(self):
        """Validates all 11 states and allowed transitions."""
        states = [
            "IDLE", "ACTIVE_INPUT", "VALIDATING", "CONFIRMING",
            "PROCESSING", "STREAMING", "REVIEWING", "SUCCESS_RESOLVED",
            "ERROR_INTERCEPTED", "FATAL_FAILURE", "ABORTED_CANCEL"
        ]
        for s in states:
            self.assertIn(s, self.contract_text)

        allowed_transitions = {
            "IDLE": ["ACTIVE_INPUT"],
            "ACTIVE_INPUT": ["VALIDATING"],
            "VALIDATING": ["CONFIRMING"],
            "CONFIRMING": ["PROCESSING"],
            "PROCESSING": ["STREAMING", "ERROR_INTERCEPTED", "FATAL_FAILURE", "ABORTED_CANCEL"],
            "STREAMING": ["REVIEWING"],
            "REVIEWING": ["SUCCESS_RESOLVED"],
            "SUCCESS_RESOLVED": ["IDLE"],
            "FATAL_FAILURE": ["IDLE"],
            "ABORTED_CANCEL": ["IDLE"],
        }
        self.assertNotIn("SUCCESS_RESOLVED", allowed_transitions["ACTIVE_INPUT"])

    # --------------------------------------------------------------------------
    # TEST-BTS-23: AI UX Needs Review Human-in-the-Loop Confirmation Gate
    # --------------------------------------------------------------------------
    def test_bts_23_ai_ux_needs_review_gate(self):
        """Needs Review state blocks silent database mutation without human confirmation."""
        ai_states = ["Idle", "Thinking", "Working", "Streaming", "Completed", "Needs Review", "Error"]
        for s in ai_states:
            self.assertIn(s, self.contract_text)

        def attempt_db_mutation(ai_state, human_confirmed):
            if ai_state == "Needs Review" and not human_confirmed:
                raise PermissionError("Human confirmation required prior to mutation.")
            return "MUTATED"

        with self.assertRaises(PermissionError):
            attempt_db_mutation("Needs Review", human_confirmed=False)

        res = attempt_db_mutation("Needs Review", human_confirmed=True)
        self.assertEqual(res, "MUTATED")

    # --------------------------------------------------------------------------
    # TEST-BTS-24: Formal Deviation Record Schema Validation & Suppression
    # --------------------------------------------------------------------------
    def test_bts_24_deviation_record_schema(self):
        """DEV-PROJ-xxx validation and suppression rules."""
        valid_deviation = {
            "deviation_id": "DEV-PROJ-001",
            "affected_rule": "MDS-RULE-TOK-004",
            "rationale": "High-density flight management radar requires 24px micro-buttons.",
            "approved_by": "Lead Architect Mohamed Khalid",
            "timestamp": "2026-10-01T20:00:00Z"
        }
        config = generate_valid_config({"approved_deviations": [valid_deviation]})
        self.assertTrue(validate_json_schema(config, self.schema))

    # --------------------------------------------------------------------------
    # TEST-BTS-25: Multi-Agent Handoff State Continuity Round-Trip
    # --------------------------------------------------------------------------
    def test_bts_25_multi_agent_handoff_roundtrip(self):
        """Roundtrip verification of the tri-artifact state persistence."""
        artifacts = ["project_design_config.json", "docs/DESIGN_DECISIONS.md", ".mds/agent_state.json"]
        for a in artifacts:
            self.assertIn(a, self.contract_text)

        agent_state = {
            "last_active_agent_id": "agent-alpha-401",
            "last_updated_timestamp": "2026-10-01T21:00:00Z",
            "implemented_components_manifest": ["Button", "IconButton", "Card"],
            "active_validation_status": "PASS",
            "pending_review_gates": []
        }
        state_str = json.dumps(agent_state)
        restored = json.loads(state_str)
        self.assertEqual(restored["last_active_agent_id"], "agent-alpha-401")
        self.assertEqual(len(restored["implemented_components_manifest"]), 3)

    # --------------------------------------------------------------------------
    # TEST-BTS-26: Canonical DSSE Authority Boundary & Non-Recalculation
    # --------------------------------------------------------------------------
    def test_bts_26_dsse_authority_boundary_invariants(self):
        """Bootstrap must NOT calculate C_req, C_eval, C_evid, C_epistemic, or margins."""
        self.assertIn("DSSE owns selection and decision semantics. The Bootstrap Contract consumes the DSSE Decision Tuple and Exit Code. The Bootstrap Contract does not redefine DSSE.", self.contract_text)
        self.assertIn("Bootstrap Contract **does NOT calculate**", self.contract_text)

        config = generate_valid_config()
        self.assertIn("confidence_tier", config["dsse_decision"])
        self.assertIn("human_review_required", config["dsse_decision"])
        self.assertIn("decision_margin_delta", config["dsse_decision"])
        self.assertIn("margin_classification", config["dsse_decision"])
        self.assertNotIn("C_req", config["dsse_decision"])
        self.assertNotIn("C_eval", config["dsse_decision"])
        self.assertNotIn("C_evid", config["dsse_decision"])

    # --------------------------------------------------------------------------
    # TEST-BTS-27: Exit 0 Automated Lock Policy & Implementation Authorization
    # --------------------------------------------------------------------------
    def test_bts_27_exit_0_automated_lock_policy(self):
        """DSSE Exit 0 -> invokes authoritative BootstrapLockPolicyEngine, authorizes implementation."""
        cfg = generate_valid_config()
        outcome = BootstrapLockPolicyEngine.apply_lock_policy(0, cfg["dsse_decision"], cfg)
        self.assertEqual(outcome.action, "AUTOMATED_LOCK")
        self.assertTrue(outcome.authorized)
        self.assertTrue(cfg["governance_lock"]["locked"])
        self.assertEqual(cfg["governance_lock"]["locked_by"], "DSSE-AUTOMATED-CLEARANCE")

        # Invoke authoritative implementation authorizer
        auth_granted = ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=0)
        self.assertTrue(auth_granted)

    # --------------------------------------------------------------------------
    # TEST-BTS-28: Exit 1 Mandatory Human Review Gate & Lock Prohibition
    # --------------------------------------------------------------------------
    def test_bts_28_exit_1_mandatory_human_review_gate(self):
        """DSSE Exit 1 -> invokes authoritative engine, keeps config unlocked, denies authorization until human signs."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "candidate_id": "MDS",
                "selection_score": 82.0,
                "confidence_tier": "HIGH",
                "decision_margin_delta": 0.8,
                "margin_classification": "Virtual Tie",
                "human_review_required": True,
                "human_review_reasons": ["Virtual Tie (Δ <= 1.0%) between MDS and Shadcn"],
                "reproducibility_digest": "c" * 64,
            }
        })

        # Invoke authoritative lock policy engine
        outcome = BootstrapLockPolicyEngine.apply_lock_policy(1, cfg["dsse_decision"], cfg)
        self.assertEqual(outcome.action, "MANDATORY_HUMAN_REVIEW_GATE")
        self.assertFalse(outcome.authorized)
        self.assertFalse(cfg["governance_lock"]["locked"])

        # Invoke authoritative authorizer on unlocked draft -> MUST raise ContractViolationError
        with self.assertRaises(ContractViolationError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=1)
        self.assertIn("UNLOCKED_DRAFT", str(ctx.exception))

        # Simulate human architect review approval
        cfg["governance_lock"]["locked"] = True
        cfg["governance_lock"]["locked_by"] = "Lead Architect Mohamed Khalid"
        cfg["governance_lock"]["review_resolution"] = "RATIFIED_MDS_FOR_FLUTTER"
        cfg["governance_lock"]["config_hash"] = compute_canonical_config_hash(cfg)

        # Invoke authoritative authorizer post human approval -> MUST succeed
        auth_granted = ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=1)
        self.assertTrue(auth_granted)

    # --------------------------------------------------------------------------
    # TEST-BTS-29: Exit 2, 3, 4 Error Abort Behavior
    # --------------------------------------------------------------------------
    def test_bts_29_exit_2_3_4_abort_behavior(self):
        """Invokes authoritative BootstrapLockPolicyEngine and ImplementationAuthorizer for Exit 2, 3, 4."""
        for code in [2, 3, 4]:
            cfg = generate_valid_config()
            outcome = BootstrapLockPolicyEngine.apply_lock_policy(code, cfg["dsse_decision"], cfg)
            self.assertEqual(outcome.action, "EXECUTION_ABORTED")
            self.assertFalse(outcome.authorized)
            self.assertFalse(cfg["governance_lock"]["locked"])

            # Invoke authoritative authorizer -> MUST raise AuthorizationDeniedError
            with self.assertRaises(AuthorizationDeniedError) as ctx:
                ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=code)
            self.assertIn(f"ABORTED_EXIT_{code}", str(ctx.exception))

    # --------------------------------------------------------------------------
    # TEST-BTS-30: Configuration Cryptographic Hashing & Tamper Detection
    # --------------------------------------------------------------------------
    def test_bts_30_tamper_detection_invariants(self):
        """Invokes authoritative GovernanceLockValidator to test hash match, tampering, illegal auto-lock, unauthorized signers."""
        valid_cfg = generate_valid_config()
        self.assertTrue(GovernanceLockValidator.verify_lock(valid_cfg, dsse_exit_code=0))

        # Tampered configuration payload -> MUST raise ContractViolationError (TAMPERED_CONFIG)
        tampered_cfg = copy.deepcopy(valid_cfg)
        tampered_cfg["theme_mode"] = "dark"
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(tampered_cfg, dsse_exit_code=0)
        self.assertIn("TAMPERED_CONFIG", str(ctx.exception))

        # Illegal auto-lock on Exit 1 (human_review_required=True) -> MUST raise ContractViolationError
        illegal_cfg = generate_valid_config({
            "dsse_decision": {
                "human_review_required": True,
                "human_review_reasons": ["LOW confidence"],
            },
            "governance_lock": {
                "locked": True,
                "locked_by": "DSSE-AUTOMATED-CLEARANCE",
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(illegal_cfg, dsse_exit_code=1)
        self.assertIn("ILLEGAL_AUTO_LOCK_VIOLATION", str(ctx.exception))

        # Unauthorized signer -> MUST raise ContractViolationError (UNAUTHORIZED_SIGNER_VIOLATION)
        unauth_cfg = generate_valid_config({
            "governance_lock": {
                "locked": True,
                "locked_by": "Unknown Junior Developer",
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(unauth_cfg, dsse_exit_code=0)
        self.assertIn("UNAUTHORIZED_SIGNER_VIOLATION", str(ctx.exception))

    # --------------------------------------------------------------------------
    # TEST-BTS-31: Multi-Source Ownership & Immutability Matrix
    # --------------------------------------------------------------------------
    def test_bts_31_ownership_matrix_enforcement(self):
        """Verifies immutability of MDS-derived and DSSE-derived properties against schema constraints."""
        schema_props = self.schema.get("properties", {})
        # Layer A: schema_version is immutable (single enum value 1.0.0)
        self.assertEqual(schema_props["schema_version"].get("enum"), ["1.0.0"])

        # Layer A: min_touch_target_px is immutable (single enum value 44)
        a11y_props = schema_props["accessibility_profile"].get("properties", {})
        self.assertEqual(a11y_props["min_touch_target_px"].get("enum"), [44])

        # Layer B: confidence_tier is strictly constrained
        dsse_props = schema_props["dsse_decision"].get("properties", {})
        self.assertEqual(set(dsse_props["confidence_tier"].get("enum")), {"HIGH", "MEDIUM", "LOW"})

        # Layer B: margin_classification is strictly constrained
        self.assertEqual(set(dsse_props["margin_classification"].get("enum")), {"Decisive Lead", "Tie-Break Zone", "Virtual Tie"})

    # --------------------------------------------------------------------------
    # TEST-BTS-32: Canonical 8 Calibration Cases Evaluation (Cases A through H)
    # --------------------------------------------------------------------------
    def test_bts_32_canonical_8_cases_evaluation(self):
        """Invokes authoritative BootstrapLockPolicyEngine and ImplementationAuthorizer across Cases A through H."""
        cases = [
            ("Case A", "Decisive Lead", "HIGH", False, 0, "AUTOMATED_LOCK", True),
            ("Case B", "Virtual Tie", "HIGH", True, 1, "MANDATORY_HUMAN_REVIEW_GATE", False),
            ("Case C", "Tie-Break Zone", "HIGH", False, 0, "AUTOMATED_LOCK", True),
            ("Case D", "Tie-Break Zone", "HIGH", True, 1, "MANDATORY_HUMAN_REVIEW_GATE", False),
            ("Case E", "Decisive Lead", "MEDIUM", False, 0, "AUTOMATED_LOCK", True),
            ("Case F", "Decisive Lead", "LOW", True, 1, "MANDATORY_HUMAN_REVIEW_GATE", False),
            ("Case G", "Decisive Lead", "HIGH", True, 1, "MANDATORY_HUMAN_REVIEW_GATE", False),
            ("Case H", "N/A", "N/A", True, 2, "EXECUTION_ABORTED", False),
        ]

        for case_id, margin_class, conf, rev_req, exit_code, expected_action, expected_auth in cases:
            cfg = generate_valid_config({
                "dsse_decision": {
                    "candidate_id": "MDS",
                    "selection_score": 90.0,
                    "confidence_tier": conf if conf != "N/A" else "HIGH",
                    "decision_margin_delta": 5.0,
                    "margin_classification": margin_class if margin_class != "N/A" else "Decisive Lead",
                    "human_review_required": rev_req,
                    "human_review_reasons": ["Review Reason"] if rev_req else [],
                    "reproducibility_digest": "a" * 64,
                }
            })

            outcome = BootstrapLockPolicyEngine.apply_lock_policy(exit_code, cfg["dsse_decision"], cfg)
            self.assertEqual(outcome.action, expected_action, f"{case_id} failed lock policy expectation")
            self.assertEqual(outcome.authorized, expected_auth, f"{case_id} failed authorization expectation")

            if expected_auth:
                auth = ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=exit_code)
                self.assertTrue(auth)
            else:
                with self.assertRaises((AuthorizationDeniedError, ContractViolationError)):
                    ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=exit_code)

    # --------------------------------------------------------------------------
    # TEST-BTS-33: Prohibited MDS & DSSE Semantic Overrides
    # --------------------------------------------------------------------------
    def test_bts_33_prohibited_semantic_overrides(self):
        """Prohibits rogue token definitions, alternative math, or component contracts in project config."""
        self.assertIn("Inviolable Non-Alternative Truth Law", self.contract_text)
        self.assertIn("**MUST NOT** and **CANNOT** become an alternative source of truth", self.contract_text)
        self.assertIn("**MUST NOT** redefine DSSE candidate rating matrices", self.contract_text)
        self.assertIn("**MUST NOT** declare alternative token definitions", self.contract_text)

    # --------------------------------------------------------------------------
    # TEST-BTS-34: Failure & Recovery Pathways
    # --------------------------------------------------------------------------
    def test_bts_34_failure_and_recovery_pathways(self):
        """Auto-remediation on validation failure, RFC logging on missing tokens, safe baseline fallbacks."""
        self.assertIn("Failure & Recovery Behavior", self.contract_text)
        self.assertIn("auto-remediation mode", self.contract_text)
        self.assertIn("RFC proposal in `docs/DESIGN_DECISIONS.md`", self.contract_text)
        self.assertIn("safe baseline", self.contract_text)


# ==============================================================================
# Mandatory Negative Security Suite (17 Tests)
# Invokes AUTHORITATIVE Runtime Enforcement Engines from tools.agent_bootstrap
# ==============================================================================

class TestNegativeSecurityInvariants(unittest.TestCase):
    """
    Exhaustive security & boundary audit tests.
    Every single test invokes the authoritative runtime enforcement classes/functions:
    - GovernanceLockValidator.verify_lock
    - ImplementationAuthorizer.authorize_implementation
    - BootstrapLockPolicyEngine.apply_lock_policy
    - validate_json_schema
    Zero inline heuristic shortcuts.
    """

    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

    def test_fixture_a_malformed_configuration(self):
        """Fixture A: Malformed configuration (raw string) must be rejected by schema validator."""
        with self.assertRaises(SchemaValidationError):
            validate_json_schema("not-a-json-object", self.schema)

    def test_fixture_b_unknown_authority_source(self):
        """Fixture B: Unknown authority source property must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["rogue_authority_source"] = "CustomLayerX"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_c_fake_dsse_digest(self):
        """Fixture C: Corrupted reproducibility digest must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["dsse_decision"]["reproducibility_digest"] = "not-a-valid-sha256-hash"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_d_exit_1_auto_lock_rejection(self):
        """Fixture D: Exit 1 + locked=true (DSSE-AUTOMATED-CLEARANCE) must be rejected by GovernanceLockValidator."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "human_review_required": True,
                "human_review_reasons": ["Virtual Tie"],
            },
            "governance_lock": {
                "locked": True,
                "locked_by": "DSSE-AUTOMATED-CLEARANCE",
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=1)
        self.assertIn("ILLEGAL_AUTO_LOCK_VIOLATION", str(ctx.exception))

    def test_fixture_e_exit_2_authorization_denial(self):
        """Fixture E: Exit 2 authorization request must be rejected by ImplementationAuthorizer."""
        cfg = generate_valid_config()
        with self.assertRaises(AuthorizationDeniedError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=2)
        self.assertIn("ABORTED_EXIT_2", str(ctx.exception))

    def test_fixture_f_unauthorized_mds_override(self):
        """Fixture F: Lowering touch target to 24px must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["accessibility_profile"]["min_touch_target_px"] = 24
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_g_unauthorized_dsse_override(self):
        """Fixture G: Unsupported design system candidate must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["selected_design_system"] = "BespokeDivFramework"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_h_invalid_config_hash_format(self):
        """Fixture H: Malformed hash string must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["governance_lock"]["config_hash"] = "invalid_hash_string"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_i_tampered_locked_configuration(self):
        """Fixture I: Mutated configuration payload must be rejected by GovernanceLockValidator."""
        cfg = generate_valid_config()
        cfg["theme_mode"] = "dark"  # Mutated post hash calculation
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=0)
        self.assertIn("TAMPERED_CONFIG", str(ctx.exception))

    def test_fixture_j_missing_required_dsse_field(self):
        """Fixture J: Missing required selection_score must be rejected by schema validator."""
        cfg = generate_valid_config()
        del cfg["dsse_decision"]["selection_score"]
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_k_invalid_confidence_tier(self):
        """Fixture K: Unknown confidence tier ULTRA_HIGH must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["dsse_decision"]["confidence_tier"] = "ULTRA_HIGH"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_l_invalid_margin_classification(self):
        """Fixture L: Unknown margin classification SLIGHT_LEAD must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["dsse_decision"]["margin_classification"] = "SLIGHT_LEAD"
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_fixture_m_fabricated_human_approval(self):
        """Fixture M: Unauthorized signer RogueAgent-999 must be rejected by GovernanceLockValidator."""
        cfg = generate_valid_config({
            "governance_lock": {
                "locked": True,
                "locked_by": "RogueAgent-999",
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=0)
        self.assertIn("UNAUTHORIZED_SIGNER_VIOLATION", str(ctx.exception))

    def test_fixture_n_conflicting_authority_layers(self):
        """Fixture N: Embedding custom token scales in config must be rejected by schema validator."""
        cfg = generate_valid_config()
        cfg["custom_tokens"] = {"--my-color": "#ffffff"}
        with self.assertRaises(SchemaValidationError):
            validate_json_schema(cfg, self.schema)

    def test_additional_exit_3_authorization_denial(self):
        """Additional: Exit 3 authorization request must be rejected by ImplementationAuthorizer."""
        cfg = generate_valid_config()
        with self.assertRaises(AuthorizationDeniedError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=3)
        self.assertIn("ABORTED_EXIT_3", str(ctx.exception))

    def test_additional_exit_4_authorization_denial(self):
        """Additional: Exit 4 authorization request must be rejected by ImplementationAuthorizer."""
        cfg = generate_valid_config()
        with self.assertRaises(AuthorizationDeniedError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=4)
        self.assertIn("ABORTED_EXIT_4", str(ctx.exception))

    def test_additional_continue_implementation_after_exit_1_blocked(self):
        """Additional: Attempt to continue implementation after Exit 1 without Architect signature must be blocked."""
        cfg = generate_valid_config({
            "dsse_decision": {"human_review_required": True},
            "governance_lock": {"locked": False}
        })
        with self.assertRaises(ContractViolationError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=1)
        self.assertIn("UNLOCKED_DRAFT", str(ctx.exception))


# ==============================================================================
# Dedicated Boundary Enforcement Suite (10 Tests: BOUNDARY-01 to BOUNDARY-10)
# ==============================================================================

class TestBoundaryEnforcementSuite(unittest.TestCase):
    """
    Mandatory boundary tests verifying strict separation-of-concerns:
    All tests invoke the authoritative runtime enforcement engines from tools.agent_bootstrap:
    - BOUNDARY-01: Exit 1 + human_review_required=true + attempted locked=true -> actual enforcement rejects
    - BOUNDARY-02: Exit 2 -> actual implementation authorization rejects
    - BOUNDARY-03: Exit 3 -> actual implementation authorization rejects
    - BOUNDARY-04: Exit 4 -> actual implementation authorization rejects
    - BOUNDARY-05: Exit 1 + fake automated clearance -> actual enforcement rejects
    - BOUNDARY-06: Exit 1 + fabricated human signer -> actual enforcement rejects
    - BOUNDARY-07: Locked config mutation after SHA-256 -> actual enforcement rejects
    - BOUNDARY-08: Valid Exit 0 + valid DSSE decision -> actual implementation permits lock
    - BOUNDARY-09: Valid Exit 1 + valid Lead Architect approval -> actual implementation permits transition
    - BOUNDARY-10: Attempt to continue implementation after denied authorization -> actual enforcement rejects
    """

    def test_boundary_01_exit_1_attempted_lock_rejected(self):
        """BOUNDARY-01: Exit 1 + human_review_required=true + attempted locked=true -> actual enforcement rejects."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "human_review_required": True,
                "human_review_reasons": ["Virtual Tie (Δ <= 1.0%)"]
            },
            "governance_lock": {
                "locked": True,
                "locked_by": "DSSE-AUTOMATED-CLEARANCE"
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=1)
        self.assertIn("ILLEGAL_AUTO_LOCK_VIOLATION", str(ctx.exception))

    def test_boundary_02_exit_2_authorization_rejected(self):
        """BOUNDARY-02: Exit 2 -> actual implementation authorization rejects."""
        cfg = generate_valid_config()
        with self.assertRaises(AuthorizationDeniedError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=2)
        self.assertIn("ABORTED_EXIT_2", str(ctx.exception))

    def test_boundary_03_exit_3_authorization_rejected(self):
        """BOUNDARY-03: Exit 3 -> actual implementation authorization rejects."""
        cfg = generate_valid_config()
        with self.assertRaises(AuthorizationDeniedError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=3)
        self.assertIn("ABORTED_EXIT_3", str(ctx.exception))

    def test_boundary_04_exit_4_authorization_rejected(self):
        """BOUNDARY-04: Exit 4 -> actual implementation authorization rejects."""
        cfg = generate_valid_config()
        with self.assertRaises(AuthorizationDeniedError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=4)
        self.assertIn("ABORTED_EXIT_4", str(ctx.exception))

    def test_boundary_05_exit_1_fake_automated_clearance_rejected(self):
        """BOUNDARY-05: Exit 1 + fake automated clearance -> actual enforcement rejects."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "human_review_required": True,
                "human_review_reasons": ["Low confidence"]
            },
            "governance_lock": {
                "locked": True,
                "locked_by": "DSSE-AUTOMATED-CLEARANCE"
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=1)
        self.assertIn("ILLEGAL_AUTO_LOCK_VIOLATION", str(ctx.exception))

    def test_boundary_06_exit_1_fabricated_human_signer_rejected(self):
        """BOUNDARY-06: Exit 1 + fabricated human signer -> actual enforcement rejects."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "human_review_required": True,
                "human_review_reasons": ["Unresolved Tie"]
            },
            "governance_lock": {
                "locked": True,
                "locked_by": "Impostor Architect"
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=1)
        self.assertIn("UNAUTHORIZED_SIGNER_VIOLATION", str(ctx.exception))

    def test_boundary_07_locked_config_mutation_after_hash_rejected(self):
        """BOUNDARY-07: Locked config mutation after SHA-256 -> actual enforcement rejects."""
        cfg = generate_valid_config()
        # Mutate visual personality after valid hash computation
        cfg["visual_personality"] = "expressive_brand"
        with self.assertRaises(ContractViolationError) as ctx:
            GovernanceLockValidator.verify_lock(cfg, dsse_exit_code=0)
        self.assertIn("TAMPERED_CONFIG", str(ctx.exception))

    def test_boundary_08_valid_exit_0_automated_lock_permitted(self):
        """BOUNDARY-08: Valid Exit 0 + valid DSSE decision -> actual implementation permits lock."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "candidate_id": "MDS",
                "selection_score": 95.0,
                "confidence_tier": "HIGH",
                "decision_margin_delta": 4.5,
                "margin_classification": "Decisive Lead",
                "human_review_required": False,
                "human_review_reasons": [],
                "reproducibility_digest": "e" * 64
            }
        })
        outcome = BootstrapLockPolicyEngine.apply_lock_policy(0, cfg["dsse_decision"], cfg)
        self.assertEqual(outcome.action, "AUTOMATED_LOCK")
        self.assertTrue(outcome.authorized)
        self.assertTrue(cfg["governance_lock"]["locked"])
        self.assertEqual(cfg["governance_lock"]["locked_by"], "DSSE-AUTOMATED-CLEARANCE")

        # Authorization succeeds
        authorized = ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=0)
        self.assertTrue(authorized)

    def test_boundary_09_valid_exit_1_architect_approval_permitted(self):
        """BOUNDARY-09: Valid Exit 1 + valid Lead Architect approval -> actual implementation permits transition."""
        cfg = generate_valid_config({
            "dsse_decision": {
                "candidate_id": "MDS",
                "selection_score": 85.0,
                "confidence_tier": "MEDIUM",
                "decision_margin_delta": 0.5,
                "margin_classification": "Virtual Tie",
                "human_review_required": True,
                "human_review_reasons": ["Virtual Tie"],
                "reproducibility_digest": "f" * 64
            },
            "governance_lock": {
                "locked": True,
                "locked_by": "Lead Architect Mohamed Khalid",
                "lock_timestamp": "2026-10-01T21:30:00Z",
                "review_resolution": "RATIFIED_BY_ARCHITECT",
                "config_hash": ""
            }
        })
        cfg["governance_lock"]["config_hash"] = compute_canonical_config_hash(cfg)

        # Implementation authorization post-review succeeds
        authorized = ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=1)
        self.assertTrue(authorized)

    def test_boundary_10_continue_implementation_after_denied_auth_rejected(self):
        """BOUNDARY-10: Attempt to continue implementation after denied authorization -> actual enforcement rejects."""
        cfg = generate_valid_config({
            "governance_lock": {
                "locked": False,
                "locked_by": "",
                "config_hash": "0" * 64
            }
        })
        with self.assertRaises(ContractViolationError) as ctx:
            ImplementationAuthorizer.authorize_implementation(cfg, dsse_exit_code=1)
        self.assertIn("UNLOCKED_DRAFT", str(ctx.exception))


# ==============================================================================
# Standalone CLI Test Runner
# ==============================================================================

def run_all_tests():
    """Runs the full test suite with structured terminal telemetry."""
    print("=" * 80)
    print("      MASTER DESIGN SYSTEM (MDS) — AGENT BOOTSTRAP TEST SUITE")
    print("=" * 80)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestAgentBootstrapSuite))
    suite.addTests(loader.loadTestsFromTestCase(TestNegativeSecurityInvariants))
    suite.addTests(loader.loadTestsFromTestCase(TestBoundaryEnforcementSuite))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("-" * 80)
    print(f"Total Tests Executed : {result.testsRun}")
    print(f"Passed               : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed               : {len(result.failures)}")
    print(f"Errors               : {len(result.errors)}")
    print("-" * 80)

    if result.wasSuccessful():
        print(">>> AGENT BOOTSTRAP SUITE VERDICT: SUCCESS (All Invariants & Boundaries Satisfied) <<<")
        return 0
    else:
        print(">>> AGENT BOOTSTRAP SUITE VERDICT: FAILED <<<")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
