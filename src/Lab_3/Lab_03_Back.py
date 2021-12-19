'''
@file       Lab_03_Back.py

@brief      Backend of lab 3 to be run on Nucleo and collect data.

@details    This file will run on the Nucleo and collect voltage data to be
            sent via serial to spyder. This program will initially wait
            for input from spyder, after which it will again wait for user
            input through the blue button. The button press causes an interrupt
            which starts the data collection of the button pin voltage. This
            data is then converted to voltage and sent back to spyder.
'''

import pyb
from pyb import UART
import array
import micropython

## Defines serial input port
myuart = UART(2)
## Defines the pin for the user input button
ADCPin = pyb.Pin(pyb.Pin.board.PA0)
## Defines the timer to be used
timer = pyb.Timer(2 , prescaler = 79 , period = int(100))
## Defines memory buffer to be used in data collection
buffer = array.array('H' , (0 for index in range (101)))
## Variable defines the analog to digital converter pin
adc = pyb.ADC(ADCPin)
## Variable representing the current state of the program
state = 0

## Setting up Nucleo LED
pinA5 = pyb.Pin(pyb.Pin.cpu.A5 , pyb.Pin.OUT_PP)

#prevent callback fcn errors by setting up memory allocation
micropython.alloc_emergency_exception_buf(200)

# Set LED to off upon program start
pinA5.value(0)

def UserInterrupt(pin):
    '''
    @brief      This is the callback function for the user button press.
    @details    This function is called when the blue user button is pressed.
                The only thing this callback does is adjust the state to the
                data collection state in order to capture the pin voltage.
    @param pin  This fulfills the parameter requirement of the callback fcn.
    '''
    
    global state
    
    state = 2
    # Turns LED off
    pinA5.value(0)
    
    
## Defining nucleo user input button as external interrupt
Interrupt_Button = pyb.ExtInt(pyb.Pin.board.PC13, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, UserInterrupt)
    
while True:
    # State 0 waits for serial input to indicate start
    if(state == 0):
        #print('Waiting for Spyder Input')
        # Check for any serial input from spyder
        if(myuart.any() != 0):
            state = 1
            
    # State 1 waits for the user button press while collecting data
    elif(state == 1):
        # Turns LED on to indicate to user to press button
        pinA5.value(1)
        timer.counter(0)
        # Constantly filling buffer with adc data until button press
        adc.read_timed(buffer , timer)
        pass

    # State 2 checks data for step
    elif(state == 2):
        # Checks first and last value of buffer to confirm step up
        if(buffer[-1] >= 4080 and buffer[0] <=0):
            state = 3
        # In case of no step return to data collection
        else:
            state = 1
            
    # State 3 converts data to voltage and sends via serial
    elif(state == 3):
        # Looping through each value in array and converting to voltage
        for n in range(len(buffer)):
            # Convert buffer data to voltage based on provided ratio
            ## Variable representing adc data converted to voltage
            voltage = int(buffer[n])*3.3/4095
            # Send each individual voltage value via serial
            myuart.write('{:}\r\n' .format(voltage))
        
        break
        
Interrupt_Button.disable()
        
