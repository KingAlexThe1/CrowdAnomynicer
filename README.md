# CrowdAnomynicer
Realtime Human-head YOLO detection and blurr; Use 1 or 2 webcams. converts video in crayscale and saves as ".avi". Anomynices Humans in crowds; Anomynice existing video. Custom YOLO-Model.

Option 1: recording and real time anomynication:
This python code opens one ore two cameras, detects and blurrs all Human heads, converts the frames in crayscale and saves the video as ".avi" . The head detections works with YOLO. The custom model is only for this task trained 52000 diffrent pictures for optimal results. The model detecs only Human head, not only faces (one class). The whole head independet of the angle will be blurred. No data will be saved before it is anomyniced. The video will be saved on your Desktop. The Gui works with Tkinter. The video processing with OpenCV. Use multipe cameras to get a whider viewingangle. The programm uses multiple threads but no multiple processes.

Option 2:
Load existiung file to anomynice. Choose if you whant to change the video in grayscale ore leave it in color. Choose if you whant to save it as .avi or .mp4

program execution: The programm will open a single Window with "loading". After a second thread is finisched loading all libarys and the YOLO-modell the main Window will load fully. There you can choose between the two Options: "record video", or "load files". after choose one option the main window will change.
Option1: On the top left you can chooe witch webcam you whant to use. You can use only one ore two at the same time. The frames will be added side by side. In the background will be the background image that shows you what the programm will doo. In the middle is a single green triangle. if clicked. the video will start. The triangle is changed to a read circle to stop the video. The video will be saved on your desktop wih the name: out-DDMMYYhhmm.avi ( out-day Month year minute second) the video will be shown on the main window.
Option2: on the top left is a input field to paste the path to the video. right to the field are two menus to chosse the color and saving format. on the left is a play button to start the video processing. if cligged the play button will disapear an a new label with " video processing" will aspear. if finsched the label disapears and the playbutton will apear again. the process can be sartet again.

Usecase: Use this app to capture videos of public gaterings without the risk of the identification of single people. One example would be a protection-cam for your demonstation. You will be able to record all acts of violenc but noe one will feel unconfortable because he is filmed. The risk of abusing your recordings will be minimiced. E.g. With the video you can form a public discusion in the case of powerabuse from the police.

greate .exe file: use pyinstaller with: pyinstaller --onedir -w -i icon.ico --add-data "human_head.pt;." --add-data "background.png;." --add-data "icon.ico;." main.py
