import RPi.GPIO as GPIO
from enum import IntEnum

import sys
sys.path.insert(0, "../SC16IS750-Python-Driver/SC16IS750-Python-Driver")
import serial
import SC16IS750

class PiNapsController:
    ##Pi to TGAT GPIOs##
    TGAT_POWER_PIN = 23
    TGAT_UART_PIN = 18

    ##I2C controlled LEDs##
    class LEDs(IntEnum):
        RED = 0
        GREEN = 1
        BLUE = 2

    ##Pi to TGAT interface##
    class Interface(IntEnum):
        NONE = 0
        UART = 1
        I2C = 2

    ##Baudrate values##
    class Baudrate(IntEnum):
        BAUD_1_2K = 1200
        BAUD_9_6K = 9600
        BAUD_57_6K = 57600

    ##TGAT operating modes##
    class OutputMode(IntEnum):
        NORMAL_OUTPUT_1_2K = 0
        NORMAL_OUTPUT_9_6K = 1
        RAW_OUTPUT_57_6K = 3
        FFT_OUTPUT_57_6K = 4

    ##Init interfaces and GPIO pins##
    def __init__(self):
        self.interface = 0
        self._UART = None
        self._I2C = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TGAT_UART_PIN, GPIO.OUT)
        GPIO.setup(self.TGAT_POWER_PIN, GPIO.OUT)

    ##Activate a chosen LED##
    def activateLED(self, selectedLED):
        self._I2C.unsetRegisterBit(self._I2C.registers.IOSTATE, selectedLED)

    ##Deactivate a chosen LED##
    def deactivateLED(self, selectedLED):
        self._I2C.setRegisterBit(self._I2C.registers.IOSTATE, selectedLED)

    ##Deactivate all LEDs##
    def deactivateAllLED(self):
        self._I2C.writeRegister(self._I2C.registers.IOSTATE, 0xFF)

    ##Power to TGAT##
    def activateTGAT(self):
        GPIO.output(self.TGAT_POWER_PIN, GPIO.HIGH)

    ##Power down TGAT## 
    def deactivateTGAT(self):
        GPIO.output(self.TGAT_POWER_PIN, GPIO.LOW)

    ##Setup UART interface between Pi and TGAT##
    def setupUART(self):
        #Acivate TGAT UART pin#
        GPIO.output(self.TGAT_UART_PIN, GPIO.HIGH)
        #Initalize Pi UART interface#
        self._interface = 1
        self._UART = serial.Serial('/dev/serial0', 57600)
        self.setMode(self.OutputMode.RAW_OUTPUT_57_6K)

    ##Deactivate UART interface between Pi and TGAT##
    def deactivateUART(self):
        #Deactivate TGAT UART pin#
        GPIO.output(self.TGAT_UART_PIN, GPIO.LOW)
        #Close Pi UART interface if open#
        if(self._UART != None):
            self._UART.close()

    ##Setup I2C interface between Pi and TGAT##
    def setupI2C(self):
        self._interface = 2
        self._I2C = SC16IS750.SC16IS750()
        self._I2C.init(14745600)
        self._I2C.writeRegister(self._I2C.registers.IODIR, 0xFF)
        #Do this here or elsewhere?
        #self._I2C.setBaudrate(9600)

    ##Check if data waiting from TGAT##
    def isWaiting(self):
        if(self._interface == self.Interface.UART):
            if(self._UART.inWaiting()):
                return True
        if(self._interface == self.Interface.I2C):
            if(self._I2C.dataWaiting()):
                return True
        return False

    ##Check how much data is waiting from TGAT##
    def dataWaiting(self):
        if(self._interface == self.Interface.UART):
            return self._UART.inWaiting()
        if(self._interface == self.Interface.I2C):
            return self._I2C.dataWaiting()
        return 0

    ##Read byte of data waiting from TGAT##
    def readTGAT(self):
        if(self._interface == self.Interface.UART):
           return self.decodeByte(self._UART.read())
        if(self._interface == self.Interface.I2C):
           return self._I2C.readRegister(self._I2C.registers.RHR)

    ##Set the TGAT operating mode##
    def setMode(self, output_mode):
        #Set TGAT mode using UART interface#
        if(self._interface == self.Interface.UART):
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_1_2K):
                self._UART.write([0x01])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_1_2K)
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_9_6K):
                self._UART.write([0x00])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_9_6K)
            if(output_mode == self.OutputMode.RAW_OUTPUT_57_6K):
                self._UART.write([0x02])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)
            if(output_mode == self.OutputMode.FFT_OUTPUT_57_6K):
                self._UART.write([0x03])
                self._UART = serial.Serial('/dev/serial0', self.Baudrate.BAUD_57_6K)

        #Set TGAT mode using I2C interface#
        if(self._interface == self.Interface.I2C):
            self._I2C.writeRegister(self._I2C.registers.LCR, 0x03) #UART Attributes - no parity, 8 databits, 1 stop bit
            self._I2C.writeRegister(self._I2C.registers.FCR, 0x07) #Fifo control - Enable + Reset RX + TX
            #sc.writeRegister(sc.registers.THR, 0x02) #
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_1_2K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x01)
                self._I2C.setBaudrate(self.Baudrate.BAUD_1_2K)
            if(output_mode == self.OutputMode.NORMAL_OUTPUT_9_6K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x00)
                self._I2C.setBaudrate(self.Baudrate.BAUD_9_6K)
            if(output_mode == self.OutputMode.RAW_OUTPUT_57_6K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x2)
                self._I2C.setBaudrate(self.Baudrate.BAUD_57_6K)
            if(output_mode == self.OutputMode.FFT_OUTPUT_57_6K):
                self._I2C.writeRegister(self._I2C.registers.THR, 0x3)
                self._I2C.setBaudrate(self.Baudrate.BAUD_57_6K)

    #This might need to be used on data recieved from UART???
    def decodeByte(self, byte):
        #return byte.decode('utf-8')
        return int((str(byte)).encode('hex'), 16)
