# CrowdAnonymizer
A real‑time human‑head detection and anonymization tool using a custom YOLO model. Supports one or two webcams. Converts video to grayscale and saves it as “.avi”. Can anonymize live recordings as well as existing videos and images.

Option 1: Real‑Time Recording and Anonymization
This Python application opens one or two cameras, detects and blurs all human heads, converts the frames to grayscale, and saves the resulting video as “.avi”.
Head detection is powered by YOLO. The custom model was trained exclusively for this task using 52,000 diverse images to achieve optimal performance.
The model detects entire human heads, not just faces (single‑class model). Heads are blurred regardless of viewing angle.
No data is stored before it has been anonymized.
Videos are saved in the directory Pictures/CrowdAnonymizer.
The GUI is built with Tkinter, and video processing is handled by OpenCV.
Multiple cameras can be used to achieve a wider field of view.
The program uses multithreading but does not rely on multiprocessing.

Option 2: Anonymizing Existing Videos or Images
Load an existing video or image and anonymize it.
Choose whether the output should be grayscale or remain in color.
Select whether the video should be saved as .avi or .mp4.

Program Execution
When launched, the program first displays a small “Loading” window.
A secondary thread loads all required libraries and the YOLO model.
Once loading is complete, the main window appears, offering two options:
“Record video” or “Load files”.
After selecting an option, the interface updates accordingly.
-Option 1 Interface
Top‑left: Select which webcam(s) to use.
You may use one or two cameras simultaneously; frames are displayed side by side.
A background image illustrates the anonymization process.
A green triangle in the center starts the recording when clicked.
It changes to a red circle to stop the recording.
Videos are saved in Pictures/CrowdAnonymizer with the filename format:
out‑DDMMYYhhmm.avi (day, month, year, hour, minute).
The recorded video is displayed directly in the main window.
-Option 2 Interface
Top‑left: Input field for pasting the video path.
To the right: Two dropdown menus for selecting color mode and output format.
A play button starts the processing.
When clicked, the button disappears and a “Video processing” label appears.
After completion, the label disappears and the play button returns.
The process can be repeated as often as needed.
Below the video path section is a similar interface for loading an image.
Images can be saved in grayscale or color.

Use Case
This application is designed for capturing videos of public gatherings without exposing individuals to identification risks.
For example, it can serve as a protective camera during demonstrations.
You can document incidents of violence while ensuring that no participant feels uncomfortable being filmed.
The risk of misuse of your recordings is minimized.
Such anonymized footage can support public discussions, for instance in cases of police violence ore powerabuse.

greate .exe file: use pyinstaller with: pyinstaller --onedir -w -i icon.ico --add-data "human_head.pt;." --add-data "background.png;." --add-data "icon.ico;." main.py
