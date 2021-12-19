'''
@file       bno055.py

@brief      This file contains a class for obtaining angular data from the bno055 IMU module.

@details    This file acts as a driver for the bno055 inertial measurement unit.
            The driver uses I2C communication to write write settings to the IMU and 
            read the appropriate registers. For this application we are setting the IMU
            to the NDOF fustion mode and retreiving the eularian pitch and roll values in radians.
'''

import pyb
from pyb import I2C

class BNO055:
    '''
    @brief      BNO055 is a class used to contain obtain the Eularian pitch and roll angles from the bno055 module.

    @details    This class communicates with the bno055 module via I2C communication. The functions contained within
                read the appropriate registers from the mode, interpret the contents, and return the results as angles in radians.
    '''
    
    def __init__(self, address): 
        '''
        @brief          This function initializes I2C comminication and inital variables
        
        @param address  This hex value specifies the I2C adress of the bno055 module. This value is 0x28 by default
        
        '''
        
        ## Variable containing I2C address of bno055 (28)
        self.address = address

        #varibale containing address of eularian pitch LSB register on the bno055 module
        self.EUL_Pitch = 0x1E

        #varibale containing address of eularian roll LSB register on the bno055 module
        self.EUL_Roll = 0x1C

        #variable containing address of the unit selection register
        self.UNIT_SEL = 0x3B

        #variable containing address of the operating mode selection register
        self.OPR_MODE = 0x3D

        #initialize I2C bus
        self.i2c = I2C(1,I2C.MASTER) 

        #set operating mode to NDOF
        self.i2c.mem_write(0b00001100,self.address,self.OPR_MODE)

        #leave the individial sensor data as the default values since we only use the fusion data
        self.i2c.mem_write(0b00000000,self.address,self.UNIT_SEL)
        
        #mask used to extract sign bit from MSBit
        self.signMask =0b1000000000000000

        #mask used to remove the sign bit without causing the ad
        self.negMask = 0b0111111111111111

    def Get_thX(self):

        #read both bytes of eularian roll data
        thX = bytearray(self.i2c.mem_read(2,self.address,self.EUL_Roll))

        #bytes are listed LSB first so shift MSB and add
        thX = thX[1]*256+thX[0]

        #get the sign bit from the MSBit of thX
        sign = thX & self.signMask

        if sign:
            #remove sign bit
            thX = thX^self.signMask

            #take the 2's complement
            thX = ~thX+1

            #remove the sign bit again (using & instead of ^ prevents creating a 1 in the 17th bit)
            thX = thX&self.negMask

            #make result negative
            thX = thX*-1

        return (thX)/900

        
    def Get_thY(self):
        #read both bytes of eularian pitch data
        thY = bytearray(self.i2c.mem_read(2,self.address,self.EUL_Pitch))

        #bytes are listed LSB first so shift MSB and add
        thY = thY[1]*256+thY[0]

        #get the sign bit from the MSBit of thY
        sign = thY & self.signMask

        if sign:
            #remove sign bit
            thY = thY^self.signMask

            #take the 2's complement
            thY = ~thY+1

            #remove the sign bit again (using & instead of ^ prevents creating a 1 in the 17th bit)
            thY = thY&self.negMask

            #make result negative
            thY = thY*-1

        return (thY)/900

    def Get_Data(self):
        #call needed functions and return result as a tuple
        return (self.Get_thX(), self.Get_thY())

if __name__ == '__main__':
    imu = BNO055(0x28)
    while True:
        print((imu.Get_thX(),imu.Get_thY()))
        #print(imu.Get_thY())       