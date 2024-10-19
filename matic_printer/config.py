import os

# Serial Communication
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

# File Paths
DEFAULT_SEARCH_PATH = os.path.expanduser("~/MATIC_Sliced")

# Display Settings
DISPLAY_RESOLUTION = (3840, 2160)

# Printer Settings
DEFAULT_CURING_TIME = 8.0
DEFAULT_DELAY_TIME = 2.0

# Logging
LOG_FILE = "matic_printer.log"
LOG_LEVEL = "INFO"

# HDMI Settings
HDMI_DEVICE = "/dev/fb0"  # Framebuffer device for HDMI output