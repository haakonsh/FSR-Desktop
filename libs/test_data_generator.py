import numpy as np
import array

import struct

class SensorSim:

    def __init__(self, number_of_sensors = 36, number_of_samples = 40, header_length = 4):
        self.number_of_sensors = number_of_sensors
        self.number_of_samples = number_of_samples
        self.header_length = header_length
        self.sample_size = 2 * self.number_of_samples
        self.packet_size = self.header_length + self.sample_size # Header_length x uint8 + number_of_samples * int16
        self.fmt = '>%dB%dH' % (header_length, number_of_samples)
        self.string = ''    # Buffer containing the encoded string

        self.byte_array = bytearray(self.number_of_sensors * self.packet_size)    # Array containing the encoded data
        self.data = ''  # Buffer containing the samples of a given sensor
        self.decoded_string = ()
        self.sensor_number = 0
        self.state = 0
        self.adc_channel = 0
        self.samples = []
        self.headers = [0 for n in range(0, self.number_of_sensors)]

    def generate_string(self):
        self.string = ''
        for sensor in range(0, self.number_of_sensors):
            self.string = self.string + chr(sensor) + '\xff' + chr(sensor)  # Add a header with incremental values

            for sample in range(0, self.number_of_samples):     # Create a string og int16's in hex format
                self.data = self.data + '\x00' + chr(sample)

            self.string = self.string + self.data   # Add the new packet to the string
            self.data = ''  # Empty the 'data' string
        return self.string

    def generate_byte_array(self):
        for sensor in range(0, self.number_of_sensors):
            offset = sensor * self.packet_size
            self.byte_array[offset] = sensor
            self.byte_array[offset + 1] = 255
            self.byte_array[offset + 2] = sensor

            for sample in range(0, self.number_of_samples):
                if sample % 2 == 0:
                    self.byte_array[offset + self.header_length + sample] = sample/2

        return self.byte_array

    def decode_string(self, string):
        self.decoded_string = ()    # Initialize empty buffer
        for sensor in range(0, self.number_of_sensors):
            offset = sensor * self.packet_size
            self.decoded_string = self.decoded_string + struct.unpack_from(self.fmt, string, offset)    # Unpack from 'string' starting at offset and ending after fmt
        return self.decoded_string

    def decode_byte_array(self, byte_array):
        for sensor in range(0, self.number_of_sensors):
            offset_start = sensor * self.packet_size

            self.sensor_number = byte_array[offset_start + 0]
            self.state = byte_array[offset_start + 1]
            self.adc_channel = byte_array[offset_start + 2]
            self.headers[sensor] = (self.sensor_number, self.state, self.adc_channel)

            offset = sensor * ((self.header_length/2) + self.number_of_samples) + self.header_length/2

            self.samples.append(np.arange(start = 0, stop = self.number_of_samples, dtype = np.int16))

            self.samples[sensor] = np.frombuffer(byte_array,
                                                 dtype = np.int16,
                                                 count = self.number_of_samples,
                                                 offset = offset)

        return self.headers, self.samples
