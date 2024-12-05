import logging
from flask import Flask, request, jsonify
from celery import Celery
from urllib.parse import urlparse, urlunparse
import shlex
import subprocess
import config  # Import configuration

# Configure logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = config.CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = config.CELERY_RESULT_BACKEND

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

def normalize_url(url):
    """
    Adds a default scheme (http) to URLs if missing and validates the format.
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            parsed = parsed._replace(scheme="http")
        if not parsed.netloc:
            return None
        return urlunparse(parsed)
    except Exception:
        return None

@app.route('/run-command', methods=['POST'])
def queue_command():
    """
    Handles POST requests to queue yt-dlp downloads.
    """
    # Get the data from the request
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL'}), 400

    url = data['url']
    normalized_url = normalize_url(url)
    if not normalized_url:
        return jsonify({'error': 'Invalid URL'}), 400

    # Extract additional arguments
    additional_args = data.get('args', [])
    if not isinstance(additional_args, list):
        return jsonify({'error': 'Args must be a list of strings'}), 400

    # Queue the download task
    task = download_video.apply_async(args=[normalized_url, additional_args])
    return jsonify({'task_id': task.id, 'status': 'queued'}), 202

@celery.task
def download_video(url, additional_args):
    """
    Handles the actual download process using yt-dlp.
    """
    logging.info(f"Starting download for: {url} with args: {additional_args}")

    # Safely escape each argument
    safe_additional_args = [shlex.quote(arg) for arg in additional_args]

    # Combine default arguments and additional arguments
    all_args = config.YT_DLP_DEFAULT_ARGS + safe_additional_args
    args_string = " ".join(all_args)
    command = f'yt-dlp {args_string} -o "{config.YT_DLP_OUTPUT_TEMPLATE}" {shlex.quote(url)}'

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        logging.info(f"Download complete for: {url}")
        return {'result': result}
    except subprocess.CalledProcessError as e:
        logging.error(f"Download failed for: {url}. Error: {e.output}")
        raise e

if __name__ == '__main__':
    logging.info("Starting Flask app")
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT)
