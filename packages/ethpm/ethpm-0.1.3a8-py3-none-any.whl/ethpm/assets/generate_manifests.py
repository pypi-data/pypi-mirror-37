import json
from pathlib import Path

from ethpm.backends.ipfs import DummyIPFSBackend
from ethpm.tools import builder as b

# examples dir
EX_DIR = Path(__file__).parent
OWNED_PATH = EX_DIR / "owned" / "owned_compiler_output.json"
ESCROW_PATH = EX_DIR / "escrow" / "xxx.json"
SAFE_MATH_LIB_PATH = EX_DIR / "safe-math-lib" / "safe_math_compiler_output.json"
STANDARD_TOKEN_PATH = EX_DIR / "standard-token" / "standard_token_compiler_output.json"
REGISTRY_PATH = EX_DIR / "registry" / "registry_compiler_output_v2.json"
LINK_PATH = EX_DIR / "link" / "compiler_output.json"
# no compiler output for pipercoin
# PIPERCOIN_PATH = EX_DIR / 'piper-coin' / 'owned_compiler_output.json'
# ignore for now
# REGISTRY_PATH = EX_DIR / 'registry' / 'registry_compiler_output.json'
# TRANSFERABLE_TOKEN_PATH = EX_DIR / 'transferable' / 'transferable_compiler_output.json'
# WALLET_PATH
# WALLET_WITH_SEND_PATH


def generate_link_manifest():
    compiler_output = json.loads(LINK_PATH.read_text())["contracts"]
    manifest = b.build(
        {},
        b.manifest_version("2"),
        b.version("1.0.1"),
        b.package_name("link"),
        b.inline_source("Link", compiler_output, package_root_dir=(EX_DIR / "link")),
        b.inline_source("Test", compiler_output, package_root_dir=(EX_DIR / "link")),
        b.contract_type("Link", compiler_output, abi=True, deployment_bytecode=True),
        b.contract_type("Test", compiler_output, abi=True, deployment_bytecode=True),
        b.validate(),
        b.write_to_disk(manifest_root_dir=(EX_DIR / "link")),
    )

    print("REGISTRY ---------------------------")
    print(manifest)


def generate_registry_manifest():
    compiler_output = json.loads(REGISTRY_PATH.read_text())["contracts"]
    inliner = b.source_inliner(
        compiler_output, package_root_dir=(EX_DIR / "registry" / "contracts")
    )
    manifest = b.build(
        {},
        b.manifest_version("2"),
        b.version("1.0.1"),
        b.package_name("registry"),
        inliner("IndexedOrderedSetLib"),
        inliner("PackageDB"),
        inliner("PackageRegistry"),
        inliner("PackageRegistryInterface"),
        inliner("ReleaseDB"),
        inliner("ReleaseValidator"),
        b.contract_type(
            "IndexedOrderedSetLib",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.contract_type(
            "PackageDB",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.contract_type(
            "PackageRegistry",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.contract_type(
            "PackageRegistryInterface",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.contract_type(
            "ReleaseDB",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.contract_type(
            "ReleaseValidator",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.validate(),
        b.write_to_disk(
            manifest_root_dir=(EX_DIR / "registry"), manifest_name="1.0.1.json"
        ),
    )

    print("REGISTRY ---------------------------")
    print(manifest)


def generate_owned_manifest():
    compiler_output = json.loads(OWNED_PATH.read_text())["contracts"]
    inliner = b.source_inliner(
        compiler_output, package_root_dir=(EX_DIR / "owned" / "contracts")
    )
    manifest = b.build(
        {},
        b.manifest_version("2"),
        b.version("1.0.1"),
        b.package_name("owned"),
        inliner("Owned"),
        b.contract_type("Owned", compiler_output, abi=True, deployment_bytecode=True),
        b.validate(),
        b.to_disk(manifest_root_dir=(EX_DIR / "owned")),
    )

    print("OWNED ---------------------------")
    print(manifest)


def generate_escrow_manifest():
    compiler_output = json.loads(ESCROW_PATH.read_text())["contracts"]
    pinner = b.source_pinner(
        compiler_output,
        DummyIPFSBackend(),
        package_root_dir=(EX_DIR / "escrow" / "contracts"),
    )
    manifest = b.build(
        {},
        b.manifest_version("2"),
        b.version("1.0.3"),
        b.package_name("escrow"),
        pinner("Escrow"),
        pinner("SafeSendLib"),
        b.contract_type(
            "Escrow",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.contract_type(
            "SafeSendLib",
            compiler_output,
            abi=True,
            deployment_bytecode=True,
            runtime_bytecode=True,
        ),
        b.validate(),
        b.to_disk(manifest_root_dir=(EX_DIR / "escrow")),
    )

    print("ESCROW ---------------------------")
    print(manifest)


def generate_safe_math_lib_manifest():
    compiler_output = json.loads(SAFE_MATH_LIB_PATH.read_text())["contracts"]
    pinner = b.source_pinner(
        compiler_output,
        DummyIPFSBackend(),
        package_root_dir=(EX_DIR / "safe-math-lib" / "contracts"),
    )
    manifest = b.build(
        {},
        b.manifest_version("2"),
        b.version("1.0.1"),
        b.package_name("safe-math-lib"),
        pinner("SafeMathLib"),
        b.contract_type(
            "SafeMathLib", compiler_output, abi=True, deployment_bytecode=True
        ),
        b.validate(),
        b.to_disk(manifest_root_dir=(EX_DIR / "safe-math-lib")),
    )

    print("SAFEMATHLIB ---------------------------")
    print(manifest)


def generate_standard_token_manifest():
    compiler_output = json.loads(STANDARD_TOKEN_PATH.read_text())["contracts"]
    pinner = b.source_pinner(
        compiler_output,
        DummyIPFSBackend(),
        package_root_dir=(EX_DIR / "standard-token" / "contracts"),
    )
    manifest = b.build(
        {},
        b.manifest_version("2"),
        b.version("1.0.1"),
        b.package_name("standard-token"),
        pinner("Token"),
        pinner("StandardToken"),
        b.contract_type("Token", compiler_output, abi=True, deployment_bytecode=True),
        b.contract_type(
            "StandardToken", compiler_output, abi=True, deployment_bytecode=True
        ),
        b.validate(),
        b.to_disk(manifest_root_dir=(EX_DIR / "standard-token")),
    )

    print("STANDARDTOKEN ---------------------------")
    print(manifest)


generate_link_manifest(),
# generate_registry_manifest()
# generate_owned_manifest()
# generate_escrow_manifest()
# generate_safe_math_lib_manifest()
# generate_standard_token_manifest()
print("DONE")
