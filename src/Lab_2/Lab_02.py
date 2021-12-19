'''
@file       Lab_02.py

@brief      This file runs a Think Fast game on the nucleo.

@details    This program prompts the user to press a button on the nucleo
            after they have seen an LED turn on. The program makes use of an
            external interrupt(the button) to break a while loop and collect
            data on every user input. If either the user presses ctrl-c or 
            waits too long after an LED flash, the program prints the users
            average response time based on all of their attempts.

'''

import utime
import pyb
import urandom
import micropython

## Setting up Nucleo LED
pinA5 = pyb.Pin(pyb.Pin.cpu.A5 , pyb.Pin.OUT_PP)

#prevent callback fcn errors by setting up memory allocation
micropython.alloc_emergency_exception_buf(200)

# Set LED to off upon program start
pinA5.value(0)

## Variable representing the reaction time of a single user attempt
reaction_time = 0

## Variable representing sum of all reaction times
total_reaction_time = 0

## Variable representing the number of game attempts by user
attempts = 0

def UserInterrupt(pin):
    '''
    @brief      This is the callback function for the user button press.
    @details    This function runs on every button press and collects data
                on the user's performance. This function updates both the
                total response time and number of attempts which are 
                ultimately used to calculate the users average response time.
    @param pin  This fulfills the parameter requirement of the callback fcn.
    '''
    
    global reaction_time
    global total_reaction_time
    global attempts
    
    reaction_time = button_timer.counter()
    total_reaction_time += reaction_time
    attempts += 1
    
    pinA5.value(0)
    button_timer.deinit()

def CalcAvg(time , timer):
    '''
    @brief      This function converts timer output to seconds.
    @details    The nucleo timer responds in counts, so this function converts
                the timer counts to seconds by dividing by the frequency
                and period.
    @param time The amount of time to be converted.
    '''
    ## Variable represents the inputted timer count converted to seconds.
    avg = time/(timer.freq()*timer.period()*attempts)
    return avg

def ReturnResults(timer):
    '''
    @brief          This function prints the users performance results.
    @details        After either pressing ctrl-c or waiting too long on an 
                    attempt, this function then provides the user with their
                    performance data. Assuming the user made at least one 
                    attempt it will print the average reaction time, otherwise
                    it will print N/A. This function then deactivates the 
                    timer and interrupt button, and turns the LED off.
    @param timer    This fulfills the parameter requirement.
    '''
    if(attempts > 0):
        avg_reaction_time = CalcAvg(total_reaction_time , timer)
        pass
    else:
        avg_reaction_time = 'N/A'
        pass
    
    print('After ' , attempts , ' attempts your average reaction time \n'
          'was ' , avg_reaction_time , ' seconds, better luck next time!')
    
    timer.deinit()
    Interrupt_Button.disable()
    pinA5.value(0)
    
def TimerCallback(timer):
    '''
    @brief          This is the callback function in case of timer overflow.
    @details        The timer is set up such that it overflows at 1 second
                    which runs this function. This overflow function changes
                    the input status parameter to False and prints Too Slow.
                    Ultimately this leads the program to print results and end.
    @param timer    Unused parameter to fulfill callback parameter requirement.
    '''
    global input_status
    
    # Sets input status to false to show that user has waited too long
    input_status = False
    pinA5.value(0)
    timer.deinit()
    
    print('Too Slow!')
    
## Defining nucleo user input button as external interrupt
Interrupt_Button = pyb.ExtInt(pyb.Pin.board.PC13, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, UserInterrupt)

print('Test your reaction time! \n' 
      'When the Nucleo LED turns on press the blue button as fast as you can!')
    
## Tracks if the user has pressed the input button
input_status = True

try:
    while True:
        if(input_status == True):
            
            ## Variable representing random time between 2 and 3 seconds
            sleep_time = urandom.randint(int(2e6) , int(3e6))
            utime.sleep_us(sleep_time)
            
            #turn on LED
            pinA5.value(1)
            
            #set up timer
            button_timer = pyb.Timer(2 , period = int(pyb.freq()[2])-1 , prescaler = 0 , callback = TimerCallback)
            button_timer.counter(0)
            
            if(reaction_time > 0):
                print('Attempt ' , attempts , ':' , CalcAvg(reaction_time , button_timer)*attempts , ' seconds')
                pass
            utime.sleep_us(int(1e6))
        
        elif(input_status == False):
            #Interrupt_Button.disable()
            ReturnResults(button_timer)
            input_status = True
            break
        
except(KeyboardInterrupt):
    # This exception will run if user presses ctrl-c
    ReturnResults(button_timer)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    