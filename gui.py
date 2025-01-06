import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

#for Battery updates
def update_battery_icon(canvas, percentage):
    canvas.create_rectangle(58, 8, 62, 18, fill="#dfe8f7", outline="#0f1a2b")
    fill_width = int(56 * (percentage / 100))
    canvas.create_rectangle(2, 2, 2 + fill_width, 24, fill="#4b637b", outline="#0f1a2b")  
    canvas.create_rectangle(2 + fill_width, 2, 58, 24, fill="#dfe8f7", outline="#0f1a2b") 
    if fill_width == 56:
        canvas.create_rectangle(58, 8, 62, 18, fill="#4b637b")

#for RSSI updates
def update_rssi_icon(canvas, strength):
    for i in range(5):
        fill = "#0f1a2b" if i < strength else "#959799"
        outline = "#0f1a2b" if i < strength else "#959799"
        canvas.create_rectangle(5 + i * 15, 35 - i * 6, 15 + i * 15, 55, fill=fill, outline=outline)

window = tk.Tk()
window.title("AscendOS")
window.geometry("1200x550")  

#for battery and title placement

left_frame = tk.Frame(window, width=200, bg="#d1cfc9")
left_frame.pack(side="left", fill="y")

title_label = tk.Label(left_frame, text="AscendOS", font=("Arial", 30), bg="#d1cfc9", fg="#0f1a2b")
title_label.pack(pady=(40, 10))

battery_frame = tk.Frame(left_frame, bg="#d1cfc9")
battery_frame.pack(pady=(0, 10))

battery_percentage = 25
voltage = 12.5

battery_icon = tk.Canvas(battery_frame, width=64, height=26, highlightthickness=0, bg="#d1cfc9")
battery_icon.pack()
update_battery_icon(battery_icon, battery_percentage)

battery_label = tk.Label(battery_frame, text=f"{battery_percentage}% | {voltage}V", font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
battery_label.pack(side="left")

#For RSSI 
rssi_label = tk.Label(left_frame, text="RSSI:", font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
rssi_label.pack()
rssi_strength = 1
rssi_canvas = tk.Canvas(left_frame, width=100, height=40, highlightthickness=0, bg="#d1cfc9")
rssi_canvas.pack(pady=(0, 10), anchor="center")
update_rssi_icon(rssi_canvas,rssi_strength)

#For IP and RTSP
ip_label = tk.Label(left_frame, text="IP:", bg="#d1cfc9", fg="#0f1a2b")
ip_label.pack()
ip_entry = tk.Entry(left_frame, highlightthickness=1, highlightcolor="#0f1a2b", background="#dfe8f7", foreground="#0f1a2b", relief="flat")
ip_entry.pack(pady=(0, 10))

rtsp_label = tk.Label(left_frame, text="RTSP:", bg="#d1cfc9", fg="#0f1a2b")#0f1a2b
rtsp_label.pack()
rtsp_entry = tk.Entry(left_frame, highlightthickness=1, highlightcolor="#0f1a2b", background="#dfe8f7", foreground="#0f1a2b", relief="flat")
rtsp_entry.pack()

#For flight mode
style = ttk.Style()
style.theme_use("clam") 
style.configure("Custom.TCombobox",
                fieldbackground="#dfe8f7",
                background="#dfe8f7",
                borderwidth=1,
                bordercolor="#0f1a2b",
                relief="flat",
                arrowcolor="#0f1a2b")

flight_modes = ["Manual", "Auto", "Stabilize"]
flight_mode_var = tk.StringVar()

# Adjust label to match theme
flight_mode_label = tk.Label(left_frame, text="Flight Mode:", bg="#d1cfc9", fg="#0f1a2b")
flight_mode_label.pack(pady=(10, 5))

# Apply correct custom style
flight_mode_dropdown = ttk.Combobox(left_frame, textvariable=flight_mode_var, values=flight_modes, style="Custom.TCombobox")
flight_mode_dropdown.pack(pady=(0, 20), padx=5, fill="x")
flight_mode_dropdown.current(0)


#For GPS Info
gps_sats = 0.0
gps_fix = 0.0

gps_sats_label = tk.Label(left_frame, text=f"GPS SATS: {gps_sats}", font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
gps_sats_label.pack()

gps_fix_label = tk.Label(left_frame, text=f"GPS Fix Type: {gps_fix}", font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
gps_fix_label.pack()

#Main view
main_frame = tk.Frame(window, bg="#4c667f")
main_frame.pack(side="right", fill="both", expand=True)

#For longitude latitude and altitude
position_frame = tk.Frame(main_frame, bg="#4c667f")
position_frame.pack(pady=20)

longitude = 0.0
latitude = 0.0
altitude = 0.0

longitude_label = tk.Label(position_frame, text=f"Longitude: {longitude}°", font=("Arial", 14), bg="#4c667f", fg="#d6d4ce")
longitude_label.grid(row=0, column=0, padx=20)

latitude_label = tk.Label(position_frame, text=f"Latitude: {latitude}°", font=("Arial", 14), bg="#4c667f", fg="#d6d4ce")
latitude_label.grid(row=0, column=1, padx=20)

altitude_label = tk.Label(position_frame, text=f"Altitude: {altitude}m", font=("Arial", 14), bg="#4c667f", fg="#d6d4ce")
altitude_label.grid(row=0, column=2, padx=20)

longitude_label.grid(row=0, column=0, padx=20, columnspan=1, sticky="nsew")
latitude_label.grid(row=0, column=1, padx=20, columnspan=1, sticky="nsew")
altitude_label.grid(row=0, column=2, padx=20, columnspan=1, sticky="nsew")

#For both Camera and plane model

display_frame = tk.Frame(main_frame, bg="#4c667f")
display_frame.pack(pady=10, padx=10, fill="both", expand=True)

video_label = tk.Label(display_frame, text="Camera View", font=("Arial", 16), width=50, height=20, bg="gray")
video_label.pack(side="left", padx=20)

map_label = tk.Label(display_frame, text="Map View", font=("Arial", 16), width=50, height=20, bg="black", fg="white")
map_label.pack(side="right", padx=20)

#For roll pitch and yaw
control_frame = tk.Frame(main_frame, bg="#4c667f")
control_frame.pack(pady=20)

roll = 0
pitch = 0
yaw = 0

roll_label = tk.Label(control_frame, text=f"Roll: {roll}°", font=("Arial", 14), bg="#4c667f", fg="#d6d4ce")
roll_label.grid(row=0, column=0, padx=20)

pitch_label = tk.Label(control_frame, text=f"Pitch: {pitch}°", font=("Arial", 14), bg="#4c667f", fg="#d6d4ce")
pitch_label.grid(row=0, column=1, padx=20)

yaw_label = tk.Label(control_frame, text=f"Yaw: {yaw}°", font=("Arial", 14), bg="#4c667f", fg="#d6d4ce")
yaw_label.grid(row=0, column=2, padx=20)

roll_label.grid(row=0, column=0, padx=20, columnspan=1, sticky="nsew")
pitch_label.grid(row=0, column=1, padx=20, columnspan=1, sticky="nsew")
yaw_label.grid(row=0, column=2, padx=20, columnspan=1, sticky="nsew")

# dumbass stream
def update_video_frame():
    ret, frame = cap.read()
    if ret:
        
        video_width = video_label.winfo_width()
        video_height = video_label.winfo_height()

      
        frame = cv2.resize(frame, (600, 200))

        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image)


        video_label.config(image=photo)
        video_label.image = photo


    window.after(10, update_video_frame)


cap = cv2.VideoCapture('rtsp://192.168.144.25:8554/main.264')


update_video_frame()


window.mainloop()


cap.release()
