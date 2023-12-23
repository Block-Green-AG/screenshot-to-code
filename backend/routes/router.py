import base64
import json
import os
import traceback
from datetime import datetime
from typing import Optional

import httpx
import openai
from access_token import validate_access_token
from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from image_generation import create_alt_url_mapping, generate_images
from llm import stream_openai_response
from mock import mock_completion
from prompts import assemble_prompt
from pydantic import BaseModel
from routes.generate import GenerateCodeRequest, generate_code
from routes.screenshot import bytes_to_data_url, capture_screenshot
from utils import pprint_prompt

router = APIRouter()

class ScreenshotRequest(BaseModel):
    url: str
    apiKey: str


class ScreenshotResponse(BaseModel):
    url: str

@router.post("/api/screenshot")
async def app_screenshot(request: ScreenshotRequest):
    # Extract the URL from the request body
    url = request.url
    api_key = request.apiKey

    # TODO: Add error handling
    image_bytes = await capture_screenshot(url, api_key=api_key)

    # Convert the image bytes to a data url
    data_url = bytes_to_data_url(image_bytes, "image/png")

    return ScreenshotResponse(url=data_url)


@router.post("/api/generate-code")
async def generate_code_endpoint(request: GenerateCodeRequest):
    return await generate_code(request)