# Real-Time IP Camera Video Streaming System

A Python application that connects to an IP camera over a local network and displays a real-time video stream using OpenCV.

## Features

- Connects to an IP camera using its HTTP stream URL.
- Displays live video.
- Resizes frames while preserving the original aspect ratio.
- Displays the camera name, timestamp, resolution and estimated FPS.
- Captures and saves screenshots.
- Records and saves video clips.
- Detects failed camera connections.
- Attempts automatic reconnection when the stream is interrupted.
- Releases camera and recording resources safely.
- Detects moving objects using OpenCV Background Subtraction (MOG2).
- Highlights detected movement with bounding boxes and a motion indicator.

## Technologies Used

- Python 3.10+
- OpenCV
- NumPy
- Requests
- Android IP Webcam
- Jupyter Notebook
- Git and GitHub

## Project Structure

```text
ip-camera-streaming-system/
├── config/
│   └── camera_config.json
├── docs/
├── notebooks/
│   └── ip_camera_streaming.ipynb
├── recordings/
├── screenshots/
├── src/
│   └── ip_camera_streaming_system/
│       ├── __init__.py
│       └── camera_viewer.py
├── tests/
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sndili/ip-camera-streaming-system.git
cd ip-camera-streaming-system
```

2. Install UV if it is not already installed.

3. Create the project environment and install dependencies:

```bash
uv sync
```

## Camera Configuration

The application uses a JSON configuration file located at:

`config/camera_config.json`

Create this file with your own camera details:

```json
{
    "camera_name": "Phone Camera",
    "stream_url": "http://YOUR_CAMERA_IP:8080/video",
    "display_width": 960
}
```

Replace `YOUR_CAMERA_IP` with the IP address displayed by your IP Webcam application.

Make sure your phone and computer are connected to the same local network and that the camera server is running.

**Security Measure:** Do not commit your private camera configuration or expose camera credentials and network details publicly.

## Running the Application

Run the following command from the project root:

```bash
uv run python src/ip_camera_streaming_system/camera_viewer.py
```

The live camera window will open when the connection succeeds.

## Keyboard Controls

| Key | Action |
|---|---|
| S | Capture a screenshot |
| R | Start or stop video recording |
| ESC | Exit the application |
| Ctrl + C | Interrupt execution from the terminal |

Screenshots are saved in the `screenshots/` directory, while video recordings are saved in the `recordings/` directory.

## Error Handling

The application handles:

- Invalid or unavailable camera URLs.
- Failed frame reads.
- Interrupted network connections.
- Limited automatic reconnection attempts.
- Keyboard interruptions.
- Safe release of camera and video recording resources.

## Development

The `notebooks/` directory contains the Jupyter Notebook used during development and testing.

The standalone application is located in:

`src/ip_camera_streaming_system/camera_viewer.py`

## License

This project was developed for educational purposes.
