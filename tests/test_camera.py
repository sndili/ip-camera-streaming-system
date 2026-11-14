import cv2
import numpy as np

from ip_camera_streaming_system.camera_viewer import (
    resize_frame,
    detect_motion
)


def test_resize_frame_preserves_aspect_ratio():
    # Create a 1920 x 1080 test frame
    frame = np.zeros((1080, 1920, 3), dtype=np.uint8)

    resized_frame = resize_frame(frame)

    # Check the new dimensions
    assert resized_frame.shape == (540, 960, 3)


def test_detect_motion_identifies_moving_object():
    # Create a background subtractor
    background_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=500,
        varThreshold=50,
        detectShadows=False
    )

    # Create a stationary black background
    background = np.zeros((200, 200, 3), dtype=np.uint8)

    # Allow the detector to learn the background
    for _ in range(5):
        background_subtractor.apply(background)

    # Create a frame containing a moving white object
    moving_frame = background.copy()
    cv2.rectangle(
        moving_frame,
        (50, 50),
        (150, 150),
        (255, 255, 255),
        -1
    )

    processed_frame, motion_detected = detect_motion(
        moving_frame,
        background_subtractor
    )

    # Check that motion was detected
    assert motion_detected is True
    assert processed_frame.shape == (200, 200, 3)
