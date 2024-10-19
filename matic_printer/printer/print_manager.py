import asyncio
from printer.image_processor import ImageProcessor
from utils.file_handler import FileHandler
from utils.hdmi_output import HDMIOutput
import config

class PrintManager:
    def __init__(self, dlp_controller):
        self.dlp_controller = dlp_controller
        self.image_processor = ImageProcessor()
        self.file_handler = FileHandler()
        self.hdmi_output = HDMIOutput()
        self.is_printing = False
        self.is_paused = False
        self.current_layer = 0
        self.total_layers = 0

    async def start_print(self, file_path):
        if self.is_printing:
            raise Exception("A print job is already in progress")
        
        self.is_printing = True
        self.is_paused = False
        self.current_layer = 0
        
        try:
            image_data_list = await self.file_handler.read_zip_file(file_path)
            self.total_layers = len(image_data_list)
            
            processed_images = self.image_processor.process_images(image_data_list)
            
            for image in processed_images:
                if not self.is_printing:
                    break
                
                while self.is_paused:
                    await asyncio.sleep(0.1)
                
                await self.print_layer(image)
                self.current_layer += 1
        
        finally:
            self.is_printing = False
            await self.dlp_controller.uv_off()
            self.image_processor.close()

    async def print_layer(self, image):
        self.hdmi_output.display_image(image)
        await self.dlp_controller.uv_on()
        await asyncio.sleep(config.DEFAULT_CURING_TIME)
        await self.dlp_controller.uv_off()
        await asyncio.sleep(config.DEFAULT_DELAY_TIME)

    async def pause_print(self):
        if not self.is_printing:
            raise Exception("No print job is in progress")
        self.is_paused = True
        await self.dlp_controller.uv_off()

    async def resume_print(self):
        if not self.is_printing or not self.is_paused:
            raise Exception("Print is not paused")
        self.is_paused = False

    async def stop_print(self):
        if not self.is_printing:
            raise Exception("No print job is in progress")
        self.is_printing = False
        await self.dlp_controller.uv_off()

    def get_progress(self):
        if self.total_layers == 0:
            return 0
        return (self.current_layer / self.total_layers) * 100