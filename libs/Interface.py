try:
    import time
    import os
    from pynrfjprog import API, Hex

except ImportError as ie:
    print (str(ie))
    # Catched if any packages are missing
    missing = str(ie).split("named")[1]
    print("Software needs %s installed\nPlease run pip install %s and restart\r\n" % (missing, missing))
    input("Press any key to exit...")
    exit()
except ValueError as e:
    print (str(e))
    input("Press any key to exit...")
    exit()

# Enable this flag to show all errors/warnings
DEBUG = False

JLINK_PRO_V8 = 4000
JLINK_OBD = 1000

# Always try to have highest speed
JLINK_SPEED_KHZ = JLINK_PRO_V8


class Instance(object):
    def __init__(self):
        """
        callback routine used to decode the data read from the device.

        @param callback: The callback used to process the data read from the device

        @return None
        """
        self.alive = True
        # Open connection to debugger
        self.nrfjprog = API.API('NRF52')
        self.nrfjprog.open()
        
        try:
            self.nrfjprog.connect_to_emu_without_snr(jlink_speed_khz = JLINK_SPEED_KHZ)
        except Exception as e:
            print('Could not connect to SEGGER debugger chip! Exception: %s' % str(e))
            raise
        # TODO Do I really need to sleep for a whole second?
        time.sleep(1)
        
        print('Connected to device')
    
    def flash_application(self, hex_file_path):
        """
        callback routine used to decode the data read from the device.

        @param int hex_file_path: Path to the hex file you want to flash

        @return None
        """
        
        try:
            if os.path.exists(hex_file_path):
                pass
            else:
                return "Failed to locate hex file at %s" % hex_file_path
            
            application = Hex.Hex(hex_file_path)  # Parsing hex file into segments
            for segment in application:
                self.nrfjprog.write(segment.address, segment.data, True)
            
            return True
        except Exception as e:
            print(str(e))
            print ("Failed to write device")
            return str(e)
    
    def read(self, address, data_length):
        """
        callback routine used to decode the data read from the device.

        @param int address: Start address of the memory block to read.
        @param int data_length: Number of bytes to read.

        @return None
        """
        try:
            
            try:
                
                byte_array = self.nrfjprog.read(address, data_length)
            
            except AttributeError as attre:
                print('Could not read device memory at address:%d with length %d. \n AttributeError: %s' % (
                    address, data_length, str(attre)))
                # Interface module reported error upon exit
                pass
            
            except Exception as e:
                print('Exception: %s' % e)
                print ("Lost connection, retrying for 10 times")
                print ("Reconnecting...")
                connected = False
                tries = 0
                while tries != 10:
                    try:
                        print tries
                        time.sleep(0.6)
                        self.nrfjprog.close()
                        self.nrfjprog = API.API('NRF52')
                        self.nrfjprog.open()
                        self.nrfjprog.connect_to_emu_without_snr(jlink_speed_khz = JLINK_SPEED_KHZ)
                        self.nrfjprog.sys_reset()
                        self.nrfjprog.go()
                        # TODO Do I really need to start rtt, and sleep for a whole second?
                        self.nrfjprog.rtt_start()
                        time.sleep(1)
                        print ("Reconnected.")
                        connected = True
                        break
                    
                    except Exception as e:
                        print ("Reconnecting...")
                        tries += 1
                        self.alive = connected
                if connected:
                    self.alive = True
                else:
                    raise Exception("Failed to reconnect")
        
        except Exception, e:
            
            self.alive = False
            print('Read failed. Device not alive. Exception: %s' % str(e))
            
        return byte_array


