try:
    import numpy as np

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
                headers[i] = (sensor_number - 1, state, adc_channel)  # The sensor number in the header is
                
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
    
    
def mapDataToSensors(headers, samples, number_of_sensors):
    """
    Map the headers and samples to their respective sensor number,
    given by the 'sensor number' field ('0') in the header.
    """
    try:
        temp_samples = [0 for n in range(0, number_of_sensors)]
        temp_headers = [0 for n in range(0, number_of_sensors)]
        
        for i in range(0, number_of_sensors):
            temp_samples[i] = samples[headers[i][0]]
            samples[i] = temp_samples[i]
            
            temp_headers[headers[i][0]] = headers[i]
            headers[i] = temp_headers[i]
           
    except Exception as error:
        raise RuntimeError('Could not map data to sensors. Error: %s' % error)

    # TODO Clean up the prints. Maybe hide behind a debug flag.
    for i in range(0, number_of_sensors):
        print("FSR" + str(i) + " Max:   " + str(samples[i].max()))
        print("FSR" + str(i) + " Min:   " + str(samples[i].min()) + "\n")
        
    return headers, samples

