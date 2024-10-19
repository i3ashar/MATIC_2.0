import numpy as np
import fcntl
import mmap
import ctypes
import config

class HDMIOutput:
    def __init__(self):
        self.fb = open(config.HDMI_DEVICE, "rb+")
        self.fb_info = self._get_fb_info()
        self.buffer = mmap.mmap(self.fb.fileno(), self.fb_info.smem_len, mmap.MAP_SHARED, mmap.PROT_WRITE)

    def _get_fb_info(self):
        class FBInfo(ctypes.Structure):
            _fields_ = [
                ("xres", ctypes.c_uint32),
                ("yres", ctypes.c_uint32),
                ("xres_virtual", ctypes.c_uint32),
                ("yres_virtual", ctypes.c_uint32),
                ("xoffset", ctypes.c_uint32),
                ("yoffset", ctypes.c_uint32),
                ("bits_per_pixel", ctypes.c_uint32),
                ("grayscale", ctypes.c_uint32),
                ("red", ctypes.c_uint32 * 3),
                ("green", ctypes.c_uint32 * 3),
                ("blue", ctypes.c_uint32 * 3),
                ("transp", ctypes.c_uint32 * 3),
                ("nonstd", ctypes.c_uint32),
                ("activate", ctypes.c_uint32),
                ("height", ctypes.c_uint32),
                ("width", ctypes.c_uint32),
                ("accel_flags", ctypes.c_uint32),
                ("pixclock", ctypes.c_uint32),
                ("left_margin", ctypes.c_uint32),
                ("right_margin", ctypes.c_uint32),
                ("upper_margin", ctypes.c_uint32),
                ("lower_margin", ctypes.c_uint32),
                ("hsync_len", ctypes.c_uint32),
                ("vsync_len", ctypes.c_uint32),
                ("sync", ctypes.c_uint32),
                ("vmode", ctypes.c_uint32),
                ("rotate", ctypes.c_uint32),
                ("colorspace", ctypes.c_uint32),
                ("reserved", ctypes.c_uint32 * 4),
            ]

        fb_info = FBInfo()
        fcntl.ioctl(self.fb, 0x4600, fb_info)
        return fb_info

    def display_image(self, image):
        if image.shape[:2] != (self.fb_info.yres, self.fb_info.xres):
            raise ValueError("Image dimensions do not match the display resolution")

        image_bytes = image.astype(np.uint32).tobytes()
        self.buffer.seek(0)
        self.buffer.write(image_bytes)

    def clear_display(self):
        black_screen = np.zeros((self.fb_info.yres, self.fb_info.xres, 4), dtype=np.uint8)
        self.display_image(black_screen)

    def close(self):
        self.buffer.close()
        self.fb.close()