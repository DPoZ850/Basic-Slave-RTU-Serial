## This is a simple Modbus Slave implementation to provide a data connection to the XDSensor Server
##
##
import asyncio
import logging

from serial import Serial
from pymodbus import __version__ as pymodbus_version

from pymodbus.datastore import  (
    ModbusSequentialDataBlock, 
    ModbusSlaveContext, 
    ##ModbusSparseDataBlock,
    ModbusServerContext
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncSerialServer
from pymodbus.transaction import ModbusRtuFramer
# from pymodbus.server import (
#     StartSerialServer
#     )

_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)


async def main():
    _logger.info("Starting Server...")
    # Define Holding Registers
    HoldingRegisters = ModbusSequentialDataBlock(0, [0]*100)

    # Define your Modbus Slave Context
    store = ModbusSlaveContext(
        di=None,                                   # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
        hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
        ir=None)                                   # Input Registers

    ## Alternative DataBlock is ModbusSparseDataBlock({0x00: 0, 0x05: 1})  ## This would create 2 memories @ 0x00 and 0x05 base address

    context = ModbusServerContext(slaves=store, single=True)

    # DeviceIdentity = ModbusDeviceIdentification(
    #     info_name={
    #         "VendorName": "XDSensor",
    #         "ProductCode":"SN"
    #         "VendorUrl":"https://XDSensor.com",
    #         "ProductName":"XDSensor Site",
    #         "ModelName":"XDSensor Server",
    #         "MajorMinorRevision": pymodbus_version
    #     }
    #)

    rtu_framer = ModbusRtuFramer

    # Define serial port settings
    serial_port = Serial('/dev/ttyUSB0', baudrate=9600, bytesize=8, parity='N', stopbits=1)

    # Start the Modbus Serial Server
    server = await StartAsyncSerialServer(
        context, 
        port=serial_port,
        ##port='/dev/ttyUSB0',         
        ##stopbits=1,        
        ##parity = 'N',
        ##baudrate=9600,
        bytesize =8,
        handle_lcoal_echo=False,
        ##identity=DeviceIdentity,
        ignore_missing_slaves=True,
        strict=True,
        framer=rtu_framer
        )
    ##server = StartAsyncSerialServer(context, port=serial_port, framer=None)

    HoldingRegisters.setValues(0,0xAA)
    HoldingRegisters.setValues(2,0xAA)

    return 1


asyncio.run(main(), debug = True)

