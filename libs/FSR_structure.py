import numpy as np


class Sensor(object):
    """
    Object containing data from each fsr sensor and supporting functions
    """
    def __init__(self, number_of_sensors, number_of_samples, header_length):
        """
        callback routine used to decode the data read from the device.

        @param int number_of_sensors:   Number of Force Sensitive Resistors on the device
        @param int number_of_samples:   Number of samples per FSR
        @param int header_length:       Size of the header, in bytes
        @return None
        """
        self.number_of_sensors = number_of_sensors
        self.number_of_samples = number_of_samples
        self.header_length = header_length
        self.byte_array_sample_length = 2 * self.number_of_samples

        self.packet_size = self.header_length + self.byte_array_sample_length  # 3 x uint8 + n * int16
        self.read_length = self.packet_size * self.number_of_sensors
        self.sensor_number = 0
        self.samples = []   # A list of numpy arrays, containing the samples of numpy.int16 type
        self.headers = [0 for n in range(0, self.number_of_sensors)]

        self.number = 0
        self.state = 0
        self.adc_channel = 0

    def rtt_handler(self, byte_array):
        # Data arrives here
        """
        callback routine used to decode the data read from the device.

        @param bytearray byte_array: data read from the device
        @return None
        """
        try:
            
            for i in range(0, self.number_of_sensors):
                # Get header
                offset_start = i * self.packet_size
                self.sensor_number = byte_array[offset_start + 0]
                self.state = byte_array[offset_start + 1]
                self.adc_channel = byte_array[offset_start + 2]
                try:
                    self.headers[i] = (self.sensor_number, self.state, self.adc_channel)
                except Exception as error:
                    raise RuntimeError('Could not decode header. Error: %s' % error)

                # Get samples
                offset = i * ((self.header_length / 2) + self.number_of_samples) + self.header_length / 2

                try:
                    self.samples.append(np.arange(start = 0, stop = self.number_of_samples, dtype = np.int16))

                except Exception as error:
                    raise RuntimeError('Could not append numpy array to list. Error: %s' % error)

                try:
                    self.samples[i] = np.frombuffer(byte_array,
                                                         dtype = np.int16,
                                                         count = self.number_of_samples,
                                                         offset = offset)
                except Exception as error:
                    raise RuntimeError('Could not copy data into numpy array. Error: %s' % error)

            # TODO Validate data
            # TODO Plot data
            pass
        
        except Exception as error:
            raise RuntimeError('Could not decode data. Error: %s' % error)








