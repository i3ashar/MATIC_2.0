import asyncio
import tkinter as tk
from ui.main_window import MATICPrinterApp
import logging
import config

def setup_logging():
    logging.basicConfig(
        filename=config.LOG_FILE,
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

async def main():
    setup_logging()
    root = tk.Tk()
    app = MATICPrinterApp(root)
    
    while True:
        root.update()
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())