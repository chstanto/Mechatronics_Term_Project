'''
@file       Lab_03_Front.py

@brief      This is the frontend of lab 3 which recieves, plots, and saves data.

@details    When run, this program first asks the user for an input. If the
            user provides the correct input it is sent to the backend of the
            lab on the Nucleo which starts the data collection. This program
            then waits to recieve the data via serial communication, after
            which it plots the data as a function of time and saves both
            the time and voltage data in a csv file.
'''


import serial
import numpy
import matplotlib.pyplot as plt

ser = serial.Serial(port='COM3',baudrate=115273,timeout=1)

inv = input('Input G to initialize program. \n' 
      'Next press blue button on Nucleo to begin data collection. \n'
      'LED on Nucleo will indicate when to push button, may need to press \n'
      'more than once if LED does not turn off. \n')

## Variable representing the current program state
state = 0

## Variable holding the data recieved from the Nucleo
data = []

## Variable representing voltage data
voltage = []

try:
    while True:
        # State 0 checking the user input
        if(state == 0):
            if(inv == 'G'):
                state = 1
            else:
                inv = input('Invalid input, press G to initialize program. \n')
        # State 1 sending character via serial to Nucleo to indicate start
        elif(state == 1):
            ser.write(str(inv).encode('ascii'))
            state = 2
        # State 2 waiting for data from nucleo and organizing that data
        elif(state == 2):
            if(len(data) < 101):
                if(ser.in_waiting != 0):
                    data.append(ser.readline().decode('ascii').strip())
            elif(len(data) == 101):
                for n in range(len(data)):
                    ## Varaible storing the stripped and split voltage data from Nucleo
                    voltage.append(float(data[n]))
                state = 3
        # State 3 plotting data and saving as csv file
        elif(state == 3):
            ## Variable storing the array of time data
            time = numpy.arange(0 , 101)
            # Plotting and setting up plot with proper labels and title
            plt.plot(time , voltage , "--b")
            plt.xlabel('Time, t [us]')
            plt.ylabel('Voltage, V [volts]')
            plt.title('Pin A5 Voltage vs Time')
            plt.show()
            # Saving both time and voltage data in a single csv file
            numpy.savetxt('VoltageTimeData.csv' , (time , voltage))
            break

except(KeyboardInterrupt):
    # This exception will run if user presses ctrl-c
    ser.close()
    
ser.close()
    