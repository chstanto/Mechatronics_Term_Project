'''
@file       Encoder_Driver.py

@brief      This file defines a class capable of reading from the encoder.

@details    The encoder driver set up in this file is able to output
            to another file the motor position, the most recent motor delta,
            and it is also able to zero the motor position.
'''

import pyb

class EncoderDriver:
    '''
    @brief      This class defines the three functions of the encoder driver.
    
    @details    The three functions defined by this class are the
                initialization function, the get position function, the set
                position function, and the zero function. All three are 
                intended to be called by another file.
    '''
    
    def __init__(self, timer_number, ch1_pin, ch2_pin):
        '''
        @brief      Defines parameters needed for an encoder object
        @details    This function accepts 5 inputs to define the appropriate
                    pins and channels needed to use any encoder. Also defines
                    variables needed when updating encoder outputs.
        @param      timer_number    Variable for desired timer number
        @param      ch1_pin         Variable for desired chanel 1 pin
        @param      ch2_pin         Variable for desired chanel 2 pin
        @param      ch1_num         Variable for desired chanel 1 number
        @param      ch2_num         Variable for desired chanel 2 number
        '''
        self.ch1_pin = pyb.Pin(ch1_pin)
        self.ch2_pin = pyb.Pin(ch2_pin)

        self.tim1 = pyb.Timer(timer_number)
        self.tim1.init(prescaler = 0 , period = 0xFFFF)
    
        self.tim1.channel(1 , pin = self.ch1_pin , mode = pyb.Timer.ENC_AB)
        self.tim1.channel(2 , pin = self.ch2_pin , mode = pyb.Timer.ENC_AB)
    
        self.delt1       = [0,0]
        self.zero1       = 0
        self.pos1        = 0
        self.position1   = 0
    
    def update(self):
        '''
        @brief      Function which consistently updates motor position.
        @details    Creates an array of two variables which upon every update
                    is changed to reflect the most recent position and the
                    last position. This array makes it easy to access the
                    most recent position as well as the delta between the
                    last update.
        '''

        self.pos1            = self.tim1.counter() - self.zero1
        self.delt1[0]        = self.delt1[1]
    
        if (self.pos1 - self.delt1[0]) >= 32768:
            self.delt1[1]    = self.pos1 - 65535
        
        elif (self.pos1 - self.delt1[0]) <= -32768:
            self.delt1[1]    = self.pos1 + 65535
        
        else:
            self.delt1[1]    = self.pos1
    
        self.delta1 = self.delt1[1]*360/4000 - self.delt1[0]*360/4000
        
    def get_position(self):
        '''
        @brief      This function returns the current position of the motor.
        @details    This function converts the position value into units of
                    degrees and then returns the most recent position.
        '''
        self.position  = self.delt1[1]*360/4000
        return self.position
        
    def set_position(self):
        '''
        @brief      This function sets the position of the motor to zero.
        @details    Sets the zero value to the current position of the motor
                    so that during the next update the position will reflect
                    the zero. 
        '''
        self.zero1       = self.tim1.counter()
        self.delt1[1]    = 0
        
    def get_delta(self):
        '''
        @brief      This function returns the most recent delta.
        @details    Returns the difference between the motor position at the
                    last two position updates.
        '''
        return self.delta1
        
if __name__ == '__main__':
    enc1 = EncoderDriver(4,'PB6','PB7')
    enc2 = EncoderDriver(8,'PC6','PC7')
    
    while True:
        enc1.update()
        enc2.update()

        print(enc1.get_position())
        #print(enc2.get_position())

        #pyb.delay(1000)
