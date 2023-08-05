import json
import os
from typing import Any, Dict, List, Set

from jsonschema import ValidationError as jsonValidationError, validate

from ethpm import SPEC_DIR, V2_PACKAGES_DIR
from ethpm.exceptions import ValidationError
from ethpm.typing import Manifest

MANIFEST_SCHEMA_PATH = str(SPEC_DIR / "package.spec.json")

META_FIELDS = {
    "license": str,
    "authors": list,
    "description": str,
    "keywords": list,
    "links": dict,
}


def validate_meta_object(meta: Dict[str, Any], allow_extra_meta_fields: bool) -> None:
    """
    Validates that every key is one of `META_FIELDS` and has a value of the expected type.
    """
    for key, value in meta.items():
        if key in META_FIELDS:
            if type(value) is not META_FIELDS[key]:
                raise ValidationError(
                    "Values for {0} are expected to have the type {1}, instead got {2}.".format(
                        key, META_FIELDS[key], type(value)
                    )
                )
        elif allow_extra_meta_fields:
            if key[:2] != "x-":
                raise ValidationError(
                    "Undefined meta fields need to begin with 'x-', "
                    "{0} is not a valid undefined meta field.".format(key)
                )
        else:
            raise ValidationError(
                "{0} is not a permitted meta field. To allow undefined fields, "
                "set `allow_extra_meta_fields` to True.".format(key)
            )


def _load_schema_data() -> Dict[str, Any]:
    with open(MANIFEST_SCHEMA_PATH) as schema:
        return json.load(schema)


def extract_contract_types_from_deployments(deployment_data: List[Any]) -> Set[str]:
    contract_types = set(
        deployment["contract_type"]
        for chain_deployments in deployment_data
        for deployment in chain_deployments.values()
    )
    return contract_types


def validate_manifest_against_schema(manifest: Dict[str, Any]) -> None:
    """
    Load and validate manifest against schema
    located at MANIFEST_SCHEMA_PATH.
    """
    schema_data = _load_schema_data()
    try:
        validate(manifest, schema_data)
    except jsonValidationError as e:
        raise ValidationError(
            "Manifest invalid for schema version {0}. "
            "Reason: {1}".format(schema_data["version"], e.message)
        )


def check_for_deployments(manifest: Dict[str, Any]) -> bool:
    if "deployments" not in manifest or not manifest["deployments"]:
        return False
    return True


def validate_build_dependencies_are_present(manifest: Dict[str, Any]) -> None:
    if "build_dependencies" not in manifest:
        raise ValidationError("Manifest doesn't have any build dependencies.")

    if not manifest["build_dependencies"]:
        raise ValidationError("Manifest's build dependencies key is empty.")


def validate_manifest_deployments(manifest: Dict[str, Any]) -> None:
    """
    Validate that a manifest's deployments contracts reference existing contract_types.
    """
    if set(("contract_types", "deployments")).issubset(manifest):
        all_contract_types = list(manifest["contract_types"].keys())
        all_deployments = list(manifest["deployments"].values())
        all_deployment_names = extract_contract_types_from_deployments(all_deployments)
        missing_contract_types = set(all_deployment_names).difference(
            all_contract_types
        )
        if missing_contract_types:
            raise ValidationError(
                "Manifest missing references to contracts: {0}.".format(
                    missing_contract_types
                )
            )


def validate_manifest_exists(manifest_id: str) -> None:
    """
    Validate that manifest with manifest_id exists in V2_PACKAGES_DIR
    """
    manifest_path = str(V2_PACKAGES_DIR / manifest_id)
    if not os.path.exists(manifest_path):
        raise ValidationError(
            "Manifest not found in V2_PACKAGES_DIR with id: {0}".format(manifest_id)
        )


def format_manifest(manifest: Manifest, *, prettify: bool) -> str:
    if prettify:
        return json.dumps(manifest, sort_keys=True, indent=4)
    return json.dumps(manifest, sort_keys=True, separators=(",", ":"))
