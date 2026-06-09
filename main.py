# Fix for PyInstaller + YOLO
import sys
import io
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

import tkinter as tk
import threading
import os
import ctypes

# Path for compyling with PyInstaller
def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

#close application with "x"
def on_close():
    stop_loop()
    window.destroy()
    os._exit(0)

#open main window with loading....
window = tk.Tk()
window.title("CrowdAnomanycer User Panel")
window.geometry("1616x909")
window.configure(bg="white")
window.iconbitmap(resource_path("icon.ico"))
window.protocol("WM_DELETE_WINDOW", on_close)
Loadinglabel = tk.Label(window, text="Loading...")
Loadinglabel.place(relx=0.45, rely=0.49)


# Variablen
running = False
thread = None
VideoName = "out-MMDDYYhhmm.mp4"
model = None
Videosource1 = None
Videosource2 = None
frame1 = None
frame2 = None
frameWidth1 = 0
frameWidth2 = 0
frameWidthOut = 640
frameHeight1 = 0
frameHeight2 = 0
frameHeightOut = 480
frameadding = False

# loads all libarys and the yolo Model on seperate thread
def LoadImport():
    global cv2, np, YOLO, datetime, time, PhotoImage, model
    import cv2
    import numpy as np
    from ultralytics import YOLO
    import datetime
    from tkinter import PhotoImage
    import time
    model = YOLO(resource_path("human_head.pt"))
    window.after(0, lambda: Main_window())

#compleats the Main Window with option: record anomyniced Video ; anomyniced existing Files 
def Main_window():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("CrowdAnomanycer")

    Loadinglabel.place_forget()
    # Hintergrundbild
    image_path = resource_path("background.png")
    bg_image_file = tk.PhotoImage(file=image_path)
    bg_image = tk.Label(window, image=bg_image_file)
    bg_image.image = bg_image_file
    bg_image.place(x=0, y=0, relwidth=1, relheight=1)

    #Choose-Buttons -> activates one of the options
    recordlabel = tk.Label(window, text="record anomyniced Video", font = "Verdana 20 bold")
    recordlabel.place(relx=0.45, rely=0.4)
    recordlabel.bind("<Button-1>", lambda e: recordMode(window,anomynicefileslabel,recordlabel))
    anomynicefileslabel = tk.Label(window, text="anomyniced existing Files", font = "Verdana 20 bold")
    anomynicefileslabel.place(relx=0.45, rely=0.45)
    anomynicefileslabel.bind("<Button-1>", lambda e: anomyniceFiles(window,recordlabel,anomynicefileslabel))

#modifies the main window for recording Videos with Webcam
def recordMode(window,anomynicefileslabel,recordlabel):
    global Videosource1, Videosource2, frameHeightOut, frameWidthOut, model, canvasC, canvasT
    recordlabel.place_forget()
    anomynicefileslabel.place_forget()
    # Dropdown for Videosources
    Videosources1 = [0, 1, 2, 3, 4]
    Videosources2 = [-1, 0, 1, 2, 3, 4]
    Videosource1 = tk.IntVar(window)
    Videosource1.set(Videosources1[0])
    Videosource2 = tk.IntVar(window)
    Videosource2.set(Videosources2[0])
    Label1 = tk.Label(window, text="choose your main videosource:")
    Label1.place(relx=0.0, rely=0.02)
    Label2 = tk.Label(window, text="choose your second videosource:")
    Label2.place(relx=0.0, rely=0.07)
    Label3 = tk.Label(window, text="-1=Not used; 0 =main camera; 1=second camera;....")
    Label3.place(relx=0.0, rely=0.13)
    Menu1 = tk.OptionMenu(window, Videosource1, *Videosources1)
    Menu1.place(relx=0.2, rely=0.02)
    Menu2 = tk.OptionMenu(window, Videosource2, *Videosources2)
    Menu2.place(relx=0.2, rely=0.07)

    # places Video-Label for pre viewing recording
    video_label = tk.Label(window, bg=None)
    video_label.place(relx=0.33, rely=0.02, width=frameWidthOut, height=frameHeightOut)
    video_label.place_forget()

    # Stop-Button
    canvasC = tk.Canvas(window, width=100, height=100, highlightthickness=0, bg=None)
    canvasC.place(relx=0.45, rely=0.72)
    circle = canvasC.create_oval(0, 0, 100, 100, fill="red", outline=None)
    canvasC.tag_bind(circle, "<Button-1>", lambda e: stop_button_pressed(canvasC, canvasT, video_label))
    canvasC.place_forget()

    # Start-Button
    canvasT = tk.Canvas(window, width=100, height=100, highlightthickness=0, bg=None)
    canvasT.place(relx=0.45, rely=0.72)
    triangle = canvasT.create_polygon(100, 50, 0, 100, 0, 0, fill="green", outline="")
    canvasT.tag_bind(triangle, "<Button-1>", lambda e: start_button_pressed(canvasT, canvasC, video_label))
    
    # Info-Text
    Infolabel = tk.Label(window, text="Videoname: out-DDMMYYhhmm.avi      Storage location: Desktop")
    Infolabel.place(relx=0.0, rely=0.95)

#start choosen webcams and start the processing when webcams are ready
def start_button_pressed(canvasT, canvasC, video_label):
    global frameWidthOut, frameHeightOut, running, thread, frameadding, frame1, frame2
    canvasT.place_forget()
    canvasC.place(relx=0.45, rely=0.72)
    
    if running:
        return  # allready startet

    running = True
    frameadding = False

    #start cam1
    threading.Thread(target=cam1, daemon=True).start()
    #start cam2 if cam is choosen and not the same
    if Videosource2.get() != Videosource1.get() and Videosource2.get() != -1:
        frameadding = True
        threading.Thread(target=cam2, daemon=True).start()
    
    wait_for_frames_and_start_OpenCV(video_label)

def stop_button_pressed(canvasC, canvasT, video_label):
    canvasC.place_forget()
    canvasT.place(relx=0.45, rely=0.72)

    stop_loop()

    # Bild wirklich löschen
    video_label.config(image="", bg=None)
    video_label.image = None
    video_label.place_forget()   

def stop_loop():
    global running, thread, frame1, frame2, frameadding
    running = False

    if thread is not None and thread.is_alive():
        thread.join(timeout=1)
    frame1 = None
    frame2 = None
    frameadding = False

def recordVideo(video_label):
    global running, frame1, frame2, frameWidth1, frameWidth2, frameHeight1, frameHeight2, frameadding, frameHeightOut, frameWidthOut

    #get time for filename
    now = datetime.datetime.now().strftime("%d%m%y%H%M")
    #parameters for saving the file
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    save_path = os.path.join(os.path.expanduser("~"), "Desktop")
    VideoName = os.path.join(save_path, f"out-{now}.avi")

    #calculates framesice for saving the video
    frameWidthOut = frameWidth1 + frameWidth2

    if frameHeight1 < frameHeight2:
        frameHeightOut = frameHeight2
    else:
        frameHeightOut = frameHeight1

    if frameadding == True:
        frameWidthOut = frameWidth1 + frameWidth2
    else:
        frameWidthOut = frameWidth1

    Out = cv2.VideoWriter(VideoName, fourcc, 10, (frameWidthOut, frameHeightOut), isColor=False)
    #calculate position for timestamp
    tSx = frameWidthOut - 90
    tSy = frameHeightOut - 5

    if not Out.isOpened():
        print("VideoWriter konnte nicht geöffnet werden!")
        running = False
        return

    # Frame-Loop
    while running:

        if frameadding:
            if frame1 is not None and frame2 is not None:
                frame = np.hstack((frame1, frame2))
            else:
                continue
        else:
            if frame1 is None:
                continue
            frame = frame1

        # YOLO-results
        results = model(frame, conf=0.1)

        # blurr human heads
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                frame[y1:y2, x1:x2, :] = cv2.blur(frame[y1:y2, x1:x2, :], (40, 40))

        # add Timestamp in lower right corner
        NOWs = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
        frame = cv2.putText(frame, NOWs, (tSx, tSy), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

        # convert in gray
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # load image for Tkinter
        img = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB)
        img = cv2.resize(img, (frameWidthOut,frameHeightOut))
        img = tk.PhotoImage(master=video_label, data=cv2.imencode('.png', img)[1].tobytes())

        # reaload video_label in main window
        video_label.config(image=img)
        video_label.image = img

        cv2.waitKey(1)
        Out.write(frame_gray)

    running = False
    Out.release()

#starts webcam, gets parameters and loads frames in global variable frame1
def cam1():
    global frame1, running, frameWidth1, frameHeight1
    webcam1 = cv2.VideoCapture(Videosource1.get())

    if not webcam1.isOpened():
        print("No video avialible")
        return

    frameWidth1 = int(webcam1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight1 = int(webcam1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while running:
        ret, frame = webcam1.read()
        if not ret:
            continue
        frame1 = frame

    webcam1.release()

#starts webcam, gets parameters and loads frames in global variable frame2
def cam2():
    global frame2, running, frameWidth2, frameHeight2
    webcam2 = cv2.VideoCapture(Videosource2.get())
    frameWidth2 = int(webcam2.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight2 = int(webcam2.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if not webcam2.isOpened():
        print("No video avialible")
        #exit()

    while running:
        ret, frame = webcam2.read()
        if not ret:
            break
        frame2 = frame
    
    webcam2.release()

#waits until cam is ready and starts to deliver frames
def wait_for_frames_and_start_OpenCV(video_label):
    global frame1, frame2, frameadding, thread
    if frame1 is None:
        #loads  it self if no frames are ready
        video_label.after(10, lambda: wait_for_frames_and_start_OpenCV(video_label))
        return

    if frameadding == True:
        if frame2 is None:
            #loads  it self if no frames are ready
            video_label.after(10, lambda: wait_for_frames_and_start_OpenCV(video_label))
            return

    #start OpenCV / YOLO Loop
    thread = threading.Thread(target=recordVideo, args=(video_label,), daemon=True)
    thread.start()
    video_label.place(relx=0.05, rely=0.15, width=frameWidthOut, height=frameHeightOut)

#+++++++++++++++load Videos to anomynice++++++++++++++++++++

#modifies main window for loading existing video
def anomyniceFiles(window,anomynicefileslabel,recordlabel):
    global FilePathV
    #delets options from main window
    anomynicefileslabel.place_forget()
    recordlabel.place_forget()
    #greads inputline for filepath
    FilePathV = tk.StringVar()
    PathLabel1 = tk.Label(window, text="paste the path to your file witout "" :")
    PathLabel1.place(relx=0.0, rely=0.02)
    Inputpath=tk.Entry(window, textvariable=FilePathV, width=100)
    Inputpath.place(relx=0.15, rely=0.02)
    #start button
    canvasT2 = tk.Canvas(window, width=50, height=50, highlightthickness=0, bg=None)
    canvasT2.place(relx=0.6, rely=0.02)
    triangle2 = canvasT2.create_polygon(50, 25, 0, 50, 0, 0, fill="green", outline="")
    #processing information
    processingLabel=tk.Label(window, text="processing video....", fg = "red", font = "Verdana 40 bold")
    processingLabel.place(relx=0.4, rely=0.45)
    processingLabel.place_forget()
    #starts videoprocessing if triangle is pressed
    canvasT2.tag_bind(triangle2, "<Button-1>", lambda e: startVideoanomynication(canvasT2,processingLabel))

#starts seperate thread for videoprocessing
def startVideoanomynication(canvasT2,processingLabel):
    threading.Thread(target=anomyniceVideo, args=(canvasT2,processingLabel,), daemon=True).start()
    #delets start triangle
    canvasT2.place_forget()

#load Video an blurres all human heads
def anomyniceVideo(canvasT2,processingLabel):
    #get filepath from main Window
    video_path = FilePathV.get()
    Video = cv2.VideoCapture(video_path)

    if not Video.isOpened():
        print("No video available:", video_path)
        canvasT2.place(relx=0.6, rely=0.02)
        return

    #get filename for saving
    basename = os.path.basename(video_path)
    filename, ext = os.path.splitext(basename) 

    #parameters for saving
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    save_path = os.path.join(os.path.expanduser("~"), "Desktop")
    VideoName = os.path.join(save_path, f"{filename}_anomyniced.avi")

    frameWidthV = int(Video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeightV = int(Video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FpsV = Video.get(cv2.CAP_PROP_FPS)

    Out = cv2.VideoWriter(VideoName, fourcc, FpsV, (frameWidthV, frameHeightV), isColor=False)

    if not Out.isOpened():
        print("VideoWriter konnte nicht geöffnet werden!")
        canvasT2.place(relx=0.6, rely=0.02)
        return

    #activate processing label
    processingLabel.place(relx=0.4, rely=0.45)

    while True:
        ret, frame = Video.read()
        if not ret:
            break

        # YOLO-results
        results = model(frame, conf=0.1)

        # blurr human heads
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                frame[y1:y2, x1:x2, :] = cv2.blur(frame[y1:y2, x1:x2, :], (40, 40))

        # convert in gray
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        Out.write(frame_gray)

    Video.release()
    Out.release()
    processingLabel.place_forget()
    canvasT2.place(relx=0.6, rely=0.02)

#starts import load
threading.Thread(target=LoadImport, daemon=True).start()
# Start programm
window.mainloop()
