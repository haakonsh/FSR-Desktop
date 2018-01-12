try:
    import numpy as np
    import panda as pd

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
    
SCALAR = -5.35 * 10 ** (-2.5)  # Magic number
MAXVALUE = 300  # 300 represents the valid range in HSV color that we will use (60-360)


def extractHeaders(byte_array, number_of_sensors, number_of_samples, header_length):
    """
    Extract the header from the packet structure: | 4 bytes of headers | 2 bytes * number_of_samples |
    """
    
    headers = [0 for n in range(0, number_of_sensors)]
    try:
            for i in range(0, number_of_sensors):
                header_offset = i * (header_length + number_of_samples * 2)
                
                sensor_number = byte_array[header_offset + 0]
                state = byte_array[header_offset + 1]
                adc_channel = byte_array[header_offset + 2]
                """ The sensor number in the headers are in the range of 1 to 36 """
                headers[i] = (sensor_number, state, adc_channel)  # The sensor number in the header is
                
    except Exception as error:
        raise RuntimeError('Could not decode header. Error: %s' % error)
    
    return headers


def extractSamples(byte_array, number_of_sensors, number_of_samples, header_length):
    """
    Extract the samples from the packet structure: | 4 bytes of headers | 2 bytes * number_of_samples |
    """
    samples = []
    try:
        
        data = np.asarray(byte_array, dtype = np.int8)
        for i in range(0, number_of_sensors):
            
            # Get samples
            offset = i * (header_length + (number_of_samples * 2)) + header_length  # Offset in bytes
            
            try:
                samples.append(np.arange(start = 0, stop = number_of_samples, dtype = np.int16))
            
            except Exception as error:
                raise RuntimeError('Could not append numpy array to list. Error: %s' % error)
            
            try:
                samples[i] = np.frombuffer(data,
                                           dtype = np.int16,
                                           count = number_of_samples,
                                           offset = offset)
            except Exception as error:
                raise RuntimeError('Could not copy data into numpy array. Error: %s' % error)
            
    except Exception as error:
        raise RuntimeError('Could not extract samples. Error: %s' % error)
    
    return samples
    
def convertToUint16t(samples, number_of_sensors):
    if samples[0].dtype != np.dtype(np.uint16):
        try:
            for i in range(0, number_of_sensors):
                samples[i] = samples[i].astype(dtype = 'uint16',
                                               order = 'C',
                                               casting = 'unsafe',
                                               copy = False)
                try:
                    assert (samples[i].dtype == np.dtype(np.uint16))
                except AssertionError as error:
                    raise RuntimeError('casted samples are not of dtype uint16. Assertion: %s' % error)
        except Exception as error:
            raise RuntimeError('Could not cast to uint16 . Error: %s' % error)
        
    return samples

def UnityBasedNormalization(samples, number_of_sensors):
    try:
        for i in range(0, number_of_sensors):
            assert (samples[i].dtype == np.dtype(np.int16))
            for j in range(0, len(samples[i])):
                samples[i][j] = MAXVALUE * (samples[i][j] - np.amin(samples[i])) / (np.amax(samples[i]) - np.amin(samples[i]))
                # verify that samples are within range
                assert ((samples[i][j] <= (MAXVALUE)) & (samples[i][j] >= 0))
    
    except Exception as error:
        raise RuntimeError('Could not perform unity based normalization on the samples. Error: %s' % error)
    
    return samples


def scaleSamples(samples, number_of_sensors):
    # This filter tries to compensate for the inherent non-linearity of the sensor material by applying a logarithmic
    # scalar.
    try:
        for i in range(0, number_of_sensors):
            for k in range(0, len(samples[i])):
                samples[i][k] = 300 * (1 - np.exp(SCALAR * samples[i][k]))  # Plot the equation by
                # exchanging 'samples[i][k]' with 0 < X < 300
                
                # verify that samples are within range
                assert ((samples[i][k] <= 300) & (samples[i][k] >= 0))

    except Exception as error:
        raise RuntimeError('Could not filter data. Error: %s' % error)
    
    return samples

def averagingFilter(samples, number_of_sensors, width_of_filter):
    try:
        assert ((width_of_filter > 0) & (width_of_filter < number_of_sensors))
    except AssertionError as error:
        raise RuntimeError('Width of the averaging filter is not a valid number: \n'
                           '0 < valid number < samples size. Assertion: %s' % error)
    # This averaging filter casts to int32!
    # This averaging filter removes a number of elements equal to its width.
    # TODO Review the issue where the filter truncates the start or end of the array
    try:
        for i in range(0, number_of_sensors):
            cumsum = np.cumsum(np.insert(samples[i], 0, 0))
            samples[i] = (cumsum[width_of_filter:] - cumsum[:-width_of_filter]) / width_of_filter
                
            """if j > (width_of_filter - 1):
                temp_sample = 0
                for k in range(0, width_of_filter):
                    temp_sample = temp_sample + samples[i][j - width_of_filter]

                samples[i][j] = temp_sample/width_of_filter"""
                
    except Exception as error:
        raise RuntimeError('Could not average the samples. Error: %s' % error)
    
    if samples[0].dtype != np.dtype(np.uint16):
        try:
            for i in range(0, number_of_sensors):
                samples[i] = samples[i].astype(dtype = 'uint16',
                                               order = 'C',
                                               casting = 'unsafe',
                                               copy = False)
                try:
                    assert (samples[i].dtype == np.dtype(np.uint16))
                except AssertionError as error:
                    raise RuntimeError('Converted samples are not of dtype uint16. Assertion: %s' % error)
    
        except Exception as error:
            raise RuntimeError('Could not convert from int32 to uint16 . Error: %s' % error)
    
    return samples
    
def mapDataToSensors(headers, samples, number_of_sensors):
    """
    Map the headers and samples to their respective sensor number,
    given by the 'sensor number' field ('0') in the header.
    """
    try:
        temp_samples = [0 for n in range(0, number_of_sensors)]
        temp_headers = [0 for n in range(0, number_of_sensors)]
        
        for i in range(0, number_of_sensors):
            temp_samples[headers[i][0]] = samples[i]
            temp_headers[headers[i][0]] = headers[i]
            
        for i in range(0, number_of_sensors):
            samples[i] = temp_samples[i]
            headers[i] = temp_headers[i]
           
    except Exception as error:
        raise RuntimeError('Could not map data to sensors. Error: %s' % error)

    
    # TODO Clean up the prints. Maybe hide behind a debug flag.
    for i in range(0, number_of_sensors):
        print("FSR" + str(i) + " Avg:   " + str(samples[i].sum() / 512))
        print("FSR" + str(i) + " Max:   " + str(samples[i].max()))
        print("FSR" + str(i) + " Min:   " + str(samples[i].min()) + "\n")
    
    return headers, samples

