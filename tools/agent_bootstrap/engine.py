"""
Master Design System (MDS) — Agent Bootstrap Runtime & Governance Lock Enforcement Engine
Phase 10.2: MDS Agent Bootstrap & Handoff Contract
Layer 13: Implementation, Tooling & Operationalization
Lead Architect: Mohamed Khalid (Senior Full Stack & Flutter Developer)

Authoritative runtime enforcement module providing:
- Domain Exceptions: ContractViolationError, AuthorizationDeniedError, SchemaValidationError
- Cryptographic Hashing: compute_canonical_config_hash (SHA-256)
- JSON Schema Validator: validate_json_schema (Draft 2020-12 recursive engine)
- Lock Policy Engine: BootstrapLockPolicyEngine (DSSE Exit Code 0-4 lock policy)
- Governance Lock Validator: GovernanceLockValidator (Tamper detection, authorized signers, auto-lock prohibition)
- Implementation Authorizer: ImplementationAuthorizer (Autonomous clearance, mandatory human review gate, error halts)
"""

import copy
import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Set, Union


# ==============================================================================
# Domain Exceptions
# ==============================================================================

class SchemaValidationError(Exception):
    """Raised when an object fails JSON schema validation against the canonical schema."""
    pass


class ContractViolationError(Exception):
    """Raised when an action violates an architectural invariant, authority boundary, or lock policy."""
    pass


class AuthorizationDeniedError(Exception):
    """Raised when downstream code generation is denied due to unfulfilled governance gates or errors."""
    pass


# ==============================================================================
# Canonical Cryptographic Hash Calculation
# ==============================================================================

def compute_canonical_config_hash(config_dict: Dict[str, Any]) -> str:
    """
    Computes the canonical SHA-256 hash of a project configuration payload,
    excluding the config_hash field itself to ensure deterministic verification.
    Keys are sorted recursively and compact separators (',', ':') are enforced.
    """
    sanitized = copy.deepcopy(config_dict)
    if "governance_lock" in sanitized and isinstance(sanitized["governance_lock"], dict):
        if "config_hash" in sanitized["governance_lock"]:
            sanitized["governance_lock"]["config_hash"] = ""
    serialized = json.dumps(sanitized, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


# ==============================================================================
# JSON Schema Validator (Draft 2020-12 Pure Standard Library Engine)
# ==============================================================================

def validate_json_schema(instance: Any, schema: Dict[str, Any], path: str = "") -> bool:
    """
    Validates a JSON instance against the Draft 2020-12 schema subset
    utilized in project_design_config.schema.json.
    Pure Python standard library implementation.
    """
    if not isinstance(schema, dict):
        return True

    # 1. Type validation
    expected_type = schema.get("type")
    if expected_type:
        type_map = {
            "object": dict,
            "array": list,
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
        }
        if expected_type == "integer" and isinstance(instance, bool):
            raise SchemaValidationError(f"At {path or 'root'}: expected integer, got boolean")
        if expected_type == "number" and isinstance(instance, bool):
            raise SchemaValidationError(f"At {path or 'root'}: expected number, got boolean")
        expected_py_type = type_map.get(expected_type)
        if expected_py_type and not isinstance(instance, expected_py_type):
            raise SchemaValidationError(f"At {path or 'root'}: expected {expected_type}, got {type(instance).__name__}")

    # 2. Enum validation
    if "enum" in schema:
        if instance not in schema["enum"]:
            raise SchemaValidationError(f"At {path or 'root'}: '{instance}' is not one of allowed enum values {schema['enum']}")

    # 3. String constraints
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            raise SchemaValidationError(f"At {path or 'root'}: string length {len(instance)} < minLength {schema['minLength']}")
        if "pattern" in schema:
            if not re.search(schema["pattern"], instance):
                raise SchemaValidationError(f"At {path or 'root'}: '{instance}' does not match pattern '{schema['pattern']}'")
        if schema.get("format") == "date-time":
            iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
            if not re.match(iso_pattern, instance):
                raise SchemaValidationError(f"At {path or 'root'}: '{instance}' is not a valid ISO-8601 date-time string")

    # 4. Numeric constraints
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaValidationError(f"At {path or 'root'}: value {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            raise SchemaValidationError(f"At {path or 'root'}: value {instance} > maximum {schema['maximum']}")

    # 5. Array constraints
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            raise SchemaValidationError(f"At {path or 'root'}: array items count {len(instance)} < minItems {schema['minItems']}")
        if "items" in schema:
            for idx, item in enumerate(instance):
                validate_json_schema(item, schema["items"], f"{path}[{idx}]")

    # 6. Object constraints
    if isinstance(instance, dict):
        required_fields = schema.get("required", [])
        for req in required_fields:
            if req not in instance:
                raise SchemaValidationError(f"At {path or 'root'}: missing required property '{req}'")

        if schema.get("additionalProperties") is False:
            allowed_props = set(schema.get("properties", {}).keys())
            for key in instance:
                if key not in allowed_props:
                    raise SchemaValidationError(f"At {path or 'root'}: unauthorized additional property '{key}'")

        properties = schema.get("properties", {})
        for prop_name, prop_val in instance.items():
            if prop_name in properties:
                sub_path = f"{path}.{prop_name}" if path else prop_name
                validate_json_schema(prop_val, properties[prop_name], sub_path)

    return True


# ==============================================================================
# Lock Policy Outcome Container
# ==============================================================================

class LockPolicyOutcome:
    """Encapsulates the result of executing the Bootstrap Lock Policy."""
    def __init__(
        self,
        action: str,
        authorized: bool,
        exit_code: int,
        review_reasons: Optional[List[str]] = None,
        error: Optional[str] = None
    ):
        self.action = action
        self.authorized = authorized
        self.exit_code = exit_code
        self.review_reasons = review_reasons or []
        self.error = error

    def __repr__(self) -> str:
        return f"<LockPolicyOutcome action={self.action} authorized={self.authorized} exit_code={self.exit_code}>"


# ==============================================================================
# Authoritative Runtime Engine: BootstrapLockPolicyEngine
# ==============================================================================

class BootstrapLockPolicyEngine:
    """
    Authoritative implementation of the Bootstrap Lock Policy (Section 3.2.2 & 4.4).
    Consumes canonical DSSE Decision Tuple and Exit Code to establish and lock configuration.
    Strictly adheres to the Authority Boundary Law: DOES NOT calculate DSSE formulas.
    """

    @staticmethod
    def apply_lock_policy(
        dsse_exit_code: int,
        dsse_decision: Dict[str, Any],
        config_payload: Dict[str, Any]
    ) -> LockPolicyOutcome:
        """
        Executes the locked Phase 10.2 lock policy on a project design configuration.
        Mutates config_payload in-place with the appropriate governance lock state.
        """
        if dsse_exit_code == 0:
            # Invariant: Exit 0 must have human_review_required == False
            if dsse_decision.get("human_review_required") is True:
                raise ContractViolationError("ILLEGAL_DSSE_STATE: Exit Code 0 cannot require human review.")

            config_payload["governance_lock"]["locked"] = True
            config_payload["governance_lock"]["locked_by"] = "DSSE-AUTOMATED-CLEARANCE"
            if not config_payload["governance_lock"].get("lock_timestamp"):
                config_payload["governance_lock"]["lock_timestamp"] = "2026-10-01T21:00:00Z"
            config_payload["governance_lock"]["review_resolution"] = ""
            config_payload["governance_lock"]["config_hash"] = compute_canonical_config_hash(config_payload)
            return LockPolicyOutcome(action="AUTOMATED_LOCK", authorized=True, exit_code=0)

        elif dsse_exit_code == 1:
            # Enforced Gate on Exit 1: Configuration MUST remain unlocked
            config_payload["governance_lock"]["locked"] = False
            config_payload["governance_lock"]["locked_by"] = ""
            config_payload["governance_lock"]["config_hash"] = "0" * 64
            reasons = dsse_decision.get("human_review_reasons", ["Human review required by DSSE"])
            return LockPolicyOutcome(
                action="MANDATORY_HUMAN_REVIEW_GATE",
                authorized=False,
                exit_code=1,
                review_reasons=reasons
            )

        elif dsse_exit_code in (2, 3, 4):
            # Error states: zero authorization, configuration locked is false
            config_payload["governance_lock"]["locked"] = False
            config_payload["governance_lock"]["locked_by"] = ""
            config_payload["governance_lock"]["config_hash"] = "0" * 64
            return LockPolicyOutcome(
                action="EXECUTION_ABORTED",
                authorized=False,
                exit_code=dsse_exit_code,
                error=f"DSSE CLI failed with Exit Code {dsse_exit_code}"
            )

        else:
            raise ContractViolationError(f"UNKNOWN_DSSE_EXIT_CODE: {dsse_exit_code}")


# ==============================================================================
# Authoritative Runtime Engine: GovernanceLockValidator
# ==============================================================================

class GovernanceLockValidator:
    """
    Authoritative validator verifying project_design_config.json governance lock integrity.
    Verifies lock status, signer authenticity, hash integrity, and tamper detection.
    """

    AUTHORIZED_SIGNERS: Set[str] = {
        "DSSE-AUTOMATED-CLEARANCE",
        "Lead Architect Mohamed Khalid"
    }

    @classmethod
    def verify_lock(
        cls,
        config_payload: Dict[str, Any],
        dsse_exit_code: Optional[int] = None
    ) -> bool:
        """
        Validates governance_lock against the 4 core tamper detection invariants:
        1. locked === false => UNLOCKED_DRAFT (halts)
        2. unauthorized locked_by => UNAUTHORIZED_SIGNER
        3. Exit 1 + "DSSE-AUTOMATED-CLEARANCE" => ILLEGAL_AUTO_LOCK_VIOLATION
        4. payload hash mismatch => TAMPERED_CONFIG
        """
        gov = config_payload.get("governance_lock")
        if not isinstance(gov, dict):
            raise ContractViolationError("MISSING_GOVERNANCE_LOCK: governance_lock object is missing.")

        locked = gov.get("locked")
        locked_by = gov.get("locked_by")
        config_hash = gov.get("config_hash")

        # 1. Unlocked Draft Check
        if not locked:
            raise ContractViolationError("UNLOCKED_DRAFT: Configuration is in unlocked draft state. Downstream code generation prohibited.")

        # 2. Authorized Signer Check
        if locked_by not in cls.AUTHORIZED_SIGNERS:
            raise ContractViolationError(f"UNAUTHORIZED_SIGNER_VIOLATION: '{locked_by}' is not authorized to sign governance lock.")

        # 3. Anti-Bypass: Exit 1 / Human Review Required cannot be signed by DSSE-AUTOMATED-CLEARANCE
        dsse_decision = config_payload.get("dsse_decision", {})
        human_review = dsse_decision.get("human_review_required", False)
        if human_review and locked_by == "DSSE-AUTOMATED-CLEARANCE":
            raise ContractViolationError("ILLEGAL_AUTO_LOCK_VIOLATION: Automated lock is strictly prohibited when DSSE requires human review.")

        # 4. Anti-Bypass: Explicit Non-Zero Exit Code Conflict
        if dsse_exit_code is not None and dsse_exit_code != 0 and locked_by == "DSSE-AUTOMATED-CLEARANCE":
            raise ContractViolationError(f"ILLEGAL_AUTO_LOCK_VIOLATION: Automated clearance cannot lock configuration on Exit Code {dsse_exit_code}.")

        # 5. Cryptographic Hash Integrity / Tamper Detection
        expected_hash = compute_canonical_config_hash(config_payload)
        if config_hash != expected_hash:
            raise ContractViolationError(f"TAMPERED_CONFIG: Configuration hash mismatch. Expected {expected_hash}, got {config_hash}.")

        return True


# ==============================================================================
# Authoritative Runtime Engine: ImplementationAuthorizer
# ==============================================================================

class ImplementationAuthorizer:
    """
    Downstream code synthesis gatekeeper.
    Guarantees that an AI coding agent CANNOT synthesize UI code or tokens
    unless all DSSE and governance prerequisites are mathematically and cryptographically ratified.
    """

    @classmethod
    def authorize_implementation(
        cls,
        config_payload: Dict[str, Any],
        dsse_exit_code: int
    ) -> bool:
        """
        Evaluates whether implementation code synthesis is authorized.
        Raises AuthorizationDeniedError or ContractViolationError if prohibited.
        """
        # 1. Error exit codes immediately deny authorization
        if dsse_exit_code in (2, 3, 4):
            raise AuthorizationDeniedError(f"ABORTED_EXIT_{dsse_exit_code}: Zero implementation authorization granted for tooling/system error.")

        # 2. Verify lock validity (will raise ContractViolationError on unlocked drafts or invalid locks)
        GovernanceLockValidator.verify_lock(config_payload, dsse_exit_code=dsse_exit_code)

        # 3. Handle Exit 1 Human Approval requirement
        if dsse_exit_code == 1:
            gov = config_payload.get("governance_lock", {})
            if gov.get("locked_by") != "Lead Architect Mohamed Khalid":
                raise AuthorizationDeniedError("UNAUTHORIZED_RESOLUTION: Exit 1 requires explicit sign-off by Lead Architect Mohamed Khalid.")

        return True
