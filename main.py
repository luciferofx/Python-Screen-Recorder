import cv2
import numpy as np
import pyautogui
import time
import os
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from threading import Thread

#============================ Setup output folder
recording_folder = "recordings"
os.makedirs(recording_folder, exist_ok=True)

#============================ Screen resolution
screen_width, screen_height = pyautogui.size()
screen_size = (screen_width, screen_height)

#============================ Video writer setup
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
filename = f"ScreenRecording_{time.strftime('%H-%M-%S_%d-%m-%y')}.mp4"
output_path = os.path.join(recording_folder, filename)
output = cv2.VideoWriter(output_path, fourcc, 20.0, screen_size)

#============================ Tkinter UI Setup
root = tk.Tk()
root.title("🎥 LUCI Recorder")
root.geometry("800x500")
root.config(bg="#2e3b4e")
root.resizable(False, False)

#============================ Load Icon (Optional, comment out if no icon available)
try:
    icon = PhotoImage(file="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2GscNm8R1sHnj36EHWCGmdQ4utAD4dL_reA&s")  # Replace with the path to your icon file (png)
    root.iconphoto(True, icon)
except:
    pass  # Ignore if no icon is available

#============================ UI Elements
status_label = tk.Label(root, text="🛑 Press 'Start' to begin recording", font=("Helvetica", 14), bg="#2e3b4e", fg="white")
status_label.pack(pady=10)

progress = ttk.Progressbar(root, length=600, mode='determinate', maximum=100, style="TProgressbar")
progress.pack(pady=10)

timer_label = tk.Label(root, text="00:00", font=("Helvetica", 16), bg="#2e3b4e", fg="white")
timer_label.pack(pady=10)

start_btn = tk.Button(root, text="Start Recording", width=20, height=2, font=("Helvetica", 12), bg="#4CAF50", fg="white", bd=0, relief="solid", command=lambda: start_recording())
start_btn.pack(pady=20)

stop_btn = tk.Button(root, text="Stop Recording", width=20, height=2, font=("Helvetica", 12), bg="#f44336", fg="white", bd=0, relief="solid", state=tk.DISABLED, command=lambda: stop_recording())
stop_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", width=20, height=2, font=("Helvetica", 12), bg="#e53935", fg="white", bd=0, relief="solid", command=root.quit)
exit_btn.pack(pady=20)

#============================ Global Variables
recording = False
elapsed_time = 0

#============================ Style Progress Bar
style = ttk.Style()
style.configure("TProgressbar",
                thickness=30,
                background="#00bcd4",
                )

def update_timer():
    """ Update the timer label """
    global elapsed_time
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_label.config(text=f"{minutes:02}:{seconds:02}")
    if recording:
        elapsed_time += 1
        root.after(1000, update_timer)

def start_recording():
    """ Start the screen recording """
    global recording, output, filename, elapsed_time

    # Disable start button and enable stop button
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)
    
    recording = True
    status_label.config(text="🟢 Recording... Press 'Stop' to finish.")
    elapsed_time = 0  # Reset timer
    update_timer()
    
    # Video writing thread
    Thread(target=record_screen).start()

def stop_recording():
    """ Stop the screen recording """
    global recording, output
    recording = False
    status_label.config(text="🛑 Recording stopped.")
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    
    output.release()
    print(f"✅ Recording saved to {output_path}")

def record_screen():
    """ Record the screen and save video, with mouse capture and overlay """
    global output, recording
    
    while recording:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Write the frame to video
        output.write(frame)
        
        # Update progress bar
        progress['value'] = min((elapsed_time / 60) * 100, 100)
        
        # Show preview window
        cv2.imshow("🎥 Screen Recorder - Preview", frame)
        
        if cv2.waitKey(1) == ord("q"):
            stop_recording()
            break

    cv2.destroyAllWindows()

#============================ Main Loop
root.mainloop()
