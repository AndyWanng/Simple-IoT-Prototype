import serial
import time
import oss2
import matplotlib.pyplot as plt
import threading

ser = serial.Serial('COM3', 9600)

access_key_id = ''
access_key_secret = ''
endpoint = ''
bucket_name = ''

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

data_list = []
monitoring = True

def upload_to_oss(data_list, plot_filename):
    if not data_list:
        return

    filename = 'temperature_and_humidity.txt'
    with open(filename, 'w') as f:
        for data in data_list:
            humidity, temperature = data
            f.write(f'Humidity (%): {humidity}\n')
            f.write(f'Temperature (°C): {temperature}\n')

    bucket.put_object_from_file(filename, filename)
    print(f'Data uploaded to OSS: {filename}')

    bucket.put_object_from_file(plot_filename, plot_filename)
    print(f'Plot image uploaded to OSS: {plot_filename}')

def plot_temperature_humidity(data_list):
    if not data_list:
        return

    humidities, temperatures = zip(*data_list)
    timestamps = range(1, len(data_list) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, humidities, label='Humidity (%)')
    plt.plot(timestamps, temperatures, label='Temperature (°C)')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Temperature and Humidity Variation')
    plt.legend()
    plt.grid(True)

    plot_filename = 'temperature_humidity_plot.png'
    plt.savefig(plot_filename)
    plt.close()

    return plot_filename

def monitor_serial_data():
    global data_list
    global monitoring

    while monitoring:
        try:
            data = ser.readline().decode().strip()
            if ',' not in data:
                continue

            humidity, temperature = data.split(',')
            humidity = float(humidity)
            temperature = float(temperature)

            print(f'Humidity: {humidity}%')
            print(f'Temperature: {temperature}°C')

            data_list.append((humidity, temperature))

            time.sleep(2)

        except Exception as e:
            print(f'Error: {e}')
            monitoring = False
            break

monitor_thread = threading.Thread(target=monitor_serial_data)
monitor_thread.start()

input("Press Enter to stop monitoring...\n")

monitoring = False
monitor_thread.join()
print("Process ended, prepare to upload...\n")

plot_filename = plot_temperature_humidity(data_list)
upload_to_oss(data_list, plot_filename)

ser.close()
