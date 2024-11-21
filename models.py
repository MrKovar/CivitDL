from enum import Enum
from typing import List
from abc import ABC, abstractmethod


class ModelTypes(Enum):
    CHECKPOINT = 0
    TEXTUALINVERSION = 1
    HYPERNETWORK = 2
    AESTHETICGRADIENT = 3
    LORA = 4
    CONTROLNET = 5
    POSES = 6


class ModelFormats(Enum):
    SAFETENSOR = 0
    PICKLETENSOR = 1
    OTHER = 2


class CivitAIModel(ABC):
    invalid_chars = [
        ":",
        ",",
        "(",
        ")",
        "/",
        "\\",
        "|",
        "[",
        "]",
        "{",
        "}",
        "<",
        ">",
        "?",
        "*",
        '"',
        "'",
    ]

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    def replace_special_chars(self, name: str) -> str:
        formatted_name = name
        for char in self.invalid_chars:
            formatted_name = name.replace(char, "")
        formatted_name = "".join(formatted_name.split())
        return formatted_name


class ModelVersionsFiles:

    def __init__(
        self,
        id: int,
        sizeKB: int,
        type: ModelTypes,
        **_,
    ):
        self.id = id
        self.size_in_kb = sizeKB
        self.type = type

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
        type: ModelTypes,
        modelVersions: List[ModelVersions],
        **_,
    ):
        self.id = id
        self.name = name
        self.model_type = type
        self.model_versions = modelVersions
        self.base_model = self.model_versions[0].base_model
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
            type: ModelTypes,
            **_,
        ):
            self.name = name
            self.model_type = type

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
        self.base_model = baseModel.upper()
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
