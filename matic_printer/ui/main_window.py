import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import asyncio
from printer.dlp_controller import DLPController
from printer.print_manager import PrintManager
from utils.file_handler import FileHandler
import config

class MATICPrinterApp:
    def __init__(self, master):
        self.master = master
        master.title("MATIC - 3D Printing Control")
        master.geometry("1024x700")
        
        self.dlp_controller = DLPController()
        self.print_manager = PrintManager(self.dlp_controller)
        self.file_handler = FileHandler()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # File selection
        ttk.Label(main_frame, text="Print File:").grid(row=0, column=0, sticky="w")
        self.file_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.file_path).grid(row=0, column=1, sticky="ew")
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)
        
        # Print controls
        ttk.Button(main_frame, text="Start Print", command=self.start_print).grid(row=1, column=0)
        ttk.Button(main_frame, text="Pause/Resume", command=self.pause_resume_print).grid(row=1, column=1)
        ttk.Button(main_frame, text="Stop Print", command=self.stop_print).grid(row=1, column=2)
        
        # Status display
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=2, column=0, columnspan=3)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100).grid(row=3, column=0, columnspan=3, sticky="ew")
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=config.DEFAULT_SEARCH_PATH,
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
    
    async def start_print(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a file to print.")
            return
        
        try:
            await self.dlp_controller.power_on()
            await self.print_manager.start_print(self.file_path.get())
            self.update_status("Printing started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start print: {str(e)}")
    
    async def pause_resume_print(self):
        try:
            if self.print_manager.is_paused:
                await self.print_manager.resume_print()
                self.update_status("Print resumed")
            else:
                await self.print_manager.pause_print()
                self.update_status("Print paused")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pause/resume print: {str(e)}")
    
    async def stop_print(self):
        try:
            await self.print_manager.stop_print()
            self.update_status("Print stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop print: {str(e)}")
    
    def update_status(self, message):
        self.status_var.set(message)
    
    def update_progress(self, progress):
        self.progress_var.set(progress)

# Note: This class would need to be integrated with an event loop to handle the async methods properly