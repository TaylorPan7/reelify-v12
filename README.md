# Video Generation Web Application

A Flask-based web application for generating videos, images, and captions.

## Requirements

- Python 3.13
- Flask
- Flask-CORS

## Project Structure

The application is organized into several files:

- `app.py` - Main application entry point
- `auth.py` - Authentication-related functions
- `video_generator.py` - Video generation functionality
- `routes.py` - All route definitions
- `pexels_maker.py` - Script for generating video content (not included in this repo)
- `merge.py` - Script for merging video and audio (not included in this repo)
- `transcriber_script.py` - Script for generating transcriptions (not included in this repo)
- `captioned_video.py` - Script for adding captions to videos (not included in this repo)

## Installation

1. Clone the repository
2. Install dependencies:

```
pip install flask flask-cors
```

## Running the Application

To run the application, simply execute:

```
python app.py
```

The application will be available at http://localhost:5000

## Features

- User authentication (signup, login, logout)
- Video generation from topics
- Image generation (placeholder)
- Caption generation (placeholder)
- Various informational pages (about, careers, etc.)

## File Structure

All files are stored in the root directory with no subdirectories, making it easy to navigate and maintain. 