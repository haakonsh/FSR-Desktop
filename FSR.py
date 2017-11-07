try:
    import platform
    if(platform.architecture()[0] != "32bit" and platform.system() == "Windows"):
        print("Wrong Python architecture, please install 32bit version of Python")
        input("Press any key to exit...")
        exit()
    import pynrfjprog
    import libs.rtt as rtt
    import libs.FSR_structure as fsr
    import sys
    import numpy as np

    # Check for python version error
    if sys.version_info[0] != 2:
        raise ValueError('Version error:\n \
        Python version in use: %d.%d.%d\n \
        PPK needs version >= 2.7.11' % (sys.version_info[0], sys.version_info[1], sys.version_info[2]))
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

NUMBER_OF_SENSORS = 36
NUMBER_OF_SAMPLES = 512
HEADER_LENGTH = 4  # Header length in bytes, given by the C struct 'fsr_field_t, 3 bytes payload and 1 byte padding

if __name__ == '__main__':

    addr = 0x0040000
    length = (NUMBER_OF_SAMPLES * 2 + HEADER_LENGTH) * NUMBER_OF_SENSORS

    print("FSR test initializing...")
    sensor = fsr.Sensor(number_of_sensors = NUMBER_OF_SENSORS,
                        number_of_samples = NUMBER_OF_SAMPLES,
                        header_length = HEADER_LENGTH)

    ''' Connect and read all initialization data '''
    try:
        Rtt = rtt.RTT(sensor.rtt_handler)
    except Exception as e:
        print("Unable to connect to the device, check debugger connection and make sure the device is flashed.")
        print(str(e))
        exit()
    try:
        Rtt.read(address = addr, data_length = length)

    except Exception as e:
        print("Unable to read to the device.")
        print(str(e))
        exit()
