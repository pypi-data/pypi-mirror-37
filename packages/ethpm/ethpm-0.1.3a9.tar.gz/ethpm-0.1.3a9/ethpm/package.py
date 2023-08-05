import json
from typing import Any, Dict, Union

from eth_utils import to_canonical_address, to_text
from web3 import Web3
from web3.eth import Contract

from ethpm.contract import LinkableContract
from ethpm.dependencies import Dependencies
from ethpm.deployments import Deployments
from ethpm.exceptions import (
    FailureToFetchIPFSAssetsError,
    InsufficientAssetsError,
    PyEthPMError,
)
from ethpm.typing import Address, ContractName
from ethpm.utils.backend import resolve_uri_contents
from ethpm.utils.cache import cached_property
from ethpm.utils.contract import (
    generate_contract_factory_kwargs,
    validate_contract_name,
    validate_minimal_contract_factory_data,
    validate_w3_instance,
)
from ethpm.utils.filesystem import load_manifest_from_file
from ethpm.utils.manifest_validation import (
    check_for_deployments,
    validate_build_dependencies_are_present,
    validate_manifest_against_schema,
    validate_manifest_deployments,
)
from ethpm.validation import (
    validate_address,
    validate_build_dependency,
    validate_single_matching_uri,
)


class Package(object):
    def __init__(self, manifest: Dict[str, Any], w3: Web3) -> None:
        """
        A package should be created using one of the available
        classmethods and a valid w3 instance.
        """
        if not isinstance(manifest, dict):
            raise TypeError(
                "Package object must be initialized with a dictionary. "
                "Got {0}".format(type(manifest))
            )

        validate_manifest_against_schema(manifest)
        validate_manifest_deployments(manifest)
        validate_w3_instance(w3)

        self.w3 = w3
        self.w3.eth.defaultContractFactory = LinkableContract
        self.manifest = manifest

    def set_default_w3(self, w3: Web3) -> None:
        """
        Set the default Web3 instance.
        """
        validate_w3_instance(w3)
        # Mechanism to bust cached properties when switching chains.
        if "deployments" in self.__dict__:
            del self.deployments
        if "build_dependencies" in self.__dict__:
            del self.build_dependencies
        self.w3 = w3
        self.w3.eth.defaultContractFactory = LinkableContract

    def __repr__(self) -> str:
        name = self.name
        version = self.version
        return "<Package {0}=={1}>".format(name, version)

    @property
    def name(self) -> str:
        return self.manifest["package_name"]

    @property
    def version(self) -> str:
        return self.manifest["version"]

    @property
    def manifest_version(self) -> str:
        return self.manifest["manifest_version"]

    @classmethod
    def from_file(cls, file_path_or_obj: str, w3: Web3) -> "Package":
        """
        Return a Package object instantiated by a manifest located at the provided filepath.
        """
        if isinstance(file_path_or_obj, str):
            with open(file_path_or_obj) as file_obj:
                manifest = load_manifest_from_file(file_obj)
        elif hasattr(file_path_or_obj, "read") and callable(file_path_or_obj.read):
            manifest = load_manifest_from_file(file_path_or_obj)
        else:
            raise TypeError(
                "The Package.from_file method takes either a filesystem path or a file-like object."
                "Got {0} instead.".format(type(file_path_or_obj))
            )

        return cls(manifest, w3)

    @classmethod
    def from_uri(cls, uri: str, w3: Web3) -> "Package":
        """
        Return a Package object instantiated by a manifest located at a content-addressed URI.
        URI schemes supported:
            - IPFS          `ipfs://Qm...`
            - HTTP          `https://raw.githubusercontent.com/repo/path.json#hash`
            - Registry      `ercXXX://registry.eth/greeter?version=1.0.0`
        """
        contents = resolve_uri_contents(uri)
        manifest = json.loads(to_text(contents))
        return cls(manifest, w3)

    def get_contract_factory(self, name: ContractName) -> Contract:
        """
        Return a contract factory for a given contract type.
        """
        validate_contract_name(name)

        if "contract_types" not in self.manifest:
            raise InsufficientAssetsError(
                "This package does not contain any contract type data."
            )

        try:
            contract_data = self.manifest["contract_types"][name]
        except KeyError:
            raise InsufficientAssetsError(
                "This package does not contain any package data to generate "
                "a contract factory for contract type: {0}. Available contract types include: "
                "{1}".format(name, list(self.manifest["contract_types"].keys()))
            )

        validate_minimal_contract_factory_data(contract_data)
        contract_kwargs = generate_contract_factory_kwargs(contract_data)
        contract_factory = self.w3.eth.contract(**contract_kwargs)
        return contract_factory

    def get_contract_instance(self, name: ContractName, address: Address) -> Contract:
        """
        Return a Contract object representing the contract type at the provided address.
        """
        validate_address(address)
        validate_contract_name(name)
        try:
            self.manifest["contract_types"][name]["abi"]
        except KeyError:
            raise InsufficientAssetsError(
                "Package does not have the ABI required to generate a contract instance "
                "for contract: {0} at address: {1}.".format(name, address)
            )
        contract_kwargs = generate_contract_factory_kwargs(
            self.manifest["contract_types"][name]
        )
        canonical_address = to_canonical_address(address)
        contract_instance = self.w3.eth.contract(
            address=canonical_address, **contract_kwargs
        )
        return contract_instance

    #
    # Build Dependencies
    #

    @cached_property
    def build_dependencies(self) -> "Dependencies":
        """
        Return `Dependencies` instance containing the build dependencies available on this Package.
        Cached property (self.build_dependencies) busted everytime self.set_default_w3() is called.
        """
        validate_build_dependencies_are_present(self.manifest)

        dependencies = self.manifest["build_dependencies"]
        dependency_packages = {}
        for name, uri in dependencies.items():
            try:
                validate_build_dependency(name, uri)
                dependency_package = Package.from_uri(uri, self.w3)
            except PyEthPMError as e:
                raise FailureToFetchIPFSAssetsError(
                    "Failed to retrieve build dependency: {0} from URI: {1}.\n"
                    "Got error: {2}.".format(name, uri, e)
                )
            else:
                dependency_packages[name] = dependency_package

        return Dependencies(dependency_packages)

    #
    # Deployments
    #

    @cached_property
    def deployments(self) -> Union["Deployments", Dict[None, None]]:
        """
        API to retrieve package deployments available on the current w3-connected chain.
        Cached property (self.deployments) gets busted everytime self.set_default_w3() is called.
        """
        if not check_for_deployments(self.manifest):
            return {}

        all_blockchain_uris = self.manifest["deployments"].keys()
        matching_uri = validate_single_matching_uri(all_blockchain_uris, self.w3)

        deployments = self.manifest["deployments"][matching_uri]
        all_contract_factories = {
            deployment_data["contract_type"]: self.get_contract_factory(
                deployment_data["contract_type"]
            )
            for deployment_data in deployments.values()
        }

        return Deployments(deployments, all_contract_factories, self.w3)
