import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import threading
from speed_tester import SpeedTester

class ModernSpeedTesterGUI:
    def __init__(self):
        self.setup_window()
        self.setup_theme()
        self.speed_tester = SpeedTester()
        self.is_testing = False
        self.create_widgets()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Internet Speed Test")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

    def setup_theme(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def create_widgets(self):
        # Main Container
        container = ctk.CTkFrame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            container,
            text="Internet Speed Test",
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=(0, 20))

        # Meters Container
        meters = ctk.CTkFrame(container)
        meters.pack(fill=tk.X, padx=10, pady=10)

        # Download Speed
        download_frame = ctk.CTkFrame(meters)
        download_frame.pack(side=tk.LEFT, expand=True, padx=5)
        
        self.download_label = ctk.CTkLabel(
            download_frame,
            text="0",
            font=("Helvetica", 32, "bold")
        )
        self.download_label.pack()
        
        ctk.CTkLabel(
            download_frame,
            text="Mbps",
            font=("Helvetica", 12)
        ).pack()
        
        ctk.CTkLabel(
            download_frame,
            text="Download",
            font=("Helvetica", 14)
        ).pack()

        # Upload Speed
        upload_frame = ctk.CTkFrame(meters)
        upload_frame.pack(side=tk.LEFT, expand=True, padx=5)
        
        self.upload_label = ctk.CTkLabel(
            upload_frame,
            text="0",
            font=("Helvetica", 32, "bold")
        )
        self.upload_label.pack()
        
        ctk.CTkLabel(
            upload_frame,
            text="Mbps",
            font=("Helvetica", 12)
        ).pack()
        
        ctk.CTkLabel(
            upload_frame,
            text="Upload",
            font=("Helvetica", 14)
        ).pack()

        # Ping
        ping_frame = ctk.CTkFrame(meters)
        ping_frame.pack(side=tk.LEFT, expand=True, padx=5)
        
        self.ping_label = ctk.CTkLabel(
            ping_frame,
            text="0",
            font=("Helvetica", 32, "bold")
        )
        self.ping_label.pack()
        
        ctk.CTkLabel(
            ping_frame,
            text="ms",
            font=("Helvetica", 12)
        ).pack()
        
        ctk.CTkLabel(
            ping_frame,
            text="Ping",
            font=("Helvetica", 14)
        ).pack()

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(container)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=20)
        self.progress_bar.set(0)

        # Start Button
        self.test_button = ctk.CTkButton(
            container,
            text="Start Test",
            font=("Helvetica", 16, "bold"),
            command=self.start_test,
            height=40,
            width=200
        )
        self.test_button.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(
            container,
            text="Ready",
            font=("Helvetica", 12)
        )
        self.status_label.pack()

    def start_test(self):
        if self.is_testing:
            return

        self.is_testing = True
        self.test_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Testing...")
        
        self.speed_tester.run_async(self.update_progress)

    def update_progress(self, test_type, value):
        if test_type == 'ping':
            self.ping_label.configure(text=f"{value:.0f}")
            self.progress_bar.set(0.2)
        elif test_type == 'download_progress':
            self.download_label.configure(text=f"{value:.1f}")
            self.progress_bar.set(0.4)
        elif test_type == 'download':
            self.download_label.configure(text=f"{value:.1f}")
            self.progress_bar.set(0.6)
        elif test_type == 'upload_progress':
            self.upload_label.configure(text=f"{value:.1f}")
            self.progress_bar.set(0.8)
        elif test_type == 'upload':
            self.upload_label.configure(text=f"{value:.1f}")
            self.progress_bar.set(1.0)
            self.test_complete()

    def test_complete(self):
        self.is_testing = False
        self.test_button.configure(state="normal")
        self.status_label.configure(text="Test completed")

    def run(self):
        self.root.mainloop()

def main():
    app = ModernSpeedTesterGUI()
    app.run()

if __name__ == "__main__":
    main()
