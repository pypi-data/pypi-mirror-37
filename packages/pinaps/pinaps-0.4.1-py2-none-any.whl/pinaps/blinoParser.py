from enum import IntEnum

class BlinoParser(object):

    ##Current state of parser##
    class State(IntEnum):
        PARSER_STATE_NULL = 0
        PARSER_STATE_SYNC = 1
        PARSER_STATE_SYNC_CHECK = 2
        PARSER_STATE_PAYLOAD_LENGTH = 3
        PARSER_STATE_PAYLOAD = 4
        PARSER_STATE_CHKSUM = 5
        PARSER_STATE_WAIT_HIGH = 6
        PARSER_STATE_WAIT_LOW = 7
        PARSER_SYNC_BYTE = 170
        PARSER_EXCODE_BYTE = 9

    ##Packet codes##
    class Code(IntEnum):
        PARSER_CODE_BATTERY            = 0x00,
        PARSER_CODE_POOR_QUALITY       = 0x02,
        PARSER_CODE_ATTENTION          = 0x04,
        PARSER_CODE_MEDITATION         = 0x05,
        PARSER_CODE_8BITRAW_SIGNAL     = 0x06,
        PARSER_CODE_RAW_MARKER         = 0x07,
        
        PARSER_CODE_RAW_SIGNAL         = 0x80,
        PARSER_CODE_EEG_POWERS         = 0x81,
        PARSER_CODE_ASIC_EEG_POWER_INT = 0x83

    ##Structure of passed packet##
    class PacketStructure():
        updated = False
        code = None #Used to indicate what was the last value to be updated. Use this or clear packet and only fill with latest each time???
        battery = None
        quality = None
        attention = None
        meditation = None
        raw = None
        class EEG():
            delta = None
            theta = None
            lAlpha = None
            hAlpha = None
            lBeta = None
            hBeta = None
            lGamma = None
            mGamma = None

    def __init__(self):
        #State of parser#
        self._state = self.State.PARSER_STATE_SYNC
        #Payload processing#
        self._payloadLength = 0
        self._payloadBytesRecieved = 0
        self._payloadData = []
        self._payloadSum = 0
        self._chksum = 0
        ##TGAT Sensor Information Callbacks##
        self._batteryCallback = None
        self._qualityCallback = None
        self._attentionCallback = None
        self._meditationCallback = None
        self._rawSignalCallback = None
        self._eegSignalCallback = None
        #Returning packet#
        self._parsedPacket = self.PacketStructure()
        self._parsedPacket.EEG = self.PacketStructure.EEG()
        #Additional reporting by parser#
        self._isDebugging = False
        self._isLogging = False
        
    def parseByte(self, byte):
        self._parsedPacket.code = None
        self._parsedPacket.updated = False
        #Waiting for SyncByte#
        if(self._state == self.State.PARSER_STATE_SYNC):
            if(self._isDebugging):
                print("\n\n\n\n\n\n\n\n")
            if(byte == self.State.PARSER_SYNC_BYTE): 
                if(self._isDebugging):
                    print("Making sync check")
                self._state = self.State.PARSER_STATE_SYNC_CHECK
                
        #Waiting for second SyncByte#
        elif(self._state == self.State.PARSER_STATE_SYNC_CHECK):
            if(byte == self.State.PARSER_SYNC_BYTE ):
                if(self._isDebugging):
                    print("Synched")
                self._state = self.State.PARSER_STATE_PAYLOAD_LENGTH
            else:
                self._state = self.State.PARSER_STATE_SYNC
                
        #Waiting for payload length#
        elif(self._state == self.State.PARSER_STATE_PAYLOAD_LENGTH):
            self._payloadLength = byte
            if(self._payloadLength > 170):
                if(self._isDebugging):
                    print("Packet exceeds legal size.")
                self._state = self.State.PARSER_STATE_SYNC
            elif(self._payloadLength == 170):
                if(self._isDebugging):
                    print("Packet exceeds legal size by 1.")
            else:
                if(self._isDebugging):
                    print("Payload of %d" % byte)
                self._payloadBytesReceived = 0
                self._payloadSum = 0
                self._state = self.State.PARSER_STATE_PAYLOAD
                
        #Waiting for payload bytes#
        elif(self._state == self.State.PARSER_STATE_PAYLOAD):
            self._payloadData.append(byte)
            self._payloadBytesReceived += 1
            self._payloadSum += byte
            if(self._payloadBytesReceived >= self._payloadLength):
                self._state = self.State.PARSER_STATE_CHKSUM
                if(self._isDebugging):
                    print("Payload finished, moving onto checksum.")
                
        #Waiting for chcksum byte#
        elif(self._state == self.State.PARSER_STATE_CHKSUM):
            self._chksum = byte
            self._state = self.State.PARSER_STATE_SYNC
            if(self._chksum != (~self._payloadSum)&0xFF):
                if(self._isDebugging):
                    print("Checksum failed.")
            else:
                if(self._isDebugging):
                    print("Checksum successful.")
                return self.parsePayload()

        #Possible future application of TGAT#
        elif(self._state == self.State.PARSER_STATE_WAIT_HIGH):
            print("")

        #Possible future application of TGAT#
        elif(self._state == self.State.PARSER_STATE_WAIT_LOW):
            print("")
            
        else:
            self._state = self.State.PARSER_STATE_SYNC

        return self._parsedPacket

    def parsePayload(self):
        if(self._isDebugging):
            print("Parsing packet payload.")
            print("\n")

        i = 0
        extendedCodeLevel = 0
        code = 0
        numBytes = 0
        while (i < self._payloadLength):
            ##Parse possible extended codes.
            while(self._payloadData[i] == self.State.PARSER_EXCODE_BYTE):
                extendedCodeLevel += 1
                i += 1

            ##Parse code.
            code = self._payloadData[i]
            i += 1

            ##Parse code length
            if(code >= 0x80):
                numBytes = self._payloadData[i]
                i += 1
            else:
                numBytes = 1

            if(self._isDebugging):
                print("Code length: %d" % numBytes)
                
            ##Handle parsing code.    
            ret = self.handleCode(extendedCodeLevel, code, numBytes, i)
            i += numBytes
            
        self._payloadData = []
        return ret

    def handleCode(self, extendedCodeLevel, code, numBytes, position):
        if(extendedCodeLevel == 0):

            #Handle battery value#
            if(code == self.Code.PARSER_CODE_BATTERY):
                self._parsedPacket.code = self.Code.PARSER_CODE_BATTERY
                battery = self._payloadData[position]
                self._parsedPacket.battery = battery
                if(self._batteryCallback != None):
                    self._batteryCallback(battery)
                    
                if(self._isDebugging):
                    print("Battery: %d" % battery)
                    print("\n")
                if(self._isLogging):
                    log = open(self.logPath, "a")
                    log.write("Battery: %d\n" % battery)
                    log.close()

            #Handle poor quality value#
            elif(code == self.Code.PARSER_CODE_POOR_QUALITY):
                self._parsedPacket.code = self.Code.PARSER_CODE_POOR_QUALITY
                quality = self._payloadData[position]
                self._parsedPacket.quality = quality
                if(self._qualityCallback != None):
                    self._qualityCallback(quality)

                if(self._isDebugging):
                    print("Poor Quality: %d" % quality)
                    print("\n")
                if(self._isLogging):
                    log = open(self.logPath, "a")
                    log.write("Poor Quality: %d\n" % quality)
                    log.close()

            #Handle attention value#
            elif(code == self.Code.PARSER_CODE_ATTENTION):
                self._parsedPacket.code = self.Code.PARSER_CODE_ATTENTION
                attention = self._payloadData[position]
                self._parsedPacket.attention = attention
                if(self._attentionCallback != None):
                    self._attentionCallback(attention)

                if(self._isDebugging):
                    print("Attention: %d" % attention)
                    print("\n")
                if(self._isLogging):
                    log = open(self.logPath, "a")
                    log.write("Attention: %d\n" % attention)
                    log.close()

            #Handle meditation value#
            elif(code == self.Code.PARSER_CODE_MEDITATION):
                self._parsedPacket.code = self.Code.PARSER_CODE_MEDITATION
                meditation = self._payloadData[position]
                self._parsedPacket.meditation = meditation
                if(self._meditationCallback != None):
                    self._meditationCallback(meditation)
                    
                if(self._isDebugging):
                    print("Meditation: %d" % meditation)
                    print("\n")
                if(self._isLogging):
                    log = open(self.logPath, "a")
                    log.write("Meditation: %d\n" % meditation)
                    log.close()

            #Handle raw value#
            elif(code == self.Code.PARSER_CODE_RAW_SIGNAL):
                self._parsedPacket.code = self.Code.PARSER_CODE_RAW_SIGNAL
                raw = (self._payloadData[position] << 8) | self._payloadData[position+1];
                position += 1
                self._parsedPacket.raw = raw
                if(self._rawSignalCallback != None):
                    self._rawSignalCallback(raw)
                    
                if(self._isDebugging):
                    print("Raw signal: %d" % raw)
                    print("\n")
                if(self._isLogging):
                    log = open(self.logPath, "a")
                    log.write("Raw signal: %d\n" % raw)
                    log.close()

            #Handle deprecated EEG powers#
            elif(code == self.Code.PARSER_CODE_EEG_POWERS):
                self._parsedPacket.code = self.Code.PARSER_CODE_EEG_POWERS

                if(self._isDebugging):
                    print("Deprecated")

            #Handle ASIC EEG powers#
            elif(code == self.Code.PARSER_CODE_ASIC_EEG_POWER_INT):
                self._parsedPacket.code = self.Code.PARSER_CODE_ASIC_EEG_POWER_INT
                ##pos = position
                delta = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                theta = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                lAlpha = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                hAlpha = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                lBeta = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                hBeta = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                lGamma = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3
                mGamma = self._payloadData[position] << 16 | self._payloadData[position+1] << 8 | self._payloadData[position+2]
                position += 3

                #Update parsed data structure with EEG powers#
                self._parsedPacket.EEG.delta = delta
                self._parsedPacket.EEG.theta = theta
                self._parsedPacket.EEG.lAlpha = lAlpha
                self._parsedPacket.EEG.hAlpha = hAlpha
                self._parsedPacket.EEG.lBeta = lBeta
                self._parsedPacket.EEG.hBeta = hBeta
                self._parsedPacket.EEG.lGamma = lGamma
                self._parsedPacket.EEG.mGamma = mGamma

                if(self._eegSignalCallback != None):
                    self._eegSignalCallback(self._parsedPacket.EEG)

                #Print Debugging information to console#
                if(self._isDebugging):
                    print("Delta: %d" % delta)
                    print("Theta: %d" % theta)
                    print("Low Alpha: %d" % lAlpha)
                    print("High Alpha: %d" % hAlpha)
                    print("Low Beta: %d" % lBeta)
                    print("High Beta: %d" % hBeta)
                    print("Low Gamma: %d" % lGamma)
                    print("Medium Gamma: %d" % mGamma)
                    print("\n")
                
                #If logging, write to file#
                if(self._isLogging):
                    log = open(self.logPath, "a")
                    log.write("Delta: %d\n" % delta)
                    log.write("Theta: %d\n" % theta)
                    log.write("Low Alpha: %d\n" % lAlpha)
                    log.write("High Alpha: %d\n" % hAlpha)
                    log.write("Low Beta: %d\n" % lBeta)
                    log.write("High Beta: %d\n" % hBeta)
                    log.write("Low Gamma: %d\n" % lGamma)
                    log.write("Medium Gamma: %d\n" % mGamma)
                    log.write("\n\n")
                    log.close()

            self._parsedPacket.updated = True
            return self._parsedPacket

    ##Additional reporting functionality by parser##
    def activateDebugging(self):
        self._isDebugging = True

    def deactivateDebugging(self):
        self._isDebugging = False
    
    def activateLogging(self, logPath):
        self._isLogging = True
        self.logPath = logPath

    def deactivateLogging(self):
        self._isLogging = False
        
    ##Getters and setters as attributes##
    @property
    def batteryCallback(self):
        return self._batteryCallback
    @property
    def qualityCallback(self):
        return self._qualityCallback
    @property
    def attentionCallback(self):
        return self._attentionCallback
    @property
    def meditationCallback(self):
        return self._meditationCallback
    @property
    def rawSignalCallback(self):
        return self._rawSignalCallback
    @property
    def eegSignalCallback(self):
        return self._eegSignalCallback
    @property
    def parsedPacket(self):
        return self._parsedPacket

    @batteryCallback.setter
    def batteryCallback(self, function):
        self._batteryCallback = function
    @qualityCallback.setter
    def qualityCallback(self, function):
        self._qualityCallback = function
    @attentionCallback.setter
    def attentionCallback(self, function):
        self._attentionCallback = function
    @attentionCallback.setter
    def attentionCallback(self, function):
        self._attentionCallback = function
    @meditationCallback.setter
    def meditationCallback(self, function):
        self._meditationCallback = function
    @rawSignalCallback.setter
    def rawSignalCallback(self, function):
        self._rawSignalCallback = function
    @eegSignalCallback.setter
    def eegSignalCallback(self, function):
        self._eegSignalCallback = function
