'''
@file       mcp9808.py

@brief      This file manages the communication between the mcp9808 sensor and the board.

@details    This file acts as a driver for the mcp9808 temperature sensor.
            The driver uses I2C communication to read the ambient temperature
            register stored on the mcp9808 module, and interprets it into
            temperatures in both celsius and fahrenheit.
'''

import pyb
from pyb import I2C

class mcp9808:
    '''
    @brief      mcp9808 is a class used to comntain temperature protocalls.  

    @details    This class initializes I2C communication with the mcp9808 
                module and contains functions for retreiving temperature
                data. 
    '''
    
    def __init__(self, address):
        '''
        @brief          This function initializes I2C comminication and inital variables
        
        @param address  The input address of mcp9808 module. This value is 24 in decimal by default but can be altered using A0, A1, and A2 pins
        '''
        
        ## Variable containing I2C address of mcp9808
        self.address = address

        ## Varibale containing address of ambient temperature register on the mcp9808 module
        self.register = 0b00000101

        self.i2c = I2C(1,I2C.MASTER) 
        ## Mask used to extract sign bit from first temperature byte
        self.signMask = 0b00010000

        ## Mask used to remove first 3 bytes from T_ambient register bytes
        self.tempMask = 0b00011111
    
    def getTemp(self):
        '''
        @brief      This function reads temperature bytes from the sensor and stores them as an int.  
        '''
        ## Variable containing the two bytes read from the ambient temperature register
        temp = bytearray

        ## Variable containing the sign of the temperature bits from the temperature sensor
        sign = int

        # Read 2 bytes from the ambient temperature register and store them in temp
        temp = bytearray(self.i2c.mem_read(2,self.address,self.register))

        # Mask out the first 3 bits which do not contain temperature data
        temp[0] = temp[0] & self.tempMask

        # Use a mask to isolate the sign bit and store it in sign
        sign = temp[0] & self.signMask

        # Concatonate the temperature bytes so they can be operated on as one binary number
        temp = temp[0]*256+temp[1]
        
        # If the temperature is negative, use the 2's complement to adjust the temperature data
        if sign:
            temp = ~temp+1

        # Return an interger that represents the unshifted temperature data
        return temp    
    
    def check(self):
        '''
        @brief This function checks returns the state of the I2C communication status
        
        '''
        
        # Check if I2C communication is ready and return the result
        return self.i2c.is_ready() 

    def celsius(self):
        '''
        @brief This function converts the results of the getTemp funtion into degrees Celsius. 
        
        '''

        # Call getTemp and convert the output to Celsius by shifting it 4 bits to the right
        return self.getTemp()*(2**(-4))
            
    def fahrenheit(self):
        '''
        @brief This function converts the results of the getTemp funtion into degrees Fahrenheit.
        
        '''

        # Call getTemp and convert the output to Fahrenheit
        return self.getTemp()*(2**(-4))*1.8+32

