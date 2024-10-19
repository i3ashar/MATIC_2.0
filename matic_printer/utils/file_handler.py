import zipfile
import io
import asyncio
import os

class FileHandler:
    @staticmethod
    async def read_zip_file(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        image_data_list = []
        
        def extract_images():
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        with zip_ref.open(file_info) as file:
                            image_data_list.append(file.read())

        await asyncio.to_thread(extract_images)
        return image_data_list

    @staticmethod
    async def save_file(file_path, content):
        def write_file():
            with open(file_path, 'wb') as file:
                file.write(content)

        await asyncio.to_thread(write_file)

    @staticmethod
    async def read_file(file_path):
        def read_file_content():
            with open(file_path, 'rb') as file:
                return file.read()

        return await asyncio.to_thread(read_file_content)