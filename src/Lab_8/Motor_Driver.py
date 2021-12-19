'''
@file       Motor_Driver.py

@brief      Sets up a class which can adjust power to the motor.

@details    This file defines a class which will allow a user to adjust the
            duty cycle of any two motors connected to the Nucleo. This file makes
            use of the pyb module for setting up pins and timers.
'''

import pyb

class MotorDriver:
    '''
    @brief      Sets up methods required to control a motor.
    
    @details    The Motor Driver class allows the user to set up two motors
                using the __init__ method. This method assigns the appropriate
                pins, timers, and channels required by the motors. The class also
                includes the enable and disable methods which set the motors
                enable pin either to high or low. Finally the set duty method 
                allows the user to input a desired motor duty cycle after it has
                been enabled.
    '''
    
    def __init__ (self , timer , nSLEEP_pin , IN1_pin , IN2_pin, channel_A, channel_B):
        '''
        @brief              Sets up pins and timers for two motors (1 and 2).
        @param timer        A timer object used PWM generation on inputs 1,2.
        @parram nSLEEP_pin  A pin object used to define enable pin.
        @param IN1_pin      A pin object used to define half bridge input 1.
        @param IN2_pin      A pin object used to define half bridge input 2.
        @param timer        A timer object used PWM generation on inputs 1,2.
        @param channel_A    Defines the channel for the IN1 pin
        @param channel_B    Defines the channel for the IN2 pin
        '''
        self.enable_pin = pyb.Pin(nSLEEP_pin, pyb.Pin.OUT_PP)
        self.enable_pin.low()
        
        self.M1_pos = pyb.Pin(IN1_pin)
        self.M1_neg = pyb.Pin(IN2_pin)
        
        self.timer1 = pyb.Timer(timer , freq = 20000)
        self.M1CH1 = self.timer1.channel(channel_A , pyb.Timer.PWM , pin = self.M1_pos)
        self.M1CH2 = self.timer1.channel(channel_B , pyb.Timer.PWM , pin = self.M1_neg)
        
        #print('M1 Driver Created')
        
    def enable (self):
        '''
        @brief  Sets the motors enable pin to high, allowing operation.
        '''
        self.enable_pin.high()
        
        #print ('Enabling Motors')
        
    def disable (self):
        '''
        @brief  Sets the motors enable pin to low, disabling operation.
        '''
        self.enable_pin.low()
            
        #print('Disabling Motors')
        
    def set_duty (self , duty):
        
        '''
        @brief  Adjusts the motors duty cycle based on input parameter.
        @param duty         A signed integer holding PWM signal duty cycle.
        '''
        if(duty >= 0):
            self.M1CH1.pulse_width_percent(0)
            self.M1CH2.pulse_width_percent(duty)
        else:
            self.M1CH1.pulse_width_percent(duty*(-1))
            self.M1CH2.pulse_width_percent(0)
        
        #print('M1 Duty Set')
    
if __name__ == '__main__':
    mot1 = MotorDriver(3,'PA15','PB4','PB5',1,2)
    mot2 = MotorDriver(3,'PA15','PB0','PB1',3,4)
    
    mot1.enable()
    mot2.enable()

    try:
        while True:
            mot1.set_duty(50)
            mot2.set_duty(50)
            print(50)
            pyb.delay(1000)
            mot1.set_duty(40)
            mot2.set_duty(40)
            print(40)
            pyb.delay(1000)
            mot1.set_duty(30)
            mot2.set_duty(30)
            print(30)
            pyb.delay(1000)
            mot1.set_duty(20)
            mot2.set_duty(20)
            print(20)
            pyb.delay(1000)
            mot1.set_duty(10)
            mot2.set_duty(10)
            print(10)
            pyb.delay(1000)
            mot1.set_duty(0)
            mot2.set_duty(0)
            print(0)
            pyb.delay(1000)
            ind = 50
            while ind >= -50:
                ind -= 1
                mot1.set_duty(ind)
                print(ind)
                pyb.delay(200)


    except KeyboardInterrupt:
        mot1.disable()
        mot2.disable()
