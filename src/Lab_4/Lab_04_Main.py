'''
@file       Lab_04_Main.py

@brief      This file manages adding collected temperature data to the csv.

@details    This file first imports the mcp9808 temperature sensor driver
            which it initializes with the correct address. Time variables
            are then set up to allow a while loop to collect data at a desired
            rate over a desired period of time. The current definitions will
            collect data every minute for eight hours. Using the with loop the
            desired csv file is opened, and the while loop runs until eight
            hours of data from both the mcp9808 and on board temperature 
            sensor have been added.
@image      html Lab_4_Plot.PNG width=1000px
'''

import pyb
import utime
from mcp9808 import mcp9808

## Variable representing Nucleo temperature pin
stm_temp = pyb.ADCAll(12 , 0x70000)

## Variable representing the interval between temp recordings in milliseconds
interval = 60000
## Variable representing the initial time used for zeroing
start_time = utime.ticks_ms()
## Variable representing the next time that loop should run
next_time = start_time + interval
## Variable representing the total length of data collection in milliseconds
total_time = 28800000

## Variable tracking the number of data points collected
points = 0

## Define the temperature sensor object
mcp = mcp9808(24)

with open('temp_file.csv' , 'w') as file:
    
    # Adding column titles to file
    file.write('Time [s],STM Temp [C],MCP Temp [C]\n')
    
    # Checking that run time has not exceeded total time
    while(next_time <= (start_time + total_time)):
        ## Variable representing the current time
        current_time = utime.ticks_ms()

        if(current_time >= next_time):
            
            ## Zeroed current time to be added to data file
            time = str(current_time - start_time)
            
            # zero nucleo temperature sensor
            stm_temp.read_vref()
            ## Current Nucleo temprature reading to be added to data file
            STM_Temp = str(stm_temp.read_core_temp())
            ## Current MCP9808 temperature reading to add to data file
            MCP_Temp = str(mcp.celsius())
            # Write current time and temp data points to file
            file.write(time+ ',' +STM_Temp+ ',' +MCP_Temp+ '\n')
            
            # Adjust next time to reflect the next interval
            next_time += interval
            # Increment number of data points variable
            points += 1