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
    CONTENT_BG = "#ffffff"       
    
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
        self.coords_label = None  # Initialize the label variable
        
        # Create frames
        self.create_frames()
        
        # Initialize connection presets
        self.connection_presets = {}
        
        # Setup all UI components
        self.setup_sidebar()
        self.setup_video_page()
        self.setup_graphs_page()
        self.setup_map_page()
        self.setup_connections_page()
        
        # Initialize graphs data
        self.graph1_data = {'x': [], 'y': []}
        self.graph2_data = {'x': [], 'y': []}
        
        # Start GUI updates
        self.update_gui()
        
        # Set up window close protocol
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_frames(self):
        # Left sidebar
        self.left_frame = tk.Frame(self.window, width=200, bg=self.SIDEBAR_BG)
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)
        
        # Main content frames
        self.video_frame = tk.Frame(self.window, bg=self.VIDEO_BG)
        self.graphs_frame = tk.Frame(self.window, bg=self.CONTENT_BG)
        self.map_frame = tk.Frame(self.window, bg=self.CONTENT_BG)
        self.connections_frame = tk.Frame(self.window, bg=self.CONTENT_BG)
        
        # Start with video frame visible
        self.video_frame.pack(side="right", fill="both", expand=True)

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
        
        self.connections_page_btn = ttk.Button(nav_buttons_frame, text="Connections",
                                          command=lambda: self.switch_page(self.connections_frame),
                                          style='Custom.TButton')
        self.connections_page_btn.pack(fill="x", pady=2)

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
        rtsp_label = tk.Label(conn_frame, text="RTSP:", bg=self.SIDEBAR_BG, fg="#0f1a2b", font=('Arial', 10))
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
        coords_frame = tk.Frame(self.map_frame, bg= self.SIDEBAR_BG,)
        coords_frame.pack(fill="x", pady=5)

        # Create label for coordinates
        self.coords_label = tk.Label(coords_frame,
                                   text="Current Position: 0.000000°, 0.000000°",
                                   font=('Arial', 12),
                                   bg= self.SIDEBAR_BG)
        self.coords_label.pack(pady=5)

        # Add clear trail button
        self.clear_trail_btn = tk.Button(coords_frame,
                                       text="Clear Trail",
                                       command=self.clear_trail,
                                       bg= self.SIDEBAR_BG,
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

    def setup_connections_page(self):
        """Setup the connections management page"""
        # Title Section
        title_frame = tk.Frame(self.connections_frame, bg=self.CONTENT_BG)
        title_frame.pack(fill="x", padx=20, pady=(20,10))
        
        title = tk.Label(title_frame, text="Connection Presets", 
                        font=("Arial", 24, "bold"), 
                        bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        title.pack()

        subtitle = tk.Label(title_frame, text="Manage your connection presets", 
                          font=("Arial", 12), 
                          bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        subtitle.pack()

        # Add New Preset Section
        add_frame = tk.Frame(self.connections_frame, bg=self.CONTENT_BG)
        add_frame.pack(fill="x", padx=20, pady=20)

        # Add a container for the form with a border
        form_container = tk.Frame(add_frame, bg=self.CONTENT_BG, 
                                relief="solid", borderwidth=1)
        form_container.pack(fill="x", padx=20)

        form_title = tk.Label(form_container, text="Add New Preset",
                            font=("Arial", 14, "bold"),
                            bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        form_title.pack(pady=(10,5))

        # Entry fields with better styling
        entry_frame = tk.Frame(form_container, bg=self.CONTENT_BG)
        entry_frame.pack(padx=20, pady=10)

        # Preset Name
        tk.Label(entry_frame, text="Preset Name:", 
                bg=self.CONTENT_BG, fg=self.TEXT_DARK,
                font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.preset_name_entry = tk.Entry(entry_frame, width=30,
                                        font=("Arial", 10))
        self.preset_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # IP Address
        tk.Label(entry_frame, text="IP Address:", 
                bg=self.CONTENT_BG, fg=self.TEXT_DARK,
                font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.preset_ip_entry = tk.Entry(entry_frame, width=30,
                                      font=("Arial", 10))
        self.preset_ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # RTSP Port
        tk.Label(entry_frame, text="RTSP Port:", 
                bg=self.CONTENT_BG, fg=self.TEXT_DARK,
                font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.preset_rtsp_entry = tk.Entry(entry_frame, width=30,
                                        font=("Arial", 10))
        self.preset_rtsp_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Add Button with hover effect
        add_btn_style = {
            'bg': self.TEXT_DARK,
            'fg': self.CONTENT_BG,
            'font': ('Arial', 10, 'bold'),
            'relief': 'flat',
            'padx': 20,
            'pady': 5,
            'cursor': 'hand2'
        }
        
        add_btn = tk.Button(form_container, text="Add Preset",
                           command=self.add_connection_preset,
                           **add_btn_style)
        add_btn.pack(pady=(0,15))

        def on_enter(e):
            e.widget['bg'] = self.BUTTON_HOVER
        def on_leave(e):
            e.widget['bg'] = self.TEXT_DARK

        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)

        # Presets List Section
        list_frame = tk.Frame(self.connections_frame, bg=self.CONTENT_BG)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        list_title = tk.Label(list_frame, text="Saved Presets",
                            font=("Arial", 14, "bold"),
                            bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        list_title.pack(pady=(0,10))

        # Create scrollable frame for presets
        self.presets_canvas = tk.Canvas(list_frame, bg=self.CONTENT_BG)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                command=self.presets_canvas.yview)
        self.scrollable_frame = tk.Frame(self.presets_canvas, bg=self.CONTENT_BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.presets_canvas.configure(
                scrollregion=self.presets_canvas.bbox("all")
            )
        )

        self.presets_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.presets_canvas.configure(yscrollcommand=scrollbar.set)

        self.presets_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initialize the presets frame
        self.presets_frame = tk.Frame(self.scrollable_frame, bg=self.CONTENT_BG)
        self.presets_frame.pack(fill="both", expand=True, padx=10)

        # Load and display existing presets
        self.load_connection_presets()
        self.refresh_presets_display()

        # Create label for coordinates
        self.coords_label = tk.Label(coords_frame,
                                   text="Current Position: 0.000000°, 0.000000°",
                                   font=('Arial', 12),
                                   bg=self.CONTENT_BG)
        self.coords_label.pack(pady=5)

        # Add clear trail button
        self.clear_trail_btn = tk.Button(coords_frame,
                                       text="Clear Trail",
                                       command=self.clear_trail,
                                       bg=self.TEXT_DARK,
                                       fg=self.CONTENT_BG,
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

    def add_connection_preset(self):
        """Add a new connection preset"""
        name = self.preset_name_entry.get().strip()
        ip = self.preset_ip_entry.get().strip()
        rtsp = self.preset_rtsp_entry.get().strip()
        
        if not all([name, ip, rtsp]):
            tk.messagebox.showerror("Error", "All fields are required")
            return
            
        if name in self.connection_presets:
            tk.messagebox.showerror("Error", "A preset with this name already exists")
            return
            
        self.connection_presets[name] = {"ip": ip, "rtsp": rtsp}
        self.save_connection_presets()
        self.refresh_presets_display()
        
        # Clear entry fields
        self.preset_name_entry.delete(0, tk.END)
        self.preset_ip_entry.delete(0, tk.END)
        self.preset_rtsp_entry.delete(0, tk.END)

    def load_connection_presets(self):
        """Load saved connection presets from file"""
        try:
            if os.path.exists("connection_presets.txt"):
                with open("connection_presets.txt", "r") as f:
                    for line in f:
                        try:
                            name, ip, rtsp = line.strip().split("|")
                            self.connection_presets[name] = {"ip": ip, "rtsp": rtsp}
                        except ValueError:
                            continue
        except Exception as e:
            print(f"Error loading presets: {e}")

    def save_connection_presets(self):
        """Save connection presets to file"""
        try:
            with open("connection_presets.txt", "w") as f:
                for name, data in self.connection_presets.items():
                    f.write(f"{name}|{data['ip']}|{data['rtsp']}\n")
        except Exception as e:
            print(f"Error saving presets: {e}")

    def refresh_presets_display(self):
        """Refresh the display of saved presets"""
        # Clear existing presets display
        for widget in self.presets_frame.winfo_children():
            widget.destroy()
            
        # If no presets, show message
        if not self.connection_presets:
            no_presets_label = tk.Label(self.presets_frame, 
                text="No saved presets. Add one above!", 
                font=("Arial", 12), 
                bg=self.CONTENT_BG, fg=self.TEXT_DARK)
            no_presets_label.pack(pady=20)
            return

        # Create headers
        headers_frame = tk.Frame(self.presets_frame, bg=self.CONTENT_BG)
        headers_frame.pack(fill="x", pady=(0,10))
        
        headers = ["Preset Name", "IP Address", "RTSP Port", "Actions"]
        for i, header in enumerate(headers):
            tk.Label(headers_frame, text=header, 
                    font=("Arial", 10, "bold"),
                    bg=self.CONTENT_BG, fg=self.TEXT_DARK).grid(
                row=0, column=i, padx=10, sticky="w")
        
        headers_frame.grid_columnconfigure(0, weight=1)
        headers_frame.grid_columnconfigure(1, weight=1)
        headers_frame.grid_columnconfigure(2, weight=1)
        headers_frame.grid_columnconfigure(3, weight=1)

        # Add separator
        ttk.Separator(self.presets_frame, orient='horizontal').pack(fill='x', pady=5)
            
        # Display presets
        for name, data in self.connection_presets.items():
            preset_frame = tk.Frame(self.presets_frame, bg=self.CONTENT_BG)
            preset_frame.pack(fill="x", pady=5)
            
            tk.Label(preset_frame, text=name, bg=self.CONTENT_BG, 
                    fg=self.TEXT_DARK).grid(row=0, column=0, padx=10, sticky="w")
            tk.Label(preset_frame, text=data["ip"], bg=self.CONTENT_BG, 
                    fg=self.TEXT_DARK).grid(row=0, column=1, padx=10, sticky="w")
            tk.Label(preset_frame, text=data["rtsp"], bg=self.CONTENT_BG, 
                    fg=self.TEXT_DARK).grid(row=0, column=2, padx=10, sticky="w")
            
            # Actions frame
            actions_frame = tk.Frame(preset_frame, bg=self.CONTENT_BG)
            actions_frame.grid(row=0, column=3, padx=10, sticky="e")
            
            # Button styles
            button_style = {
                'font': ('Arial', 9),
                'relief': 'flat',
                'cursor': 'hand2',
                'padx': 10
            }
            
            use_btn = tk.Button(actions_frame, text="Use", 
                              bg=self.BUTTON_BG, fg=self.CONTENT_BG,
                              command=lambda n=name: self.use_connection_preset(n),
                              **button_style)
            use_btn.pack(side="left", padx=2)
            
            delete_btn = tk.Button(actions_frame, text="Delete",
                                 bg="#dc3545", fg=self.CONTENT_BG,
                                 command=lambda n=name: self.delete_connection_preset(n),
                                 **button_style)
            delete_btn.pack(side="left", padx=2)
            
            # Add hover effects
            def on_enter(e):
                if "Delete" in str(e.widget['text']):
                    e.widget['bg'] = '#bb2d3b'
                else:
                    e.widget['bg'] = self.BUTTON_HOVER
            
            def on_leave(e):
                if "Delete" in str(e.widget['text']):
                    e.widget['bg'] = '#dc3545'
                else:
                    e.widget['bg'] = self.BUTTON_BG
            
            for btn in [use_btn, delete_btn]:
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
            
            preset_frame.grid_columnconfigure(0, weight=1)
            preset_frame.grid_columnconfigure(1, weight=1)
            preset_frame.grid_columnconfigure(2, weight=1)
            preset_frame.grid_columnconfigure(3, weight=1)

    def use_connection_preset(self, name):
        """Apply the selected connection preset"""
        if name in self.connection_presets:
            preset = self.connection_presets[name]
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, preset["ip"])
            self.rtsp_entry.delete(0, tk.END)
            self.rtsp_entry.insert(0, preset["rtsp"])
            
            # Switch to video page and show confirmation
            self.switch_page(self.video_frame)
            tk.messagebox.showinfo("Success", f"Connection preset '{name}' loaded successfully!")

    def delete_connection_preset(self, name):
        """Delete a connection preset"""
        if name in self.connection_presets:
            if tk.messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete the preset '{name}'?"):
                del self.connection_presets[name]
                self.save_connection_presets()
                self.refresh_presets_display()

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
        graph1_frame = tk.Frame(graphs_container, bg=self.CONTENT_BG, relief="solid", borderwidth=1)
        graph1_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        graph2_frame = tk.Frame(graphs_container, bg=self.CONTENT_BG, relief="solid", borderwidth=1)
        graph2_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Setup both graphs
        self.setup_graph(graph1_frame, 1)
        self.setup_graph(graph2_frame, 2)

    def setup_graph(self, parent_frame, graph_num):
        # Title and controls frame
        controls_frame = tk.Frame(parent_frame, bg=self.CONTENT_BG)
        controls_frame.pack(fill="x", pady=5)

        title = tk.Label(controls_frame, text=f"Graph {graph_num}", 
                        font=("Arial", 12, "bold"), bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        title.pack(side="left", padx=15)

        # Buttons frame
        buttons_frame = tk.Frame(controls_frame, bg=self.CONTENT_BG)
        buttons_frame.pack(side="right", padx=15)

        graph_button_style = {
            'background': self.TEXT_DARK,
            'foreground': self.CONTENT_BG,
            'activebackground': '#1a2738',
            'activeforeground': self.CONTENT_BG,
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
        plot_frame = tk.Frame(parent_frame, bg=self.CONTENT_BG)
        plot_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create matplotlib figure
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        
        # Style the plot
        fig.patch.set_facecolor(self.CONTENT_BG)
        ax.set_facecolor(self.CONTENT_BG)
        
        # Initialize empty plot
        ax.plot([], [], '-', color=self.BUTTON_BG, linewidth=2)
        
        # Configure grid and spines
        ax.grid(True, linestyle='--', alpha=0.3, color=self.BUTTON_BG)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(self.BUTTON_BG)
            
        # Set labels
        ax.set_xlabel('X Axis', color=self.TEXT_DARK)
        ax.set_ylabel('Y Axis', color=self.TEXT_DARK)
        ax.set_title(f'Graph {graph_num}', color=self.TEXT_DARK, pad=10)
        
        # Style ticks
        ax.tick_params(colors=self.TEXT_DARK, which='both')

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

    def setup_video_capture(self):
        try:
            self.cap = cv2.VideoCapture("rtsp://192.168.144.25:8554/main.264")
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
            self.cap.set(cv2.CAP_PROP_FPS, 30)
        except Exception as e:
            print(f"Error initializing video capture: {e}")
            self.cap = None

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

    def update_battery_icon(self, percentage):
        self.battery_icon.delete("all")
        
        # Draw battery outline and cap
        self.battery_icon.create_rectangle(58, 8, 62, 18, fill="#dfe8f7", outline=self.TEXT_DARK)
        
        # Calculate fill width based on percentage
        fill_width = int(56 * (percentage / 100))
        
        # Draw filled portion
        self.battery_icon.create_rectangle(2, 2, 2 + fill_width, 24, 
                                         fill=self.BUTTON_BG, outline=self.TEXT_DARK)
        
        # Draw unfilled portion
        self.battery_icon.create_rectangle(2 + fill_width, 2, 58, 24, 
                                         fill="#dfe8f7", outline=self.TEXT_DARK)
        
        # Fill the cap if battery is full
        if fill_width == 56:
            self.battery_icon.create_rectangle(58, 8, 62, 18, fill=self.BUTTON_BG)

    def update_rssi_icon(self, strength):
        self.rssi_canvas.delete("all")
        for i in range(5):
            fill = self.TEXT_DARK if i < strength else "#959799"
            outline = self.TEXT_DARK if i < strength else "#959799"
            self.rssi_canvas.create_rectangle(5 + i * 15, 35 - i * 6, 15 + i * 15, 55, 
                                           fill=fill, outline=outline)

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

    def connect_to_drone(self):
        try:
            ip = self.ip_entry.get()
            rtsp = self.rtsp_entry.get()
            
            self.connect_button.config(text="Connecting...", state="disabled")
            
            if self.cap is not None:
                self.cap.release()
            
            # Use the full RTSP URL from the entry
            rtsp_url = rtsp if '://' in rtsp else f"rtsp://{ip}:{rtsp}/main.264"
            self.cap = cv2.VideoCapture(rtsp_url)
            
            if self.cap.isOpened():
                self.connect_button.config(text="Connected", bg="#4CAF50", fg="white")
            else:
                self.connect_button.config(text="Connect", state="normal", bg="#f0f0f0", fg="black")
                raise Exception("Failed to connect to video stream")
                
        except Exception as e:
            print(f"Connection error: {e}")
            self.connect_button.config(text="Connect", state="normal", bg="#f0f0f0", fg="black")

    def update_gui(self):
        # Get data from server
        data = self.get_server_data()
        battery_percentage, rssi_strength, gps_sats, gps_fix, longitude, latitude, altitude, roll, pitch, yaw, battery_voltages, total_voltage = data

        # Update current position for map
        self.current_latitude = latitude
        self.current_longitude = longitude
        
        # Update map if map page is visible and we have valid coordinates
        if self.map_frame.winfo_ismapped() and latitude != 0 and longitude != 0:
            try:
                if self.coords_label:
                    self.coords_label.config(text=f"Current Position: {latitude:.6f}°, {longitude:.6f}°")
                
                # Update or create drone marker
                if self.drone_marker:
                    self.drone_marker.set_position(latitude, longitude)
                else:
                    self.drone_marker = self.map_widget.set_marker(latitude, longitude, text="Drone")

                # Add position to history and update trail
                current_pos = (latitude, longitude)
                if not self.position_history or current_pos != self.position_history[-1]:
                    self.position_history.append(current_pos)
                    if len(self.position_history) > 1000:
                        self.position_history.pop(0)

                # Update trail path
                if len(self.position_history) > 1:
                    if self.trail_path:
                        self.trail_path.delete()
                    self.trail_path = self.map_widget.set_path(self.position_history, color="red", width=2)

                # Center map on drone position
                self.map_widget.set_position(latitude, longitude)
            except Exception as e:
                print(f"Error updating map: {e}")
        
        # Update other GUI elements
        battery_percentage = round(battery_percentage, 2)
        self.update_battery_icon(battery_percentage)
        self.battery_label.config(text=f"{battery_percentage}% | {total_voltage:.2f}V")
        
        self.update_rssi_icon(rssi_strength)
        
        self.gps_sats_label.config(text=f"GPS SATS: {gps_sats}")
        self.gps_fix_label.config(text=f"GPS Fix Type: {gps_fix}")
        
        # Schedule next update
        self.window.after(100, self.update_gui)

    def switch_page(self, page_frame):
        """Switch between different pages/views"""
        # Hide all content frames
        for frame in [self.video_frame, self.graphs_frame, self.map_frame, self.connections_frame]:
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

    def setup_connections_page(self):
        # Main container
        main_container = tk.Frame(self.connections_frame, bg=self.CONTENT_BG)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_container, text="Connection Presets", 
                        font=("Arial", 16, "bold"), bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        title.pack(pady=(0, 20))
        
        # Add new preset section
        add_frame = tk.Frame(main_container, bg=self.CONTENT_BG)
        add_frame.pack(fill="x", pady=10)
        
        # Entry fields container
        entries_frame = tk.Frame(add_frame, bg=self.CONTENT_BG)
        entries_frame.pack(fill="x", pady=10)
        
        # Preset name entry
        name_label = tk.Label(entries_frame, text="Preset Name:", bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.preset_name_entry = tk.Entry(entries_frame)
        self.preset_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # IP address entry
        ip_label = tk.Label(entries_frame, text="IP Address:", bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        ip_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.preset_ip_entry = tk.Entry(entries_frame)
        self.preset_ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # RTSP port entry
        rtsp_label = tk.Label(entries_frame, text="RTSP Port:", bg=self.CONTENT_BG, fg=self.TEXT_DARK)
        rtsp_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.preset_rtsp_entry = tk.Entry(entries_frame)
        self.preset_rtsp_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        entries_frame.grid_columnconfigure(1, weight=1)
        
        # Add button
        add_btn = tk.Button(add_frame, text="Add Preset", 
                           command=self.add_connection_preset,
                           bg=self.TEXT_DARK, fg=self.CONTENT_BG,
                           font=('Arial', 10, 'bold'))
        add_btn.pack(pady=10)
        
        # Presets list section
        self.presets_frame = tk.Frame(main_container, bg=self.CONTENT_BG)
        self.presets_frame.pack(fill="both", expand=True, pady=20)
        
        # Load saved presets
        self.load_connection_presets()
        
        # Display existing presets
        self.refresh_presets_display()

    def add_connection_preset(self):
        name = self.preset_name_entry.get().strip()
        ip = self.preset_ip_entry.get().strip()
        rtsp = self.preset_rtsp_entry.get().strip()
        
        if not all([name, ip, rtsp]):
            tk.messagebox.showerror("Error", "All fields are required")
            return
            
        self.connection_presets[name] = {"ip": ip, "rtsp": rtsp}
        self.save_connection_presets()
        self.refresh_presets_display()
        
        # Clear entry fields
        self.preset_name_entry.delete(0, tk.END)
        self.preset_ip_entry.delete(0, tk.END)
        self.preset_rtsp_entry.delete(0, tk.END)

    def load_connection_presets(self):
        try:
            if os.path.exists("connection_presets.txt"):
                with open("connection_presets.txt", "r") as f:
                    for line in f:
                        try:
                            name, ip, rtsp = line.strip().split("|")
                            self.connection_presets[name] = {"ip": ip, "rtsp": rtsp}
                        except ValueError:
                            continue
        except Exception as e:
            print(f"Error loading presets: {e}")

    def save_connection_presets(self):
        try:
            with open("connection_presets.txt", "w") as f:
                for name, data in self.connection_presets.items():
                    f.write(f"{name}|{data['ip']}|{data['rtsp']}\n")
        except Exception as e:
            print(f"Error saving presets: {e}")

    def refresh_presets_display(self):
        # Clear existing presets display
        for widget in self.presets_frame.winfo_children():
            widget.destroy()
            
        # Create header
        if self.connection_presets:
            headers = ["Preset Name", "IP Address", "RTSP Port", "Actions"]
            for i, header in enumerate(headers):
                label = tk.Label(self.presets_frame, text=header, 
                               font=("Arial", 10, "bold"),
                               bg=self.CONTENT_BG, fg=self.TEXT_DARK)
                label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            
            # Display presets
            for i, (name, data) in enumerate(self.connection_presets.items(), start=1):
                tk.Label(self.presets_frame, text=name, bg=self.CONTENT_BG, fg=self.TEXT_DARK).grid(
                    row=i, column=0, padx=5, pady=2, sticky="w")
                tk.Label(self.presets_frame, text=data["ip"], bg=self.CONTENT_BG, fg=self.TEXT_DARK).grid(
                    row=i, column=1, padx=5, pady=2, sticky="w")
                tk.Label(self.presets_frame, text=data["rtsp"], bg=self.CONTENT_BG, fg=self.TEXT_DARK).grid(
                    row=i, column=2, padx=5, pady=2, sticky="w")
                
                actions_frame = tk.Frame(self.presets_frame, bg=self.CONTENT_BG)
                actions_frame.grid(row=i, column=3, padx=5, pady=2)
                
                # Use button
                tk.Button(actions_frame, text="Use", 
                         command=lambda n=name: self.use_connection_preset(n),
                         bg=self.TEXT_DARK, fg=self.CONTENT_BG).pack(side="left", padx=2)
                
                # Delete button
                tk.Button(actions_frame, text="Delete", 
                         command=lambda n=name: self.delete_connection_preset(n),
                         bg="#dc3545", fg=self.CONTENT_BG).pack(side="left", padx=2)

    def use_connection_preset(self, name):
        if name in self.connection_presets:
            preset = self.connection_presets[name]
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, preset["ip"])
            self.rtsp_entry.delete(0, tk.END)
            self.rtsp_entry.insert(0, preset["rtsp"])
            self.switch_page(self.video_frame)

    def delete_connection_preset(self, name):
        if name in self.connection_presets:
            if tk.messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete the preset '{name}'?"):
                del self.connection_presets[name]
                self.save_connection_presets()
                self.refresh_presets_display()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AscendOS()
    app.run()