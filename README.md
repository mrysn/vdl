# vdl

Video DownLoad tool, send it URLs via API & CURL from anywhere. Concurrent downloads queued with Celery and Redis, highly customisable, Python Flask-based running in a container.

## Features

- **Video Downloads**: Utilising latest version of `yt-dlp`, pulled upon container build
- **Subtitles**: Downloads and embeds subtitles in the video file as optionable subs
- **Queue System**: Uses Celery and Redis to queue and manage multiple simultanous downloads
- **Custom Arguments**: Allows passing additional `yt-dlp` arguments via the API / cURL commands
- **Containerised**: Fully containerised for easy deployment and scalability

## Installation and Running

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

## Updating `yt-dlp`

Recommended:
- Destroy and rebuild the container

Alternatively:
- Connect to the container CLI and run `yt-dlp -U`

## API Endpoints

### Queue a Download

Endpoint: `/vdl`
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
    http://127.0.0.1:5050/vdl
```
cURL in one line:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ","args": ["--format", "bestvideo+bestaudio"]}' http://127.0.0.1:5050/vdl
```

## Customisation

You can customise the application's behavior by modifying the variables in `config.py`.

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
    "--compat-options", "no-keep-subs",
    "--merge-output-format", "mp4",
    "--ignore-errors",
    "--restrict-filenames",
    "--no-check-certificate",
    "--force-ipv4",
    "--legacy-server-connect",
    "--convert-thumbnail", "jpg",
    "--embed-thumbnail",
    "--add-metadata",
    "--download-archive", "/downloads/yt-dlp-videos-mp4-maxquality.txt",
    "-P", "/downloads"
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