from utils import (
    get_input_params,
    get_model_numbers,
    get_model_info,
    get_model_version_info,
    set_model_versions_obj_from_payload,
    set_model_obj_from_payload,
    download_civitai_model,
    get_cookies_from_file,
    update_cookies,
    MODEL_DIRS,
    COOKIE_FILE_PATH,
)

COOKIES = get_cookies_from_file(COOKIE_FILE_PATH)

if __name__ == "__main__":
    url = get_input_params()
    model, model_version = get_model_numbers(url)

    if model_version:
        print("Using model version...")
        model_payload = get_model_version_info(model_version)

        if not model_payload:
            raise Exception("Model payload was empty for a non-empty model version id")

        model = set_model_versions_obj_from_payload(model_payload)

    else:
        print("Using model...")

        model_payload = get_model_info(model)

        if not model_payload:
            raise Exception("Model payload was empty for a non-empty model id")

        model = set_model_obj_from_payload(model_payload)

    print(model.get_file_name())

    download_res = download_civitai_model(
        model, MODEL_DIRS.get(model.model_type), COOKIES
    )
    COOKIES = update_cookies(download_res)
