from machine import ADC, Pin, UART
import utime

          # -------- Initialize the ADC pin --------
adc = ADC(Pin(26))  # GP26 corresponds to ADC0

# -----Initialize UART for Bluetooth communication --------
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# -----These are the reference voltage and the ADC's resolution ---------
vref = 3.3  # The maximum voltage the ADC can read
adc_resolution = 65535  # The range of values the ADC can output



def read_wind_speed():
    # Read the ADC value
    adc_value = adc.read_u16()
    # Convert the ADC value to voltage (3.3V reference, 16-bit resolution)
    voltage = adc_value * vref / adc_resolution
    return voltage

def append_wind_speed_data_to_file(timestamp_str, voltage):
    try:
        # Open the file in append mode
        with open("wind_speed_voltage.csv", "a") as data_file:
            # Write the voltage and timestamp to the file
            data_file.write("{}, {:.2f}\n".format(timestamp_str, voltage))
    except Exception as e:
        print("Error writing to file:", e)

def main():
    while True:
        voltage = read_wind_speed()
        # Print the voltage (which corresponds to wind speed)
    
        # Get the current timestamp
        timestamp = utime.localtime()
        timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            timestamp[0], timestamp[1], timestamp[2], 
            timestamp[3], timestamp[4], timestamp[5]
        )
        
        
        
        # Append data to the file
        append_wind_speed_data_to_file(timestamp_str, voltage)
        
        print("Wind speed voltage:", voltage)
    
        # Print the timestamp and voltage to the Thonny console
        print("Timestamp: {}, Wind speed voltage: {:.2f}V".format(timestamp_str, voltage))
    
        # Send the voltage via Bluetooth
        uart.write(f"{timestamp_str},{voltage}\n")
        
        utime.sleep(1)



# Initialize the data file with headers if it doesn't exist
try:
    with open("wind_speed_voltage.csv", "r") as data_file:
        pass
except OSError:
    with open("wind_speed_voltage.csv", "w") as data_file:
        data_file.write("Timestamp,Voltage\n")

try:
    main()
except KeyboardInterrupt:
    print("Program interrupted.")
