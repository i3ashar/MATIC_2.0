import asyncio
from utils.serial_communication import SerialCommunication
import config
import logging

class DLPController:
    def __init__(self):
        self.serial_comm = SerialCommunication(config.SERIAL_PORT, config.BAUD_RATE)
        self.is_powered_on = False

    async def power_on(self):
        response = await self.serial_comm.send_command(b'\x2A\xFA\x0D', b'\x2A\xFA\x00\x0D', "Power On")
        if response == b'\x2A\xFA\x00\x0D':
            self.is_powered_on = True
            logging.info("DLP engine powered on successfully")
        else:
            raise Exception("Failed to power on DLP engine")

    async def power_off(self):
        response = await self.serial_comm.send_command(b'\x2A\xFB\x0D', b'\x2A\xFB\x00\x0D', "Power Off")
        if response == b'\x2A\xFB\x00\x0D':
            self.is_powered_on = False
            logging.info("DLP engine powered off successfully")
        else:
            raise Exception("Failed to power off DLP engine")

    async def uv_on(self):
        response = await self.serial_comm.send_command(b'\x2A\x4B\x0D', b'\x2A\x4B\x00\x0D', "UV LED On")
        if response != b'\x2A\x4B\x00\x0D':
            raise Exception("Failed to turn on UV LED")

    async def uv_off(self):
        response = await self.serial_comm.send_command(b'\x2A\x47\x0D', b'\x2A\x47\x00\x0D', "UV LED Off")
        if response != b'\x2A\x47\x00\x0D':
            raise Exception("Failed to turn off UV LED")

    async def get_temperature(self):
        response = await self.serial_comm.send_command(b'\x2A\x4E\x0D', None, "Get Temperature")
        if response and len(response) == 4 and response[0:2] == b'\x2A\x4E':
            return response[2]
        else:
            raise Exception("Failed to get temperature")

    async def set_fan_speed(self, fan_type, speed):
        if fan_type not in ["module", "uv_led"] or not 30 <= speed <= 100:
            raise ValueError("Invalid fan type or speed")
        
        command = b'\x2A\xEF' if fan_type == "module" else b'\x2A\xEE'
        command += bytes([speed, 0x0D])
        
        response = await self.serial_comm.send_command(command, None, f"Set {fan_type} fan speed")
        if response != command[0:2] + b'\x00\x0D':
            raise Exception(f"Failed to set {fan_type} fan speed")

    # Add other methods for UV current setting, display direction, etc.