import serial
import asyncio
import logging

class SerialCommunication:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_port = None

    async def connect(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baud_rate, timeout=1)
            logging.info(f"Successfully connected to {self.port}")
        except serial.SerialException as e:
            logging.error(f"Failed to connect to {self.port}: {e}")
            raise

    async def send_command(self, command, expected_response=None, command_name=""):
        if not self.serial_port or not self.serial_port.is_open:
            await self.connect()

        try:
            self.serial_port.reset_input_buffer()
            self.serial_port.write(command)
            logging.debug(f"Sent command: {command_name} - {command.hex()}")

            response = await asyncio.wait_for(self._read_response(), timeout=1.0)

            logging.debug(f"Received response for {command_name}: {response.hex()}")

            if expected_response and response != expected_response:
                logging.warning(f"Unexpected response for {command_name}. Expected: {expected_response.hex()}, Got: {response.hex()}")
            return response
        except asyncio.TimeoutError:
            logging.error(f"Timeout waiting for response to {command_name}")
        except serial.SerialException as e:
            logging.error(f"Error sending {command_name} command: {e}")
        return None

    async def _read_response(self):
        response = b''
        while len(response) < 4:
            if self.serial_port.in_waiting:
                response += self.serial_port.read(self.serial_port.in_waiting)
            await asyncio.sleep(0.01)
        return response

    def close(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            logging.info(f"Closed connection to {self.port}")