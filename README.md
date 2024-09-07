# AI Alt Text Generation API

This API provides alt text generation for images using AI models. It's built with FastAPI and supports multiple models including BLIP-base and InternVL2.

## Features

- Authentication for secure access
- Resource management (GPU and CPU limitations)
- Performance logging
- Automatic model loading on startup
- CORS support

## API Endpoints

- `/api/v1/alt_text`: Generates alt text for a given image

## Setup and Installation

1. Clone this repository
2. Install Docker
3. Build and run the Docker container:

```bash
docker build -t alt-text-api .
docker run -p 8000:8000 alt-text-api
```

## Configuration

Environment variables can be set in the Dockerfile or passed at runtime:

- `API_V1_STR`: API version string
- `PROJECT_NAME`: Name of the project
- `API_KEY`: API key for authentication
- `USE_GPU`: Whether to use GPU (boolean)
- `MAX_CPU_USAGE_PERCENT`: Maximum CPU usage percentage
- `NUMEXPR_MAX_THREADS`: Maximum number of threads for NumExpr

## Usage

Send a POST request to `/api/v1/alt_text` with the image data and any required parameters. Refer to the API documentation for detailed usage instructions.

## Logging

The application logs general system information and specific alt text generation metrics. Check the application logs for detailed information.

## Development

To run the application in development mode:

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `uvicorn app.main:app --reload`
