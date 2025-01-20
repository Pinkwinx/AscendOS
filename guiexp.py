import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import socket
import random
import time
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import traceback
from datetime import datetime

class DarkButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=40, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg="#0f1a2b", highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.normal_bg = "#0f1a2b"
        self.hover_bg = "#1a2738"
        self.click_bg = "#141f2d"
        
        # Create the button shape and text
        self.rect_id = self.create_rectangle(0, 0, width, height, 
                                           fill=self.normal_bg, outline="")
        self.text_id = self.create_text(width/2, height/2, 
                                      text=text, fill="white", 
                                      font=('Arial', 10, 'bold'))
        
        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        self.bind('<ButtonRelease-1>', self.on_release)
        
        # Set cursor
        self.configure(cursor='hand2')
    
    def on_enter(self, event=None):
        self.itemconfig(self.rect_id, fill=self.hover_bg)
    
    def on_leave(self, event=None):
        self.itemconfig(self.rect_id, fill=self.normal_bg)
    
    def on_click(self, event=None):
        self.itemconfig(self.rect_id, fill=self.click_bg)
        if self.command:
            self.command()
    
    def on_release(self, event=None):
        if self.winfo_containing(event.x_root, event.y_root) == self:
            self.itemconfig(self.rect_id, fill=self.hover_bg)
        else:
            self.itemconfig(self.rect_id, fill=self.normal_bg)

class AscendOS:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AscendOS")
        self.window.geometry("1200x550")
        
        # Initialize state variables
        self.is_playing = False
        self.cap = None
        
        # Initialize GPS trail data
        self.gps_trail = {'latitude': [], 'longitude': []}
        
        # Initialize graphs data
        self.graph1_data = {'x': [], 'y': []}
        self.graph2_data = {'x': [], 'y': []}
        
        # Create frames
        self.create_frames()
        
        # Setup UI components
        self.setup_sidebar()
        self.setup_video_page()
        self.setup_graphs_page()
        self.setup_gps_page()
        
        # Start GUI updates
        self.update_gui()
        
        # Set up window close protocol
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_frames(self):
        # Left sidebar
        self.left_frame = tk.Frame(self.window, width=200, bg="#d1cfc9")
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)
        
        # Main content frames
        self.video_frame = tk.Frame(self.window, bg="#4c667f")
        self.graphs_frame = tk.Frame(self.window, bg="#ffffff")
        self.gps_frame = tk.Frame(self.window, bg="#ffffff")
        
        # Start with video frame visible
        self.video_frame.pack(side="right", fill="both", expand=True)

    def setup_sidebar(self):
        # Logo
        try:
            logo_image = Image.open("ASCENDOS.png")
            logo_image = logo_image.resize((170, 100))
            logo_image = ImageTk.PhotoImage(logo_image)
            title_label = tk.Label(self.left_frame, image=logo_image, bg="#d1cfc9")
            title_label.image = logo_image
            title_label.pack(pady=(40, 10))
        except FileNotFoundError:
            title_label = tk.Label(self.left_frame, text="AscendOS", font=("Arial", 30), bg="#d1cfc9", fg="#0f1a2b")
            title_label.pack(pady=(40, 10))

        # Page navigation buttons
        page_buttons_frame = tk.Frame(self.left_frame, bg="#d1cfc9")
        page_buttons_frame.pack(pady=(10, 20))

        button_style = {
            'bg': "#4c667f",
            'fg': "white",
            'relief': "flat",
            'padx': 15,
            'pady': 8,
            'font': ('Arial', 10),
            'width': 10,
            'bd': 0
        }

        self.video_page_btn = tk.Button(page_buttons_frame, text="Video Feed",
                                      command=lambda: self.switch_page(self.video_frame),
                                      **button_style)
        self.video_page_btn.pack(side="left", padx=5)

        self.graphs_page_btn = tk.Button(page_buttons_frame, text="Graphs",
                                       command=lambda: self.switch_page(self.graphs_frame),
                                       **button_style)
        self.graphs_page_btn.pack(side="left", padx=5)

        self.gps_page_btn = tk.Button(page_buttons_frame, text="GPS",
                                    command=lambda: self.switch_page(self.gps_frame),
                                    **button_style)
        self.gps_page_btn.pack(side="left", padx=5)

        # Add hover effects
        def on_enter(e):
            e.widget['background'] = '#5d7b99'

        def on_leave(e):
            e.widget['background'] = '#4c667f'

        for btn in [self.video_page_btn, self.graphs_page_btn, self.gps_page_btn]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Setup other sidebar components
        self.setup_battery_frame()
        self.setup_rssi()
        self.setup_connection_controls()
        self.setup_flight_mode()
        self.setup_gps_info()

    def setup_battery_frame(self):
        battery_frame = tk.Frame(self.left_frame, bg="#d1cfc9")
        battery_frame.pack(pady=(0, 10))

        self.battery_icon = tk.Canvas(battery_frame, width=64, height=26, 
                                    highlightthickness=0, bg="#d1cfc9")
        self.battery_icon.pack()
        self.update_battery_icon(25)  # Default value

        self.battery_label = tk.Label(battery_frame, text="25% | 12.5V", 
                                    font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
        self.battery_label.pack(side="left")

    def setup_rssi(self):
        rssi_label = tk.Label(self.left_frame, text="RSSI:", 
                             font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
        rssi_label.pack()
        self.rssi_canvas = tk.Canvas(self.left_frame, width=100, height=40, 
                                   highlightthickness=0, bg="#d1cfc9")
        self.rssi_canvas.pack(pady=(0, 10), anchor="center")
        self.update_rssi_icon(3)  # Default value

    def setup_connection_controls(self):
        conn_frame = tk.Frame(self.left_frame, bg="#d1cfc9")
        conn_frame.pack(pady=(0, 10))

        # IP entry
        ip_label = tk.Label(conn_frame, text="IP:", bg="#d1cfc9", 
                           fg="#0f1a2b", font=('Arial', 10))
        ip_label.pack()
        self.ip_entry = tk.Entry(conn_frame, 
                                highlightthickness=1, 
                                highlightcolor="#0f1a2b",
                                background="#0f1a2b",
                                foreground="white",
                                insertbackground="white",
                                relief="flat",
                                width=20, 
                                justify='center')
        self.ip_entry.pack(pady=(0, 10))
        self.ip_entry.insert(0, "192.168.144.25")

        # RTSP entry
        rtsp_label = tk.Label(conn_frame, text="RTSP:", bg="#d1cfc9", 
                             fg="#0f1a2b", font=('Arial', 10))
        rtsp_label.pack()
        self.rtsp_entry = tk.Entry(conn_frame, 
                                  highlightthickness=1, 
                                  highlightcolor="#0f1a2b",
                                  background="#0f1a2b",
                                  foreground="white",
                                  insertbackground="white",
                                  relief="flat",
                                  width=20, 
                                  justify='center')
        self.rtsp_entry.pack(pady=(0, 10))
        self.rtsp_entry.insert(0, "8554")

        # Media controls container
        media_container = tk.Frame(conn_frame, bg="#d1cfc9")
        media_container.pack(pady=5)

        # Connect button
        connect_style = {
            'background': "#0f1a2b",
            'foreground': "white",
            'activebackground': '#1a2738',
            'activeforeground': 'white',
            'relief': "flat",
            'padx': 20,
            'pady': 10,
            'font': ('Arial', 10, 'bold'),
            'width': 12,
            'bd': 0,
            'cursor': 'hand2',
            'highlightthickness': 0
        }

        self.connect_button = tk.Button(media_container, 
                                      text="Connect", 
                                      command=self.connect_to_drone,
                                      **connect_style)
        self.connect_button.pack(pady=5)

        # Play button container
        play_container = tk.Frame(media_container, bg="#d1cfc9")
        play_container.pack(pady=5)

        self.play_button = tk.Canvas(play_container, 
                                   width=36, height=36,
                                   bg="#0f1a2b", 
                                   highlightthickness=0,
                                   cursor='hand2')
        self.play_button.pack()
        
        # Draw initial play button state
        self.draw_play_button()
        self.play_button.bind('<Button-1>', self.toggle_playback)
        
        # Add hover effects
        def on_enter(e):
            e.widget['background'] = '#1a2738'
        def on_leave(e):
            e.widget['background'] = '#0f1a2b'
            
        for btn in [self.connect_button, self.play_button]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def setup_flight_mode(self):
        flight_modes = ["Manual", "Auto", "Stabilize"]
        self.flight_mode_var = tk.StringVar()

        flight_mode_label = tk.Label(self.left_frame, text="Flight Mode:", 
                                   bg="#d1cfc9", fg="#0f1a2b")
        flight_mode_label.pack(pady=(10, 5))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
                       fieldbackground="#0f1a2b",
                       background="#0f1a2b",
                       foreground="white",
                       borderwidth=0,
                       relief="flat",
                       arrowcolor="white")

        self.flight_mode_dropdown = ttk.Combobox(self.left_frame, 
                                               textvariable=self.flight_mode_var,
                                               values=flight_modes, 
                                               style="Custom.TCombobox",
                                               justify='center')
        self.flight_mode_dropdown.pack(pady=(0, 20), padx=5, fill="x")
        self.flight_mode_dropdown.current(0)

    def setup_gps_info(self):
        self.gps_sats_label = tk.Label(self.left_frame, text="GPS SATS: 0", 
                                      font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
        self.gps_sats_label.pack()

        self.gps_fix_label = tk.Label(self.left_frame, text="GPS Fix Type: 0", 
                                     font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
        self.gps_fix_label.pack()

    def setup_video_page(self):
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(fill="both", expand=True)

    def setup_graphs_page(self):
        self.graphs_frame.configure(bg="#d1cfc9")
        graphs_container = tk.Frame(self.graphs_frame, bg="#d1cfc9")
        graphs_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create frames for each graph
        graph1_frame = tk.Frame(graphs_container, bg="#ffffff", relief="solid", borderwidth=1)
        graph1_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        graph2_frame = tk.Frame(graphs_container, bg="#ffffff", relief="solid", borderwidth=1)
        graph2_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Setup both graphs
        self.setup_graph(graph1_frame, 1)
        self.setup_graph(graph2_frame, 2)

    def setup_graph(self, parent_frame, graph_num):
        controls_frame = tk.Frame(parent_frame, bg="#ffffff")
        controls_frame.pack(fill="x", pady=5)

title = tk.Label(controls_frame, text=f"Graph {graph_num}", 
                        font=("Arial", 12, "bold"), bg="#ffffff", fg="#0f1a2b")
        title.pack(side="left", padx=15)

        # Buttons frame
        buttons_frame = tk.Frame(controls_frame, bg="#ffffff")
        buttons_frame.pack(side="right", padx=15)

        load_btn = DarkButton(buttons_frame, text="Load Data",
                           command=lambda: self.load_graph_data(graph_num),
                           width=100, height=30)
        load_btn.pack(side="left", padx=5)

        export_btn = DarkButton(buttons_frame, text="Export Data",
                             command=lambda: self.export_graph_data(graph_num),
                             width=100, height=30)
        export_btn.pack(side="left", padx=5)

        # Create frame for matplotlib
        plot_frame = tk.Frame(parent_frame, bg="#ffffff")
        plot_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create matplotlib figure
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # Style the plot
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        ax.plot([], [], '-', color='#4c667f', linewidth=2)
        ax.grid(True, linestyle='--', alpha=0.3, color='#4c667f')
        
        # Configure spines
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#4c667f')
            
        # Set labels
        ax.set_xlabel('X Axis', color='#0f1a2b')
        ax.set_ylabel('Y Axis', color='#0f1a2b')
        ax.set_title(f'Graph {graph_num}', color='#0f1a2b', pad=10)
        ax.tick_params(colors='#0f1a2b', which='both')

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(highlightthickness=0)
        canvas_widget.pack(fill="both", expand=True)
        
        fig.tight_layout()
        canvas.draw()

        # Store references
        if graph_num == 1:
            self.fig1, self.ax1, self.canvas1 = fig, ax, canvas
        else:
            self.fig2, self.ax2, self.canvas2 = fig, ax, canvas

    def setup_gps_page(self):
        # Main container
        gps_container = tk.Frame(self.gps_frame, bg="#ffffff", padx=20, pady=20)
        gps_container.pack(fill="both", expand=True)

        # Title and controls
        header_frame = tk.Frame(gps_container, bg="#ffffff")
        header_frame.pack(fill="x", pady=(0, 20))

        title = tk.Label(header_frame, text="GPS Position", 
                        font=("Arial", 16, "bold"), bg="#ffffff", fg="#0f1a2b")
        title.pack(side="left")

        # GPS data display
        data_frame = tk.Frame(gps_container, bg="#ffffff")
        data_frame.pack(fill="x", pady=(0, 20))

        metrics_style = {
            'bg': "#ffffff",
            'relief': "solid",
            'borderwidth': 1,
            'padx': 20,
            'pady': 10
        }

        # Latitude display
        lat_frame = tk.Frame(data_frame, **metrics_style)
        lat_frame.pack(side="left", expand=True, padx=5)
        
        tk.Label(lat_frame, text="Latitude", font=("Arial", 12),
                bg="#ffffff", fg="#0f1a2b").pack()
        self.lat_value = tk.Label(lat_frame, text="0.000°", 
                                font=("Arial", 14, "bold"),
                                bg="#ffffff", fg="#4c667f")
        self.lat_value.pack()

        # Longitude display
        lon_frame = tk.Frame(data_frame, **metrics_style)
        lon_frame.pack(side="left", expand=True, padx=5)
        
        tk.Label(lon_frame, text="Longitude", font=("Arial", 12),
                bg="#ffffff", fg="#0f1a2b").pack()
        self.lon_value = tk.Label(lon_frame, text="0.000°", 
                                font=("Arial", 14, "bold"),
                                bg="#ffffff", fg="#4c667f")
        self.lon_value.pack()

        # Altitude display
        alt_frame = tk.Frame(data_frame, **metrics_style)
        alt_frame.pack(side="left", expand=True, padx=5)
        
        tk.Label(alt_frame, text="Altitude", font=("Arial", 12),
                bg="#ffffff", fg="#0f1a2b").pack()
        self.alt_value = tk.Label(alt_frame, text="0.0m", 
                                font=("Arial", 14, "bold"),
                                bg="#ffffff", fg="#4c667f")
        self.alt_value.pack()

        # Map frame
        map_frame = tk.Frame(gps_container, bg="#ffffff", relief="solid", borderwidth=1)
        map_frame.pack(fill="both", expand=True, pady=(20, 0))

        # Create matplotlib figure for the map
        self.map_fig = Figure(figsize=(8, 6), dpi=100)
        self.map_ax = self.map_fig.add_subplot(111)
        
        # Style the map
        self.map_fig.patch.set_facecolor('#ffffff')
        self.map_ax.set_facecolor('#f0f0f0')
        
        # Set labels and grid
        self.map_ax.set_xlabel('Longitude', color='#0f1a2b')
        self.map_ax.set_ylabel('Latitude', color='#0f1a2b')
        self.map_ax.grid(True, linestyle='--', alpha=0.3, color='#4c667f')
        
        # Create canvas
        self.map_canvas = FigureCanvasTkAgg(self.map_fig, master=map_frame)
        self.map_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize empty map
        self.update_map()

    def update_map(self):
        if hasattr(self, 'map_ax'):
            self.map_ax.clear()
            
            if self.gps_trail['latitude'] and self.gps_trail['longitude']:
                # Plot the GPS trail
                self.map_ax.plot(self.gps_trail['longitude'], 
                               self.gps_trail['latitude'],
                               '-', color='#4c667f', linewidth=2)
                
                # Plot current position
                self.map_ax.plot(self.gps_trail['longitude'][-1],
                               self.gps_trail['latitude'][-1],
                               'o', color='#ff4444', markersize=8)
                
                # Set limits with padding
                pad = 0.0001
                self.map_ax.set_xlim(min(self.gps_trail['longitude']) - pad,
                                   max(self.gps_trail['longitude']) + pad)
                self.map_ax.set_ylim(min(self.gps_trail['latitude']) - pad,
                                   max(self.gps_trail['latitude']) + pad)
            
            # Style the map
            self.map_ax.grid(True, linestyle='--', alpha=0.3, color='#4c667f')
            self.map_ax.set_xlabel('Longitude', color='#0f1a2b')
            self.map_ax.set_ylabel('Latitude', color='#0f1a2b')
            
            # Update canvas
            self.map_canvas.draw()

    def draw_play_button(self):
        self.play_button.delete("all")
        if not self.is_playing:
            # Draw play triangle
            self.play_button.create_polygon(12, 8, 12, 28, 28, 18, 
                                          fill="white", outline="white")
        else:
            # Draw pause bars
            self.play_button.create_rectangle(11, 8, 17, 28, 
                                            fill="white", outline="white")
            self.play_button.create_rectangle(23, 8, 29, 28, 
                                            fill="white", outline="white")

    def update_battery_icon(self, percentage):
        self.battery_icon.delete("all")
        self.battery_icon.create_rectangle(58, 8, 62, 18, fill="#dfe8f7", outline="#0f1a2b")
        fill_width = int(56 * (percentage / 100))
        self.battery_icon.create_rectangle(2, 2, 2 + fill_width, 24, fill="#4b637b", outline="#0f1a2b")
        self.battery_icon.create_rectangle(2 + fill_width, 2, 58, 24, fill="#dfe8f7", outline="#0f1a2b")
        if fill_width == 56:
            self.battery_icon.create_rectangle(58, 8, 62, 18, fill="#4b637b")

    def update_rssi_icon(self, strength):
        self.rssi_canvas.delete("all")
        for i in range(5):
            fill = "#0f1a2b" if i < strength else "#959799"
            outline = "#0f1a2b" if i < strength else "#959799"
            self.rssi_canvas.create_rectangle(5 + i * 15, 35 - i * 6, 
                                            15 + i * 15, 55, 
                                            fill=fill, outline=outline)

    def toggle_playback(self, event=None):
        self.is_playing = not self.is_playing
        self.draw_play_button()
        
        if self.is_playing:
            print("Starting stream...")
            try:
                if not self.cap:
                    ip = self.ip_entry.get()
                    rtsp = self.rtsp_entry.get()
                    rtsp_url = f"rtsp://{ip}:{rtsp}/main.264"
                    self.cap = cv2.VideoCapture(rtsp_url)
                    
                    if not self.cap.isOpened():
                        raise Exception("Failed to open video stream")
                    
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                self.update_video_frame()
                
            except Exception as e:
                print(f"Error starting stream: {e}")
                self.is_playing = False
                self.draw_play_button()
                messagebox.showerror("Error", f"Failed to start video stream: {str(e)}")
        else:
            print("Stopping stream...")
            if self.cap:
                self.cap.release()
                self.cap = None
            
            self.video_label.config(image='')
            self.video_label.image = None

def connect_to_drone(self):
        try:
            ip = self.ip_entry.get()
            rtsp = self.rtsp_entry.get()
            
            self.connect_button.config(text="Connecting...", state="disabled")
            
            if self.cap is not None:
                self.cap.release()
            
            rtsp_url = f"rtsp://{ip}:{rtsp}/main.264"
            self.cap = cv2.VideoCapture(rtsp_url)
            
            if self.cap.isOpened():
                self.connect_button.config(text="Connected", background="#4CAF50", foreground="white")
            else:
                self.connect_button.config(text="Connect", state="normal", background="#0f1a2b", foreground="white")
                raise Exception("Failed to connect to video stream")
                
        except Exception as e:
            print(f"Connection error: {e}")
            self.connect_button.config(text="Connect", state="normal", background="#0f1a2b", foreground="white")

    def update_video_frame(self):
        if not self.is_playing or not self.cap:
            return
            
        try:
            # Skip frames to reduce latency
            for _ in range(5):
                self.cap.grab()
            
            ret, frame = self.cap.retrieve()
            if not ret:
                print("Error: Couldn't read frame")
                self.is_playing = False
                self.draw_play_button()
                self.cap.release()
                self.cap = None
                return

            data = self.get_server_data()
            battery_percentage, rssi_strength, gps_sats, gps_fix, longitude, latitude, altitude, roll, pitch, yaw, battery_voltages, total_voltage = data

            # Add overlay
            overlay = frame.copy()
            cv2.rectangle(overlay, (5, 5), (400, 80), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

            # Add text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            font_thickness = 2
            font_color = (214, 212, 206)
            
            position_text = f"Long: {longitude:.2f}° | Lat: {latitude:.2f}° | Alt: {altitude:.2f}m"
            cv2.putText(frame, position_text, (10, 30), font, font_scale, font_color, font_thickness)
            
            orientation_text = f"Roll: {roll:.2f