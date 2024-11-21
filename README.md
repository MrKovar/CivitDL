# CivitDL
  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Download all your AI needs from CivitAI to the directory you need it with a single command - even login restricted ones if you import cookies!

## Quick Start

Assuming you have Python installed, set the download path variables in `.env` file and run the following command:

`
. ./civitaidl.sh "<civitai_model_url>"`

The script will create a virtual Python environment, download Python dependencies, and run the script to download the model to the directory you specify based on the model metadata. That's it! Run the same command with a different URL to download any other model.

NOTE: If you are wondering where the variable for "embeddings" is stored, its in the TEXTUALINVERSIONS_DIR variable in the `.env` file. They are the same thing. Two words for the same thing. You are not a dingus. It is confusing and its okay to be confused😊

## Cookies

Some models are restricted to users who are logged in. If you have an account, download your cookies from your browser manually using dev tools or with a tool like [Cookie Editor](https://cookie-editor.com/) and refernce the saved cookie file in the `.env` file. The script will automatically use the cookies to download the model and update them per request.

### Prerequisites

You will need to have Python installed on your machine. I might make a containerized version in the future, but felt unneccessary for now.

## License

This project is licensed under the MIT License

## Acknowledgments

* CivitAI and team for hosting the models and making them available for download.
