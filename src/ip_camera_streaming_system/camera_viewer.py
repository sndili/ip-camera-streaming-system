
import cv2
import json
import os
import time
import requests
from pathlib import Path
from datetime import datetime

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "camera_config.json"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
RECORDINGS_DIR = PROJECT_ROOT / "recordings"

# Reconnection settings
MAX_RECONNECT_ATTEMPTS = 5
RECONNECT_DELAY = 2
MAX_FAILED_READS = 5

# Recording settings
RECORDING_FPS = 20.0

# Load camera configuration
with open(CONFIG_PATH, "r") as file:
    camera_config = json.load(file)

camera_name = camera_config["camera_name"]
stream_url = camera_config["stream_url"]
display_width = camera_config["display_width"]


def check_camera_server():
    """Check whether the camera's HTTP server is reachable."""
    server_url = stream_url.rsplit("/video", 1)[0]

    response = requests.get(server_url, timeout=5)
    response.raise_for_status()


def connect_camera():
    """Connect to the IP camera."""
    try:
        check_camera_server()
        camera = cv2.VideoCapture(stream_url)

        if camera.isOpened():
            return camera

        camera.release()

    except requests.RequestException as error:
        print(f"Camera server unavailable: {error}")

    return None


def resize_frame(frame):
    """Resize the frame while preserving its aspect ratio."""
    height, width = frame.shape[:2]
    new_height = int(height * display_width / width)

    return cv2.resize(frame, (display_width, new_height))


def main():
    camera = None
    video_writer = None
    recording = False
    recording_start = None
    failed_reads = 0
    fps = 0
    previous_time = time.time()
    last_message = ""

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    try:
        # Initial camera connection
        for attempt in range(1, MAX_RECONNECT_ATTEMPTS + 1):
            print(f"Connection attempt {attempt}/{MAX_RECONNECT_ATTEMPTS}")

            camera = connect_camera()

            if camera is not None:
                break

            time.sleep(RECONNECT_DELAY)

        if camera is None:
            print("Could not connect to the camera. Check the URL and network.")
            return

        print("Camera streaming started.")
        print("Press S to capture a screenshot.")
        print("Press R to start/stop recording.")
        print("Press ESC to exit.")

        while True:
            success, frame = camera.read()

            if not success:
                failed_reads += 1
                print(
                    f"Frame read failed "
                    f"({failed_reads}/{MAX_FAILED_READS})"
                )

                if failed_reads < MAX_FAILED_READS:
                    time.sleep(0.5)
                    continue

                print("Camera connection lost.")
                camera.release()
                camera = None

                reconnected = False

                for attempt in range(1, MAX_RECONNECT_ATTEMPTS + 1):
                    print(
                        f"Reconnection attempt "
                        f"{attempt}/{MAX_RECONNECT_ATTEMPTS}"
                    )

                    time.sleep(RECONNECT_DELAY)
                    camera = connect_camera()

                    if camera is not None:
                        print("Camera reconnected successfully!")
                        reconnected = True
                        failed_reads = 0
                        break

                if not reconnected:
                    print("Could not reconnect to the camera.")
                    break

                continue

            failed_reads = 0

            # Resize frame
            frame = resize_frame(frame)
            height, width = frame.shape[:2]

            # Calculate FPS
            current_time = time.time()
            elapsed = current_time - previous_time

            if elapsed > 0:
                fps = 1 / elapsed

            previous_time = current_time

            # Add information overlays
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cv2.putText(
                frame, camera_name, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2
            )

            cv2.putText(
                frame, timestamp, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 2
            )

            cv2.putText(
                frame, f"Resolution: {width}x{height}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 2
            )

            cv2.putText(
                frame, f"FPS: {fps:.1f}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 2
            )

            # Recording status
            if recording:
                elapsed_recording = time.time() - recording_start

                cv2.putText(
                    frame,
                    f"RECORDING {elapsed_recording:.1f}s",
                    (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

                video_writer.write(frame)

            # Screenshot confirmation
            if time.time() - previous_time < 0.05 and last_message:
                pass

            if last_message:
                cv2.putText(
                    frame, last_message, (10, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0), 2
                )

            cv2.imshow("IP Camera Stream", frame)

            key = cv2.waitKey(1) & 0xFF

            # Capture screenshot
            if key == ord("s") or key == ord("S"):
                filename = (
                    f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
                )
                filepath = SCREENSHOTS_DIR / filename

                if cv2.imwrite(str(filepath), frame):
                    last_message = "Screenshot saved!"
                    print(f"Screenshot saved: {filepath}")
                else:
                    last_message = "Screenshot could not be saved."

            # Start or stop recording
            elif key == ord("r") or key == ord("R"):
                if not recording:
                    filename = (
                        f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                    )
                    filepath = RECORDINGS_DIR / filename

                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

                    video_writer = cv2.VideoWriter(
                        str(filepath),
                        fourcc,
                        RECORDING_FPS,
                        (width, height)
                    )

                    if video_writer.isOpened():
                        recording = True
                        recording_start = time.time()
                        last_message = "Recording started!"
                        print(f"Recording started: {filepath}")
                    else:
                        video_writer.release()
                        video_writer = None
                        last_message = "Could not start recording."
                        print("Could not start recording.")

                else:
                    recording = False
                    video_writer.release()
                    video_writer = None
                    last_message = "Recording saved!"
                    print("Recording stopped and saved.")

            # Exit stream
            elif key == 27:
                print("ESC pressed. Stopping stream.")
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping stream.")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")

    finally:
        if video_writer is not None:
            video_writer.release()

        if camera is not None:
            camera.release()

        cv2.destroyAllWindows()

        print("All camera resources released.")


if __name__ == "__main__":
    main()