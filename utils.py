import requests
import requests.cookies
from copy import deepcopy
import sys
import re
from enum import Enum
from typing import Optional
from models import (
    CivitAIModelResponse,
    CivitAIModelVersionResponse,
    ModelVersionsFiles,
    ModelVersions,
    CivitAIModel,
)
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://civitai.com/models"

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
COOKIE_FILE_PATH = os.getenv("COOKIE_FILE_PATH")
LORA_DIR = os.getenv("LORA_DIR")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR")
TEXTUALINVERSION_DIR = os.getenv("TEXTUALINVERSION_DIR")
HYPERNETWORK_DIR = os.getenv("HYPERNETWORK_DIR")
AESTHETICGRADIENT_DIR = os.getenv("AESTHETICGRADIENT_DIR")
CONTROLNET_DIR = os.getenv("CONTROLNET_DIR")
POSES_DIR = os.getenv("POSES_DIR")

MODEL_DIRS = {
    "LORA": LORA_DIR,
    "CHECKPOINT": CHECKPOINT_DIR,
    "TEXTUALINVERSION": TEXTUALINVERSION_DIR,
    "HYPERNETWORK": HYPERNETWORK_DIR,
    "AESTHETICGRADIENT": AESTHETICGRADIENT_DIR,
    "CONTROLNET": CONTROLNET_DIR,
    "POSES": POSES_DIR,
}


class ModelDownloadDirectory(Enum):
    LORA = LORA_DIR
    CHECKPOINT = CHECKPOINT_DIR
    TEXTUALINVERSION = TEXTUALINVERSION_DIR
    HYPERNETWORK = HYPERNETWORK_DIR
    AESTHETICGRADIENT = AESTHETICGRADIENT_DIR
    CONTROLNET = CONTROLNET_DIR
    POSES = POSES_DIR


def get_cookie_dict_from_str(cookie_str: str) -> dict:
    """
    Get the cookie dictionary from the cookie string
    """
    return {
        cookie.split("=")[0]: cookie.split("=")[1]
        for cookie in cookie_str.split(";")
        if "=" in cookie
    }


def get_cookies_from_file(cookie_file: str) -> requests.cookies.RequestsCookieJar:
    """
    Get the cookies from the cookie file and return a cookie jar
    """
    cookie_jar = requests.cookies.RequestsCookieJar()
    try:
        with open(cookie_file, "r") as f:
            cookie_dict = get_cookie_dict_from_str(f.readline().strip())
            cookie_jar.update(cookie_dict)
    except Exception as e:
        print(
            f"Error while reading cookies from file in function get_cookies_from_file: {e}"
        )
        print(
            "NOTE: This should not impact the download unless it requires login to download."
        )

    return cookie_jar


def update_cookies(response: requests.Response) -> requests.cookies.RequestsCookieJar:
    """
    Update the cookie jar with the cookies from the response object
    """
    cookie_jar = requests.cookies.RequestsCookieJar()
    if "Set-Cookie" in response.headers:
        cookie_dict = get_cookie_dict_from_str(response.headers["Set-Cookie"])
        cookie_jar.update(cookie_dict)

        write_cookies_to_file(cookie_jar)

    return cookie_jar


def write_cookies_to_file(cookie_jar: requests.cookies.RequestsCookieJar) -> bool:
    """
    Write the cookies to the cookie file
    """
    try:
        with open(COOKIE_FILE_PATH, "w") as f:
            for cookie in cookie_jar:
                f.write(f"{cookie.name}={cookie.value};")
    except Exception as e:
        print(f"Error writing cookies to file in function write_cookies_to_file: {e}")
        print(
            "NOTE: This should not impact the download. Please ensure you have the correct permissions to write to the file."
        )

    return True


def get_model_numbers(url: str) -> tuple[str, Optional[str]]:
    model_url = url[len(BASE_URL) :]
    model_id_pos = re.compile(r"[/?][\d]+", re.DOTALL).search(model_url).span()
    model_version_id_pos = None
    model_version_id = None

    if "modelVersionId=" in url:
        model_version_id_pos = url.rindex("modelVersionId=") + len("modelVersionId=")
        model_version_id = url[model_version_id_pos:]

    return model_url[model_id_pos[0] + 1 : model_id_pos[1]], model_version_id


def get_model_info(model_id: str) -> dict:
    models_info_endpoint = f"https://civitai.com/api/v1/models/{model_id}"

    res = requests.get(models_info_endpoint)

    if res.status_code != 200:
        return None

    if res.json() == {}:
        return None

    return res.json()


def get_model_version_info(model_version: str):
    model_version_info_endpoint = (
        f"https://civitai.com/api/v1/model-versions/{model_version}"
    )

    res = requests.get(model_version_info_endpoint)

    if res.status_code != 200:
        return None

    if res.json() == {}:
        return None

    return res.json()


def set_model_obj_from_payload(payload: dict):
    modify_payload = deepcopy(payload)
    versions_obs = []
    for mv in modify_payload["modelVersions"]:
        mv["files"] = [ModelVersionsFiles(**mf) for mf in mv["files"]]
        versions_obs.append(ModelVersions(**mv))
    modify_payload["modelVersions"] = versions_obs
    return CivitAIModelResponse(**modify_payload)


def set_model_versions_obj_from_payload(payload: dict):
    modify_payload = deepcopy(payload)
    modify_payload["model"] = CivitAIModelVersionResponse.Model(
        **modify_payload["model"]
    )
    files_obj = []
    for files in modify_payload["files"]:
        files_obj.append(ModelVersionsFiles(**files))
    modify_payload["files"] = files_obj
    return CivitAIModelVersionResponse(**modify_payload)


def get_input_params():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    return sys.argv[1]


def download_civitai_model(
    model: CivitAIModel,
    download_dir: str,
    cookie_jar: requests.cookies.RequestsCookieJar,
):
    url = f"https://civitai.com/api/download/models/{model.download_id}?type=Model&format=SafeTensor"

    res = requests.get(url, cookies=cookie_jar, stream=True)

    if res.status_code != 200:
        raise Exception("Failed to download model")

    with open(f"{download_dir}/{model.get_file_name()}", "wb") as f:
        chunk_count = 0
        model_size = int(res.headers["Content-Length"])
        for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
            chunk_count += 1
            if chunk_count % 500 == 0:
                sys.stdout.write(
                    f"Percent Downloaded: {chunk_count * CHUNK_SIZE / model_size * 100:.2f}%\r"
                )
                sys.stdout.flush()
            f.write(chunk)

    print("Download complete!\t\t\t\t")
    return res
