
import base64
import json
import os
import shutil
import traceback
from datetime import datetime
from typing import List, Optional

import openai
from access_token import validate_access_token
from image_generation import create_alt_url_mapping, generate_images
from llm import stream_openai_response
from mock import mock_completion
from prompts import assemble_prompt
from pydantic import BaseModel
from utils import extract_source_code, write_logs

# Useful for debugging purposes when you don't want to waste GPT4-Vision credits
# Setting to True will stream a mock response instead of calling the OpenAI API
# TODO: Should only be set to true when value is 'True', not any abitrary truthy value
SHOULD_MOCK_AI_RESPONSE = bool(os.environ.get("MOCK", False))

# Set to True when running in production (on the hosted version)
# Used as a feature flag to enable or disable certain features
IS_PROD = os.environ.get("IS_PROD", False)

FRONTEND_FILE_PATH = "../frontend/src/components/GeneratedComponent.tsx"
LOADING_FILE_PATH = "../frontend/src/components/LoadingComponent.tsx"


class GenerateCodeRequest(BaseModel):
    generationType: str;
    image: str;
    resultImage: Optional[str];
    history: Optional[List[str]];
    openAiApiKey: Optional[str]
    openAiBaseURL: Optional[str]
    screenshotOneApiKey: Optional[str]
    isImageGenerationEnabled: bool
    generatedCodeConfig: str
    isTermOfServiceAccepted: bool
    accessCode: Optional[str]

class GenerateCodeResponse(BaseModel):
    code: str

# TODO: reduce code duplication with websocket version (main.py)

async def generate_code(request: GenerateCodeRequest):
    print("Generating code...")
    shutil.copyfile(LOADING_FILE_PATH, FRONTEND_FILE_PATH)

    # Read the code config settings from the request. Fall back to default if not provided.
    generated_code_config = ""
    if request.generatedCodeConfig:
        generated_code_config = request.generatedCodeConfig
    print(f"Generating {generated_code_config} code")

    # Get the OpenAI API key from the request. Fall back to environment variable if not provided.
    # If neither is provided, we throw an error.
    openai_api_key = None
    if  request.accessCode:
        print("Access code - using platform API key")
        res = await validate_access_token(request.accessCode)
        if res["success"]:
            openai_api_key = os.environ.get("PLATFORM_OPENAI_API_KEY")
        else:
            raise Exception(res["failure_reason"])
    else:
        if request.openAiApiKey:
            openai_api_key = request.openAiApiKey
            print("Using OpenAI API key from client-side settings dialog")
        else:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if openai_api_key:
                print("Using OpenAI API key from environment variable")

    if not openai_api_key:
        print("OpenAI API key not found")
        raise Exception(
            "No OpenAI API key found. Please add your API key in the settings dialog or add it to backend/.env file."
        )

    # Get the OpenAI Base URL from the request. Fall back to environment variable if not provided.
    openai_base_url = None
    # Disable user-specified OpenAI Base URL in prod
    if not os.environ.get("IS_PROD"):
        if  request.openAiBaseURL:
            openai_base_url = request.openAiBaseURL
            print("Using OpenAI Base URL from client-side settings dialog")
        else:
            openai_base_url = os.environ.get("OPENAI_BASE_URL")
            if openai_base_url:
                print("Using OpenAI Base URL from environment variable")

    if not openai_base_url:
        print("Using official OpenAI URL")

    # Get the image generation flag from the request. Fall back to True if not provided.
    should_generate_images = request.isImageGenerationEnabled

    print("generating code...")

    # Assemble the prompt
    try:
        if request.resultImage:
            prompt_messages = assemble_prompt(
                request.image, generated_code_config, request.resultImage
            )
        else:
            prompt_messages = assemble_prompt(request.image, generated_code_config)
    except:
        raise Exception("Error assembling prompt")

    # Image cache for updates so that we don't have to regenerate images
    image_cache = {}

    if request.generationType == "update":
        # Transform into message format
        # TODO: Move this to frontend
        for index, text in enumerate(request.history):
            prompt_messages += [
                {"role": "assistant" if index % 2 == 0 else "user", "content": text}
            ]
        image_cache = create_alt_url_mapping(request.history[-2])

    if SHOULD_MOCK_AI_RESPONSE:
        completion = await mock_completion(None)
    else:
        try:
            completion = await stream_openai_response(
                prompt_messages,
                api_key=openai_api_key,
                base_url=openai_base_url,
            )
        except openai.AuthenticationError as e:
            print("[GENERATE_CODE] Authentication failed", e)
            error_message = (
                "Incorrect OpenAI key. Please make sure your OpenAI API key is correct, or create a new OpenAI API key on your OpenAI dashboard."
                + (
                    " Alternatively, you can purchase code generation credits directly on this website."
                    if IS_PROD
                    else ""
                )
            )
            raise Exception(error_message)
        except openai.NotFoundError as e:
            print("[GENERATE_CODE] Model not found", e)
            error_message = (
                e.message
                + ". Please make sure you have followed the instructions correctly to obtain an OpenAI key with GPT vision access: https://github.com/abi/screenshot-to-code/blob/main/Troubleshooting.md"
                + (
                    " Alternatively, you can purchase code generation credits directly on this website."
                    if IS_PROD
                    else ""
                )
            )
            raise Exception(error_message)
        except openai.RateLimitError as e:
            print("[GENERATE_CODE] Rate limit exceeded", e)
            error_message = (
                "OpenAI error - 'You exceeded your current quota, please check your plan and billing details.'"
                + (
                    " Alternatively, you can purchase code generation credits directly on this website."
                    if IS_PROD
                    else ""
                )
            )
            raise Exception(error_message)

    # Write the messages dict into a log so that we can debug later
    write_logs(prompt_messages, completion)

    completion = extract_source_code(completion)

    try:
        if should_generate_images:
            updated_html = await generate_images(
                completion,
                api_key=openai_api_key,
                base_url=openai_base_url,
                image_cache=image_cache,
            )
        else:
            updated_html = completion
    except Exception as e:
        traceback.print_exc()
        print("Image generation failed", e)
        raise Exception("Image generation failed but code is complete.")


    # Write the content of updated_html to GeneratedComponent.tsx
    with open(FRONTEND_FILE_PATH, "w") as file:
        file.write(updated_html)

    return GenerateCodeResponse(code=updated_html)
