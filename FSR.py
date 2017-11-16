try:
    import platform
    if(platform.architecture()[0] != "32bit" and platform.system() == "Windows"):
        print("Wrong Python architecture, please install 32bit version of Python")
        input("Press any key to exit...")
        exit()

    from libs.Device import Device
    import libs.QtGUI as GUI
    import sys
    from time import sleep

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
ADDRESS = 0x0040000  # Address in device flash where the FSR structure is located.


if __name__ == '__main__':
    
    device = Device(number_of_sensors = NUMBER_OF_SENSORS,
                    number_of_samples = NUMBER_OF_SAMPLES,
                    header_length = HEADER_LENGTH,
                    read_address = ADDRESS)
    
    application = GUI.guiAppInit()
    window = GUI.Window()
    
    GUI.samplesToGui(device = device,
                     qt_app = window,
                     number_of_sensors = NUMBER_OF_SENSORS,
                     number_of_samples = NUMBER_OF_SAMPLES)
    
    sys.exit(application.exec_())
        
    
    

