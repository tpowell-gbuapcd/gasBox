#!/usr/bin/env python3

import sys
import argparse
import busio, board
import purple_air_diagnostic as pa
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--wait_time', type=int, help='The amount of seconds to wait between reads. Must be at least 2 seconds long. Default is 2 seconds. ex.) 2', default=2)
parser.add_argument('-n', '--n_points', type=int, help='The number of points to average over. Total time span between writes to csv is n_points*wait_time. Default is 300 ex.) 300 (300*2 = 10 minute averaging)', default=300)
parser.add_argument('-l', '--log', type=str, help='Would you like to print the output to screen? Yes or No? Otherwise, direct output to file.txt. Default is No.', default='No')
args = parser.parse_args()

if args.log == 'No':
    sys.stdout = open("/home/tpowell/gasCode/file.txt", "w")

try:
    print("Initializing I2C devices")
    i2c = busio.I2C(board.SCL, board.SDA)
    device_list = pa.device_list(i2c)
    mux, tca = pa.mux_init(i2c, device_list)
except Exception as e:
    print(e)

wait_time = args.wait_time
n_points = args.n_points

j = 0 
while j == 0:
    
    try:
        print("Initializing Dictionary")
        device_data = pa.make_device_dict(device_list)
        print("Dictionary Initialized: ", datetime.now())
    except Exception as e:
        print(e)

    try:
        print("Capturing Data")
        data_dict = pa.capture_data(device_data, tca, wait_time, n_points, i2c)
        print("Dictionary Filled: ", datetime.now())
    except Exception as e:
        print(e)
    
    try:
        print("Averaging Data")
        avg_dict = pa.get_averages(data_dict)
        print("Dictionary Averaged: ", datetime.now())
    except Exception as e:
        print(e)

    if args.log == 'Yes':
        try:
            print("Printing Averaged Data")
            pa.print_avg_data(avg_dict)
            print("Averaged Data Printed: ", datetime.now())
        except Exception as e:
            print(e)

    try:
        print("Writing Data")
        pa.csv_write(avg_dict)
        print("CSV Written: ", datetime.now())
    except Exception as e:
        print(e)
