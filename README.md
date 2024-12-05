# vdl

vdl is a Flask-based application that uses `yt-dlp` to download videos from various platforms. The app supports queuing downloads with Celery and Redis, allowing for concurrent downloads with customizable options.

## Features

- **Video Downloads**: Supports video downloads with `yt-dlp`
- **Subtitles**: Downloads and embeds subtitles in the video file
- **Queue System**: Uses Celery and Redis to queue and manage multiple simultanous downloads
- **Custom Arguments**: Allows passing additional `yt-dlp` arguments via the API / cURL commands
- **Dockerized**: Fully containerized for easy deployment and scalability

## Installation

### Prerequisites

- Docker
- Docker Compose
- Git

### Clone the Repository

```bash
git clone https://github.com/mrysn/vdl.git
cd vdl
```

### Running Locally

Build and start the services:

```bash
docker-compose up --build
```

Access the application at http://localhost:5050.

## API Endpoints

Queue a Download

Endpoint: `/run-command`
Method: `POST`
Request Body:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "args": ["--format", "bestvideo+bestaudio"]
}
```
Response:
```json
{
  "task_id": "some-task-id",
  "status": "queued"
}
```

Example using cURL:
```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "args": ["--format", "bestvideo+bestaudio"]
    }' \
    http://127.0.0.1:5050/run-command
```
cURL in one line:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ","args": ["--format", "bestvideo+bestaudio"]}' http://127.0.0.1:5050/run-command
```

## Customization

You can customize the application's behavior by modifying the variables in `config.py`.

### Default Filename Output

```python
YT_DLP_OUTPUT_TEMPLATE = "/downloads/%(channel)s-%(upload_date)s-%(title)s-%(id)s-%(width)sp.%(ext)s"
```

### Default `yt-dlp` Arguments

```python
YT_DLP_DEFAULT_ARGS = [
    "--write-sub",
    "--write-auto-subs",
    "--sub-lang", "en.*",
    "--sub-format", "ttml",
    "--convert-subs", "srt",
    "--embed-subs",
    "--merge-output-format", "mp4",
    "--restrict-filenames",
    # Other arguments...
]
```

## Development

### Hot Reloading

To enable live updates during development, use the following command:
```bash
docker-compose -f docker-compose.override.yml up
```

## Deployment

`vdl` can be deployed using Docker and GitHub Actions. A pre-configured workflow in `.github/workflows/docker-build.yml` builds and pushes Docker images to Docker Hub.

## License

This project is licensed under the MIT License.