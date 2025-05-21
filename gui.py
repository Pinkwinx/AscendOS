import tkinter as tk
from tkinter import ttk, filedialog
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
import tkintermapview
import os
from threading import Timer

class AscendOS:
    # Color scheme
    SIDEBAR_BG = "#d1cfc9"       
    BUTTON_BG = "#4c667f"       
    BUTTON_HOVER = "#5d7b99"    
    TEXT_DARK = "#0f1a2b"        
    VIDEO_BG = "#4c667f"         
    CONTENT_BG = "#ffffff"       # White for content background
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AscendOS")
        self.window.geometry("1200x550")
        
        # Set consistent style for all buttons
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Custom.TButton',
                           background=self.BUTTON_BG,
                           foreground=self.CONTENT_BG,  # White text
                           relief="flat",
                           font=('Arial', 10),
                           padding=8)
        
        # Initialize state variables
        self.is_playing = False
        self.cap = None
        self.current_latitude = None
        self.current_longitude = None
        self.position_history = []
        self.trail_path = None
        self.first_real_position = False
        
        # Create frames
        self.left_frame = tk.Frame(self.window, width=200, bg=self.SIDEBAR_BG)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)
        
        # Main content frames
        self.video_frame = tk.Frame(self.window, bg=self.VIDEO_BG)
        self.graphs_frame = tk.Frame(self.window, bg=self.CONTENT_BG)
        self.map_frame = tk.Frame(self.window, bg=self.CONTENT_BG)
        
        # Setup all components
        self.setup_sidebar()
        self.setup_video_page()
        self.setup_graphs_page()
        self.setup_map_page()
        
        # Start with video frame visible
        self.video_frame.pack(side="right", fill="both", expand=True)
        
        # Initialize graphs data
        self.graph1_data = {'x': [], 'y': []}
        self.graph2_data = {'x': [], 'y': []}
        
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
        self.map_frame = tk.Frame(self.window, bg="#ffffff")
        
        # Setup all components
        self.setup_sidebar()
        self.setup_video_page()
        self.setup_graphs_page()
        self.setup_map_page()
        
        # Start with video frame visible
        self.video_frame.pack(side="right", fill="both", expand=True)
        
        # Create frames
        self.create_frames()
        
        # Setup UI components
        self.setup_sidebar()
        self.setup_video_page()
        self.setup_graphs_page()
        self.setup_map_page()
        
        # Initialize graphs data
        self.graph1_data = {'x': [], 'y': []}
        self.graph2_data = {'x': [], 'y': []}
        
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
        self.map_frame = tk.Frame(self.window, bg="#ffffff")
        
        # Start with video frame visible
        self.video_frame.pack(side="right", fill="both", expand=True)

    def setup_battery_frame(self):
        battery_frame = tk.Frame(self.left_frame, bg=self.SIDEBAR_BG)
        battery_frame.pack(pady=(0, 10))

        self.battery_icon = tk.Canvas(battery_frame, width=64, height=26, highlightthickness=0, bg=self.SIDEBAR_BG)
        self.battery_icon.pack()
        self.update_battery_icon(25)  # Default value

        self.battery_label = tk.Label(battery_frame, text="25% | 12.5V", 
                                    font=("Arial", 14), bg="#d1cfc9", fg="#0f1a2b")
        self.battery_label.pack(side="left")

    def setup_sidebar(self):
        # Logo
        try:
            logo_image = Image.open("ASCENDOS.png")
            logo_image = logo_image.resize((170, 100))
            logo_image = ImageTk.PhotoImage(logo_image)
            title_label = tk.Label(self.left_frame, image=logo_image, bg=self.SIDEBAR_BG)
            title_label.image = logo_image
            title_label.pack(pady=(40, 10))
        except FileNotFoundError:
            title_label = tk.Label(self.left_frame, text="AscendOS", 
                                 font=("Arial", 30), bg=self.SIDEBAR_BG, 
                                 fg=self.TEXT_DARK)
            title_label.pack(pady=(40, 10))

        # Create a frame for the navigation buttons
        nav_buttons_frame = tk.Frame(self.left_frame, bg=self.SIDEBAR_BG)
        nav_buttons_frame.pack(pady=(10, 20), fill="x", padx=10)

        # Create buttons using ttk
        self.video_page_btn = ttk.Button(nav_buttons_frame, text="Video Feed",
                                     command=lambda: self.switch_page(self.video_frame),
                                     style='Custom.TButton')
        self.video_page_btn.pack(fill="x", pady=2)

        self.graphs_page_btn = ttk.Button(nav_buttons_frame, text="Graphs",
                                      command=lambda: self.switch_page(self.graphs_frame),
                                      style='Custom.TButton')
        self.graphs_page_btn.pack(fill="x", pady=2)

        self.map_page_btn = ttk.Button(nav_buttons_frame, text="Map View",
                                   command=lambda: self.switch_page(self.map_frame),
                                   style='Custom.TButton')
        self.map_page_btn.pack(fill="x", pady=2)

        # Battery frame
        self.setup_battery_frame()
        
        # RSSI
        self.setup_rssi()
        
        # Connection controls
        self.setup_connection_controls()
        
        # Flight mode
        self.setup_flight_mode()
        
        # GPS Info
        self.setup_gps_info()

    def setup_battery_frame(self):
        battery_frame = tk.Frame(self.left_frame, bg=self.SIDEBAR_BG)
        battery_frame.pack(pady=(0, 10))

        self.battery_icon = tk.Canvas(battery_frame, width=64, height=26, 
                                    highlightthickness=0, bg=self.SIDEBAR_BG)
        self.battery_icon.pack()
        self.update_battery_icon(25)  # Default value

        self.battery_label = tk.Label(battery_frame, text="25% | 12.5V", 
                                    font=("Arial", 14), bg=self.SIDEBAR_BG, 
                                    fg=self.TEXT_DARK)
        self.battery_label.pack(side="left")

    def setup_rssi(self):
        rssi_label = tk.Label(self.left_frame, text="RSSI:", 
            font=("Arial", 14), bg=self.SIDEBAR_BG, fg=self.TEXT_DARK)
        rssi_label.pack()
        self.rssi_canvas = tk.Canvas(self.left_frame, width=100, height=40, 
            highlightthickness=0, bg=self.SIDEBAR_BG)
        self.rssi_canvas.pack(pady=(0, 10), anchor="center")
        self.update_rssi_icon(3)

    def setup_connection_controls(self):
        # Connection controls container
        conn_frame = tk.Frame(self.left_frame, bg=self.SIDEBAR_BG)
        conn_frame.pack(pady=(0, 10))

        # IP entry
        ip_label = tk.Label(conn_frame, text="IP:", bg=self.SIDEBAR_BG, fg=self.TEXT_DARK, font=('Arial', 10))
        ip_label.pack()
        self.ip_entry = tk.Entry(conn_frame, 
                                highlightthickness=1, 
                                highlightcolor=self.TEXT_DARK,
                                background=self.TEXT_DARK,
                                foreground=self.CONTENT_BG,
                                insertbackground=self.CONTENT_BG,
                                relief="flat",
                                width=20, 
                                justify='center')
        self.ip_entry.pack(pady=(0, 10))
        self.ip_entry.insert(0, "192.168.144.25")

        # RTSP entry
        rtsp_label = tk.Label(conn_frame, text="RTSP:", bg=self.SIDEBAR_BG, fg=self.TEXT_DARK, font=('Arial', 10))
        rtsp_label.pack()
        self.rtsp_entry = tk.Entry(conn_frame, 
                                  highlightthickness=1, 
                                  highlightcolor=self.TEXT_DARK,
                                  background=self.TEXT_DARK,
                                  foreground=self.CONTENT_BG,
                                  insertbackground=self.CONTENT_BG,
                                  relief="flat",
                                  width=20, 
                                  justify='center')
        self.rtsp_entry.pack(pady=(0, 10))
        self.rtsp_entry.insert(0, "8554")

        # Button container for media controls
        media_container = tk.Frame(conn_frame, bg=self.SIDEBAR_BG)
        media_container.pack(pady=5)

        # Connect button with updated style
        connect_style = {
            'background': self.TEXT_DARK,
            'foreground': self.CONTENT_BG,
            'activebackground': self.BUTTON_HOVER,
            'activeforeground': self.CONTENT_BG,
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

        # Play/Pause button in its own container
        play_container = tk.Frame(media_container, bg=self.SIDEBAR_BG)
        play_container.pack(pady=5)

        self.play_button = tk.Canvas(play_container, 
            width=36, height=36,
            bg=self.TEXT_DARK, 
            highlightthickness=0,
            cursor='hand2')
        self.play_button.pack()

    def setup_flight_mode(self):
        flight_modes = ["Manual", "Auto", "Stabilize"]
        self.flight_mode_var = tk.StringVar()

        flight_mode_label = tk.Label(self.left_frame, text="Flight Mode:", 
            bg=self.SIDEBAR_BG, fg=self.TEXT_DARK)
        flight_mode_label.pack(pady=(10, 5))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TCombobox",
            fieldbackground=self.TEXT_DARK,
            background=self.TEXT_DARK,
            foreground=self.CONTENT_BG,
            borderwidth=0,
            relief="flat",
            arrowcolor=self.CONTENT_BG)

        self.flight_mode_dropdown = ttk.Combobox(self.left_frame, 
            textvariable=self.flight_mode_var,
            values=flight_modes, 
            style="Custom.TCombobox",
            justify='center')
        self.flight_mode_dropdown.pack(pady=(0, 20), padx=5, fill="x")
        self.flight_mode_dropdown.current(0)

    def setup_gps_info(self):
        self.gps_sats_label = tk.Label(self.left_frame, text="GPS SATS: 0", 
            font=("Arial", 14), bg=self.SIDEBAR_BG, fg=self.TEXT_DARK)
        self.gps_sats_label.pack()

        self.gps_fix_label = tk.Label(self.left_frame, text="GPS Fix Type: 0", 
            font=("Arial", 14), bg=self.SIDEBAR_BG, fg=self.TEXT_DARK)
        self.gps_fix_label.pack()

    def setup_battery_frame(self):
        battery_frame = tk.Frame(self.left_frame, bg=self.SIDEBAR_BG)
        battery_frame.pack(pady=(0, 10))

        self.battery_icon = tk.Canvas(battery_frame, width=64, height=26, 
            highlightthickness=0, bg=self.SIDEBAR_BG)
        self.battery_icon.pack()
        self.update_battery_icon(25)  # Default value

        self.battery_label = tk.Label(battery_frame, text="25% | 12.5V", 
            font=("Arial", 14), bg=self.SIDEBAR_BG, fg=self.TEXT_DARK)
        self.battery_label.pack(side="left")  # Default value

    def setup_connection_controls(self):
        # Connection controls container
        conn_frame = tk.Frame(self.left_frame, bg=self.SIDEBAR_BG)
        conn_frame.pack(pady=(0, 10))

        # IP entry
        ip_label = tk.Label(conn_frame, text="IP:", bg=self.SIDEBAR_BG, fg="#0f1a2b", font=('Arial', 10))
        ip_label.pack()
        self.ip_entry = tk.Entry(conn_frame, 
                                highlightthickness=1, 
                                highlightcolor="#0f1a2b",
                                background="#0f1a2b",
                                foreground="white",
                                insertbackground="white",  # Cursor color
                                relief="flat",
                                width=20, 
                                justify='center')
        self.ip_entry.pack(pady=(0, 10))
        self.ip_entry.insert(0, "192.168.144.25")

        # RTSP entry
        rtsp_label = tk.Label(conn_frame, text="RTSP:", bg= self.SIDEBAR_BG, fg="#0f1a2b", font=('Arial', 10))
        rtsp_label.pack()
        self.rtsp_entry = tk.Entry(conn_frame, 
                                  highlightthickness=1, 
                                  highlightcolor="#0f1a2b",
                                  background="#0f1a2b",
                                  foreground="white",
                                  insertbackground="white",  # Cursor color
                                  relief="flat",
                                  width=20, 
                                  justify='center')
        self.rtsp_entry.pack(pady=(0, 10))
        self.rtsp_entry.insert(0, "8554")

        # Button container for media controls
        media_container = tk.Frame(conn_frame, bg=self.SIDEBAR_BG)
        media_container.pack(pady=5)

        # Connect button with updated style
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
        self.connect_button.pack(pady=5)  # Stack vertically

        # Play/Pause button in its own container
        play_container = tk.Frame(media_container, bg=self.SIDEBAR_BG)
        play_container.pack(pady=5)

        self.play_button = tk.Canvas(play_container, 
                                   width=36, height=36,
                                   bg="#0f1a2b", 
                                   highlightthickness=0,
                                   cursor='hand2')
        self.play_button.pack()
        
        # Draw initial play triangle
        self.draw_play_button()
        
        # Bind click event
        self.play_button.bind('<Button-1>', self.toggle_playback)
        self.is_playing = False
        
        # Add hover effects
        def on_enter(e):
            e.widget['background'] = '#1a2738'
        def on_leave(e):
            e.widget['background'] = '#0f1a2b'
            
        for btn in [self.connect_button, self.play_button]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

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

    def setup_flight_mode(self):
        flight_modes = ["Manual", "Auto", "Stabilize"]
        self.flight_mode_var = tk.StringVar()

        flight_mode_label = tk.Label(self.left_frame, text="Flight Mode:", bg=self.SIDEBAR_BG, fg=self.TEXT_DARK)
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
                                      font=("Arial", 14), bg=self.SIDEBAR_BG, fg="#0f1a2b")
        self.gps_sats_label.pack()

        self.gps_fix_label = tk.Label(self.left_frame, text="GPS Fix Type: 0", 
                                     font=("Arial", 14), bg=self.SIDEBAR_BG, fg="#0f1a2b")
        self.gps_fix_label.pack()

    def setup_video_page(self):
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(fill="both", expand=True)

    def setup_map_page(self):
        # Create frame for coordinates display
        coords_frame = tk.Frame(self.map_frame, bg="#ffffff")
        coords_frame.pack(fill="x", pady=5)

        # Create label for coordinates
        self.coords_label = tk.Label(coords_frame,
                                   text="Current Position: 0.000000°, 0.000000°",
                                   font=('Arial', 12),
                                   bg="#ffffff")
        self.coords_label.pack(pady=5)

        # Add clear trail button
        self.clear_trail_btn = tk.Button(coords_frame,
                                       text="Clear Trail",
                                       command=self.clear_trail,
                                       bg="#0f1a2b",
                                       fg="white",
                                       font=('Arial', 10))
        self.clear_trail_btn.pack(pady=5)

        # Create map widget
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Set initial map position
        self.map_widget.set_position(0, 0)  # Default position
        self.map_widget.set_zoom(15)

        # Create marker for drone position
        self.drone_marker = None
        # Initialize trail path
        self.trail_path = None
        self.update_map_position()

    def clear_trail(self):
        """Clear the trail history and remove it from the map"""
        if self.trail_path:
            self.trail_path.delete()
            self.trail_path = None
        self.position_history = []

    def update_map_position(self):
        """Update the map with current coordinates"""
        try:
            # Update coordinates label
            self.coords_label.config(
                text=f"Current Position: {self.current_latitude:.6f}°, {self.current_longitude:.6f}°"
            )

            # Add current position to history if it's different from the last position
            current_pos = (self.current_latitude, self.current_longitude)
            if not self.position_history or current_pos != self.position_history[-1]:
                self.position_history.append(current_pos)

                # Limit trail length if needed (e.g., keep last 1000 points)
                if len(self.position_history) > 1000:
                    self.position_history.pop(0)

            # Update or create drone marker
            if self.drone_marker:
                self.drone_marker.set_position(self.current_latitude, self.current_longitude)
            else:
                self.drone_marker = self.map_widget.set_marker(
                    self.current_latitude,
                    self.current_longitude,
                    text="Drone"
                )

            # Update or create trail path
            if len(self.position_history) > 1:
                if self.trail_path:
                    self.trail_path.delete()
                self.trail_path = self.map_widget.set_path(self.position_history, 
                                                         color="red",
                                                         width=2)

            # Center map on drone position
            self.map_widget.set_position(self.current_latitude, self.current_longitude)

        except Exception as e:
            print(f"Error updating map position: {e}")

    def refresh_map(self):
        """Refresh the map with current coordinates"""
        self.update_map_position()

    def setup_graphs_page(self):
        # Main container with background color
        self.graphs_frame.configure(bg=self.SIDEBAR_BG)
        
        # Container for graphs with padding
        graphs_container = tk.Frame(self.graphs_frame, bg=self.SIDEBAR_BG)
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
        # Title and controls frame
        controls_frame = tk.Frame(parent_frame, bg="#ffffff")
        controls_frame.pack(fill="x", pady=5)

        title = tk.Label(controls_frame, text=f"Graph {graph_num}", 
                        font=("Arial", 12, "bold"), bg="#ffffff", fg="#0f1a2b")
        title.pack(side="left", padx=15)

        # Buttons frame
        buttons_frame = tk.Frame(controls_frame, bg="#ffffff")
        buttons_frame.pack(side="right", padx=15)

        graph_button_style = {
            'background': "#0f1a2b",
            'foreground': "white",
            'activebackground': '#1a2738',
            'activeforeground': 'white',
            'relief': "flat",
            'padx': 10,
            'pady': 5,
            'font': ('Arial', 9, 'bold'),
            'width': 10,
            'bd': 0,
            'cursor': 'hand2'
        }

        load_btn = tk.Button(buttons_frame, text="Load Data",
                           command=lambda: self.load_graph_data(graph_num),
                           **graph_button_style)
        load_btn.pack(side="left", padx=5)

        export_btn = tk.Button(buttons_frame, text="Export Data",
                             command=lambda: self.export_graph_data(graph_num),
                             **graph_button_style)
        export_btn.pack(side="left", padx=5)

        # Add hover effects
        def on_enter(e):
            e.widget['background'] = '#1a2738'

        def on_leave(e):
            e.widget['background'] = '#0f1a2b'

        for btn in [load_btn, export_btn]:
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Create frame for matplotlib
        plot_frame = tk.Frame(parent_frame, bg="#ffffff")
        plot_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create matplotlib figure
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # Style the plot
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        
        # Initialize empty plot
        ax.plot([], [], '-', color='#4c667f', linewidth=2)
        
        # Configure grid and spines
        ax.grid(True, linestyle='--', alpha=0.3, color='#4c667f')
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#4c667f')
            
        # Set labels
        ax.set_xlabel('X Axis', color='#0f1a2b')
        ax.set_ylabel('Y Axis', color='#0f1a2b')
        ax.set_title(f'Graph {graph_num}', color='#0f1a2b', pad=10)
        
        # Style ticks
        ax.tick_params(colors='#0f1a2b', which='both')

        # Create canvas and pack it
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(highlightthickness=0)
        canvas_widget.pack(fill="both", expand=True)
        
        # Force a draw
        fig.tight_layout()
        canvas.draw()

        # Store references
        if graph_num == 1:
            self.fig1, self.ax1, self.canvas1 = fig, ax, canvas
        else:
            self.fig2, self.ax2, self.canvas2 = fig, ax, canvas

    def toggle_playback(self, event=None):
        self.is_playing = not self.is_playing
        self.draw_play_button()
        
        if self.is_playing:
            print("Starting stream...")
            try:
                # Initialize video capture
                if not self.cap:
                    ip = self.ip_entry.get()
                    rtsp = self.rtsp_entry.get()
                    rtsp_url = f"rtsp://{ip}:{rtsp}/main.264"
                    self.cap = cv2.VideoCapture(rtsp_url)
                    
                    if not self.cap.isOpened():
                        raise Exception("Failed to open video stream")
                    
                    # Optimize capture settings for low latency
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
                    self.cap.set(cv2.CAP_PROP_FPS, 30)
                    
                    # Additional settings to minimize latency
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                # Start the video update loop
                self.update_video_frame()
                
            except Exception as e:
                print(f"Error starting stream: {e}")
                self.is_playing = False
                self.draw_play_button()
                tk.messagebox.showerror("Error", f"Failed to start video stream: {str(e)}")
        else:
            print("Stopping stream...")
            # Stop the video stream
            if self.cap:
                self.cap.release()
                self.cap = None
            
            # Clear the video display
            self.video_label.config(image='')
            self.video_label.image = None

    def load_graph_data(self, graph_num):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            if not file_path:
                return

            x_data = []
            y_data = []
            
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and '|' in line:
                        try:
                            x_str, y_str = line.split('|', 1)
                            x = float(x_str.strip())
                            y = float(y_str.strip())
                            x_data.append(x)
                            y_data.append(y)
                        except ValueError as e:
                            print(f"Skipping invalid line: {line}, Error: {e}")
                            continue

            if not x_data or not y_data:
                tk.messagebox.showwarning("Warning", "No valid data points found in file")
                return

            # Update data storage
            if graph_num == 1:
                self.graph1_data = {'x': x_data, 'y': y_data}
            else:
                self.graph2_data = {'x': x_data, 'y': y_data}

            self.update_graph(graph_num)
            
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "File not found")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error loading data: {str(e)}")
            print(f"Error details: {e}")

    def export_graph_data(self, graph_num):
        data = self.graph1_data if graph_num == 1 else self.graph2_data
        if not data['x']:
            tk.messagebox.showwarning("Warning", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w') as file:
                for x, y in zip(data['x'], data['y']):
                    file.write(f"{x}|{y}\n")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error exporting data: {str(e)}")

    def update_graph(self, graph_num):
        try:
            if graph_num == 1:
                data = self.graph1_data
                ax = self.ax1
                canvas = self.canvas1
                fig = self.fig1
            else:
                data = self.graph2_data
                ax = self.ax2
                canvas = self.canvas2
                fig = self.fig2

            # Clear previous plot
            ax.clear()
            
            # Plot new data
            if data['x'] and data['y']:
                # Create the line plot
                ax.plot(data['x'], data['y'], '-', color='#4c667f', linewidth=2, label='Data')
                
                # Set the limits slightly larger than the data range
                x_margin = (max(data['x']) - min(data['x'])) * 0.05
                y_margin = (max(data['y']) - min(data['y'])) * 0.05
                ax.set_xlim(min(data['x']) - x_margin, max(data['x']) + x_margin)
                ax.set_ylim(min(data['y']) - y_margin, max(data['y']) + y_margin)
                
                # Style the plot
                ax.grid(True, linestyle='--', alpha=0.3, color='#4c667f')
                for spine in ax.spines.values():
                    spine.set_visible(True)
                    spine.set_color('#4c667f')
                
                # Set labels
                ax.set_xlabel('X Axis', color='#0f1a2b')
                ax.set_ylabel('Y Axis', color='#0f1a2b')
                ax.set_title(f'Graph {graph_num}', color='#0f1a2b', pad=10)
                
                # Style ticks
                ax.tick_params(colors='#0f1a2b', which='both')
                
                # Update layout and redraw
                fig.tight_layout()
                canvas.draw()
                
        except Exception as e:
            print(f"Error updating graph: {e}")
            import traceback
            print(traceback.format_exc())
            tk.messagebox.showerror("Error", f"Error updating graph: {str(e)}")

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
            self.rssi_canvas.create_rectangle(5 + i * 15, 35 - i * 6, 15 + i * 15, 55, 
                                           fill=fill, outline=outline)

    def get_server_data(self, file_path="output.txt"):
        # Default random values for variables
        battery_percentage = random.randint(0, 100)
        rssi_strength = random.randint(0, 5)
        gps_sats = random.randint(0, 12)
        gps_fix = random.choice([0, 1, 2])
        longitude = random.uniform(-180, 180)
        latitude = random.uniform(-90, 90)
        altitude = random.uniform(0, 5000)
        roll = random.uniform(-180, 180)
        pitch = random.uniform(-90, 90)
        yaw = random.uniform(-180, 180)
        battery_voltages = [random.uniform(3.0, 4.2) for _ in range(6)]
        total_voltage = sum(battery_voltages)

        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                last_line = next((line.strip() for line in reversed(lines) if line.strip()), None)
                
                if last_line:
                    values = last_line.split("|")
                    
                    try:
                        pitch = float(values[0]) if values[0] else 0.0
                        roll = float(values[1]) if values[1] else 0.0
                        yaw = float(values[2]) if values[2] else 0.0
                        
                        battery_voltages = [float(v) if v else 0.0 for v in values[3:9]]
                        total_voltage = float(values[9]) if values[9] else 0.0
                        
                        latitude = float(values[10]) if values[10] else 0.0
                        longitude = float(values[11]) if values[11] else 0.0
                        altitude = float(values[12]) if values[12] else 0.0
                        
                        battery_percentage = (total_voltage / (4.2 * 6)) * 100
                        battery_percentage = round(battery_percentage, 2)
                        battery_percentage = min(max(battery_percentage, 0), 100)
                    except ValueError as e:
                        print(f"Error processing line values: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

        return (battery_percentage, rssi_strength, gps_sats, gps_fix, 
                longitude, latitude, altitude, roll, pitch, yaw, 
                battery_voltages, total_voltage)

    def setup_video_capture(self):
        try:
            self.cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/main.264")
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
            self.cap.set(cv2.CAP_PROP_FPS, 30)
        except Exception as e:
            print(f"Error initializing video capture: {e}")
            self.cap = None

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
                self.connect_button.config(text="Connected", bg="#4CAF50", fg="white")
            else:
                self.connect_button.config(text="Connect", state="normal", bg="#f0f0f0", fg="black")
                raise Exception("Failed to connect to video stream")
                
        except Exception as e:
            print(f"Connection error: {e}")
            self.connect_button.config(text="Connect", state="normal", bg="#f0f0f0", fg="black")

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
            
            orientation_text = f"Roll: {roll:.2f}° | Pitch: {pitch:.2f}° | Yaw: {yaw:.2f}°"
            cv2.putText(frame, orientation_text, (10, 60), font, font_scale, font_color, font_thickness)

            # Resize and display frame
            video_width = self.video_label.winfo_width()
            video_height = self.video_label.winfo_height()

            if video_width > 1 and video_height > 1:
                # Use NEAREST neighbor for faster resizing
                frame = cv2.resize(frame, (video_width, video_height), 
                                 interpolation=cv2.INTER_NEAREST)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Use more efficient image conversion
                image = Image.frombytes('RGB', (video_width, video_height), 
                                      frame_rgb.tobytes())
                photo = ImageTk.PhotoImage(image)
                
                self.video_label.config(image=photo)
                self.video_label.image = photo

            # Schedule next update if still playing
            if self.is_playing:
                self.window.after(1, self.update_video_frame)  # Reduced delay to 1ms

        except cv2.error as e:
            print(f"OpenCV error: {e}")
            self.is_playing = False
            self.draw_play_button()
            if self.cap:
                self.cap.release()
                self.cap = None
        except Exception as e:
            print(f"Error in video update: {e}")
            self.is_playing = False
            self.draw_play_button()

    def reset_video_capture(self):
        try:
            if self.cap is not None:
                self.cap.release()
            
            self.cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/main.264")
            
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FPS, 60)
            
            codecs = [
                cv2.VideoWriter_fourcc(*'H264'),
                cv2.VideoWriter_fourcc(*'HEVC'),
                cv2.VideoWriter_fourcc(*'X264'),
                cv2.VideoWriter_fourcc('M','J','P','G')
            ]
            
            for codec in codecs:
                self.cap.set(cv2.CAP_PROP_FOURCC, codec)
                if self.cap.isOpened():
                    break
                    
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
        except Exception as e:
            print(f"Error resetting video capture: {e}")
            self.cap = None

    def update_gui(self):
        data = self.get_server_data()
        battery_percentage, rssi_strength, gps_sats, gps_fix, longitude, latitude, altitude, roll, pitch, yaw, battery_voltages, total_voltage = data

        # Update current position for map
        self.current_latitude = latitude
        self.current_longitude = longitude
        
        # Update map if map page is visible
        if self.map_frame.winfo_ismapped():
            self.update_map_position()
        
        battery_percentage = round(battery_percentage, 2)
        self.update_battery_icon(battery_percentage)
        self.battery_label.config(text=f"{battery_percentage}% | {total_voltage:.2f}V")
        
        self.update_rssi_icon(rssi_strength)
        
        self.gps_sats_label.config(text=f"GPS SATS: {gps_sats}")
        self.gps_fix_label.config(text=f"GPS Fix Type: {gps_fix}")
        
        self.window.after(100, self.update_gui)

    def switch_page(self, page_frame):
        """Switch between different pages/views"""
        # Hide all content frames
        for frame in [self.video_frame, self.graphs_frame, self.map_frame]:
            frame.pack_forget()
            
        # Show the selected frame
        page_frame.pack(side="right", fill="both", expand=True)
        
        # If switching to map page, update position
        if page_frame == self.map_frame and self.current_latitude is not None:
            self.update_map_position()

    def on_closing(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AscendOS()
    app.run()
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
