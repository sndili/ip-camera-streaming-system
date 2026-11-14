# Manual Testing Results

Project: Real-Time IP Camera Video Streaming System

Testing was performed using an Android phone running IP Webcam and a computer connected to the same local network.

| Test ID | Test Description | Action Performed | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC01 | Live camera streaming | Started the camera server and ran the application. | Live video should display continuously. | Live camera feed displayed successfully. | PASS |
| TC02 | Invalid camera URL | Replaced the stream URL with an invalid endpoint and ran the application. | Application should attempt connection and report failure. | Five connection attempts were made before the application reported that it could not connect. | PASS |
| TC03 | Camera unavailable | Stopped the IP Webcam server and ran the application. Restarted the server afterwards. | Application should detect the unavailable camera and recover when the server becomes available. | Connection failed while the server was stopped. Streaming worked again after restarting the server. | PASS |
| TC04 | Information overlays | Ran the application and observed the displayed information. | Camera name, timestamp, resolution and FPS should appear. | Information overlays displayed successfully. | PASS |
| TC05 | Frame resizing | Ran the application with the camera stream. | Frames should be resized while preserving aspect ratio. | Frames displayed at 960 x 540 resolution. | PASS |
| TC06 | Screenshot capture | Pressed S twice during streaming. | Two timestamped screenshots should be saved. | Screenshots were saved successfully in the screenshots folder. | PASS |
| TC07 | Video recording | Pressed R to start recording and R again to stop. | A video file should be saved and playable. | Recording was saved successfully and played correctly. | PASS |
| TC08 | Network interruption | Disabled phone Wi-Fi for approximately 10 seconds, then restored it. | Application should detect failed reads and attempt reconnection. | Five failed reads were detected. The camera reconnected successfully after Wi-Fi was restored. | PASS |
| TC09 | ESC during recording | Started recording and pressed ESC while recording was active. | Application should exit and finalize the recording. | Application exited, released resources and produced a playable video. | PASS |
| TC10 | Ctrl+C during recording | Started recording and interrupted the application using Ctrl+C in the terminal. | Application should handle KeyboardInterrupt and release resources. | KeyboardInterrupt was handled, resources were released and the recording was playable. | PASS |

## Summary

- Total test cases: 10
- Passed: 10
- Failed: 0

All ten manual test cases passed during testing.

## Test Evidence

Screenshots and video evidence should be collected and included with the final project report.