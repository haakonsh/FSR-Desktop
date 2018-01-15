try:
    import Interface
    from libs import DataProcessing as process
    import math
    
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


class Device(object):
    """
    Object containing the computer-device interface and the device's Sensor object.
    """
    
    def __init__(self, number_of_sensors, number_of_samples, header_length, read_address):
        """
        @param int number_of_sensors:   Number of Force Sensitive Resistor sensors on the device
        @param int number_of_samples:   Number of samples per sensor
        @param int header_length:       Size of a sensor's header data, in bytes
        @param int read_address:        Address in device memory where the data will be read from
        """
        self.number_of_sensors = number_of_sensors
        self.number_of_samples = number_of_samples
        self.header_length = header_length
        self.read_address = read_address
        """
        The packet structure is: | 4 bytes of headers | 2 bytes * number_of_samples |, for each sensor
        """
        self.read_length = (self.header_length + self.number_of_samples * 2) * self.number_of_samples
        
        self.samples = []  # A list of numpy arrays, containing the samples of numpy.int16 type
        self.headers = [0 for n in range(0, self.number_of_sensors)]
        
        self.interface = self.interfaceInit()

        self.data_buffer = self.readDeviceData()
        self.processData(self.data_buffer)
        # self.nonlinearToLinear()

    def interfaceInit(self):
        """
        Initializes an interface built from the pynrfjprog library.

        @return interface: An Interface instance that can be used to read from the device's memory at location ADDRESS
        and of length READ_LENGTH, as well as flashing the device with a new HEX file.
        """
        try:
            interface = Interface.Instance()
        except Exception as e:
            print("Unable to connect to the device, check debugger connection and make sure the device is flashed.")
            print(str(e))
            exit()
        return interface

    def readDeviceData(self):
        """
        Reads the devices memory at read_address and of read_length.
        Data is processed by calling 'processData'
        """
        return self.interface.read(address = self.read_address, data_length = self.read_length)

    def processData(self, data):
        """
        Extracts headers and samples from the data read from the device, and Maps the headers and samples to their
        respective sensor number as given by the 'sensor number' field ('0') in the header.
        """
        headers = process.extractHeaders(byte_array = data,
                                         number_of_sensors = self.number_of_sensors,
                                         number_of_samples = self.number_of_samples,
                                         header_length = self.header_length)
        
        samples = process.extractSamples(byte_array = data,
                                         number_of_sensors = self.number_of_sensors,
                                         number_of_samples = self.number_of_samples,
                                         header_length = self.header_length)
        
        samples = process.UnityBasedNormalization(samples = samples,
                                                  number_of_sensors = self.number_of_sensors)

        samples = process.nonLinearityCompensation(samples = samples,
                                                   number_of_sensors = self.number_of_sensors)
        
        samples = process.convertToUint16t(samples = samples,
                                           number_of_sensors = self.number_of_sensors)

        samples = process.averagingFilter(samples = samples,
                                          number_of_sensors = self.number_of_sensors,
                                          width_of_filter = 4)
        
        

        self.headers, self.samples = process.mapDataToSensors(headers = headers,
                                                              samples = samples,
                                                              number_of_sensors = self.number_of_sensors)
