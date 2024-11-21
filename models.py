from typing import List
from abc import ABC, abstractmethod
import re

# TODO: 
# 1. Add PickleTensor Support
# 2. Add ability to select file if multiple files are available
# 3. Add ability to add file name prefix for tags/nsfw flags (e.g. "FLUX__NSFW-ModelName.safetensors")


class CivitAIModel(ABC):
    invalid_regex = re.compile(r"[^a-zA-Z0-9\s\.\-_]")

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    def replace_special_chars(self, name: str) -> str:
        formatted_name = name
        formatted_name = self.invalid_regex.sub("", formatted_name)
        formatted_name = "".join(formatted_name.split())
        return formatted_name


class ModelVersionsFiles:

    def __init__(
        self,
        id: int,
        sizeKB: int,
        type: str,
        **_,
    ):
        self.id = id
        self.size_in_kb = sizeKB
        self.type = type.upper()

    def __repr__(self):
        return (
            "\tModel Version File:\n"
            + f"\t\tID: {self.id}\n"
            + f"\t\tSize: {self.size_in_kb}\n"
            + f"\t\tType: {self.type}\n"
        )


class ModelVersions:
    def __init__(
        self,
        id: int,
        index: int,
        name: str,
        baseModel: str,
        **_,
    ):
        self.id = id
        self.index = index
        self.name = name
        self.base_model = baseModel.upper()

    def __repr__(self):
        return (
            "\tModel Version:\n"
            + f"\tID: {self.id}\n"
            + f"\tIndex: {self.index}\n"
            + f"\tName: {self.name}\n"
            + f"\tBase Model: {self.base_model}\n"
        )


class CivitAIModelResponse(CivitAIModel):
    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        modelVersions: List[ModelVersions],
        **_,
    ):
        self.id = id
        self.name = name
        self.model_type = type.upper()
        self.model_versions = modelVersions
        self.base_model = "".join(self.model_versions[0].base_model.split())
        self.download_id = self.model_versions[0].id

    def get_file_name(self) -> str:
        formatted_name = self.replace_special_chars(self.name)

        return f"{self.base_model}__{formatted_name}.safetensors"

    def __repr__(self):
        return (
            "CivitAI Model:\n"
            + f"ID: {self.id}\n"
            + f"Name: {self.name}\n"
            + f"Type: {self.model_type}\n"
            + f"{self.model_versions}\n"
        )


class CivitAIModelVersionResponse(CivitAIModel):

    class Model:
        def __init__(
            self,
            name: str,
            type: str,
            **_,
        ):
            self.name = name
            self.model_type = type.upper()

        def __repr__(self):
            return (
                "Model:\n" + f"\tName: {self.name}\n" + f"\tType: {self.model_type}\n"
            )

    def __init__(
        self,
        id: int,
        modelId: int,
        name: str,
        baseModel: str,
        model: Model,
        files: List[ModelVersionsFiles],
        **_,
    ):
        self.id = id
        self.model_id = modelId
        self.name = name
        self.base_model = "".join(baseModel.upper().split())
        self.model = model
        self.model_type = model.model_type
        self.model_files = files
        self.download_id = self.id

    def get_file_name(self) -> str:
        formatted_base_name = self.replace_special_chars(self.model.name)
        formatted_name = self.replace_special_chars(self.name)

        return f"{self.base_model}__{formatted_base_name}-{formatted_name}.safetensors"

    def __repr__(self):
        return (
            "Model Version:\n"
            + f"ID: {self.id}\n"
            + f"Model ID: {self.model_id}\n"
            + f"Name: {self.name}\n"
            + f"Base Model: {self.base_model}\n"
            + f"{self.model}\n"
            + f"{self.model_files}\n"
        )
