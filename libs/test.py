from libs.test_data_generator import SensorSim

test = SensorSim(10, 10, 3)

# generated_string = test.generate_string()
# decoded_string = test.decode_string(generated_string)

generated_array = test.generate_byte_array()
decoded_array = test.decode_byte_array(generated_array)



