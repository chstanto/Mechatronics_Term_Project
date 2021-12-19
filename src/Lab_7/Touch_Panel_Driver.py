'''
@file       Touch_Panel_Driver.py

@brief      This driver allows the nucleo to gather position data from the touch panel.

@details    This file defines the Touch_Panel class which has five methods.
            Methods include init, Scan_x, Scan_y, Scan_z, and get_pos. By using
            the provided methods the user can determine if anything is in contact
            with the touch panel and the location of that contact. The image
            below shows the wiring and soldering setup of the touch panel used
            when testing for this driver.

@image      html TP_Setup.PNG width=1000px

@details    The image below shows the average time to use the get_pos method
            after looping it 100 times. Testing code was written at the bottom
            of the program to generate this data.
            
@image      html TP_Avg_Time.PNG width=1000px

'''

import pyb
import utime

class Touch_Panel:
    '''
    @brief        

    @details    
    '''
    
    def __init__(self , xp , xm , yp , ym , width , height , center_x , center_y):
        '''
        @brief      
        
        @param xp   Pin to be used for positive X direction.
        @param xm   Pin to be used for negative X direction.
        @param yp   Pin to be used for positive Y direction.
        @param ym   Pin to be used for negative Y direction.
        @param width    Panel width in mm, corresponds to X axis.
        @param height   Panel height in mm, corresponds to Y axis.
        @param center_x Panel center coordinate in mm, X direction.
        @param center_y Panel center coordinate in mm, Y direction.
        
        '''
        ## Pin object to be used for x positive.
        self.xp = xp
        ## Pin object to be used for x negative.
        self.xm = xm
        ## Pin object to be used for y positive.
        self.yp = yp
        ## Pin object to be used for y negative.
        self.ym = ym
        ## Variable defining the width of the touch panel in mm.
        self.width = width
        ## Variable defining the height of the touch panel in mm.
        self.height = height
        ## Variable defining the measured x-axis center of the touch panel in mm.
        self.center_x = center_x
        ## Variable defining the measured y-axis center of the touch panel in mm.
        self.center_y = center_y
        
        ## Variable defining the adc threshold for touch panel contact.
        self.z_bound = 4000
        ## Varaible defining the max adc output along the x-axis.
        self.x_max = 3700
        ## Variable defining the min adc output along the x-axis.
        self.x_min = 460
        ## Variable defining the max adc output along the y-axis.
        self.y_max = 3780
        ## Variable defining the min adc output along the y-axis.
        self.y_min = 210
        
    def Scan_x(self):
        '''
        @brief      Finds the x position of contact on touch panel.
        
        @details    The four touch panel pins are defined to find the x position
                    of contact on the touch panel. This requires the positive x
                    pin be set to input, x negative pin be set to ground, y
                    positive pin be set to analog, and y negative pin be set 
                    to ADC. The ADC reading is then converted to mm and zeroed
                    using the defined panel x center.
        
        @return     Method returns zeroed x contact position on touch panel.
        '''
        
        self.xp.init(mode = pyb.Pin.OUT_PP, value = 1)
        self.xm.init(mode = pyb.Pin.OUT_PP, value = 0)
        self.yp.init(mode = pyb.Pin.ANALOG) 
        self.ym.init(mode = pyb.Pin.IN)
        ## ADC object reading output from y negative pin on touch panel.
        self.adc_ym = pyb.ADC(self.ym)
        ## Variable storing the x position ADC output from touch panel.
        self.x_val = self.adc_ym.read()
        ## Variable storing the converted and zeroed ADC output for x position.
        self.x_mm = self.x_val/(self.x_max-self.x_min)*self.width - self.center_x
        
        return(self.x_mm)
    
    def Scan_y(self):
        '''
        @brief      Finds the x position of contact on touch panel.
        
        @details    The four touch panel pins are defined to find the y position
                    of contact on the touch panel. This requires the positive y
                    pin be set to input, y negative pin be set to ground, x
                    positive pin be set to analog, and x negative pin be set 
                    to ADC. The ADC reading is then converted to mm and zeroed
                    using the defined panel y center.
        
        @return     Method returns zeroed y contact position on touch panel.
        
        '''
        self.yp.init(mode = pyb.Pin.OUT_PP, value = 1)
        self.ym.init(mode = pyb.Pin.OUT_PP, value = 0)
        self.xp.init(mode = pyb.Pin.ANALOG) 
        self.xm.init(mode = pyb.Pin.IN)
        ## ADC object reading output from x negative pin on touch panel.
        self.adc_xm = pyb.ADC(self.xm)
        ## Variable storing the y position ADC output from touch panel.
        self.y_val = self.adc_xm.read()
        ## Variable storing the converted and zeroed ADC output for y position.
        self.y_mm = self.y_val/(self.y_max-self.y_min)*self.height - self.center_y
        
        return(self.y_mm)

    def Scan_z(self):
        '''
        @brief      Determines if there is contact on the touch panel.
        
        @details    The four touch panel pins are defined to determine if the 
                    touch panel is experiencing contact. This requires the positive y
                    pin be set to input, x negative pin be set to ground, x
                    positive pin be set to analog, and y negative pin be set 
                    to ADC. The ADC reading is then converted to mm and zeroed
                    using the defined panel y center.
        
        @return     This method returns either a true or false depending on contact.
        
        '''
        self.yp.init(mode = pyb.Pin.OUT_PP, value = 1)
        self.xm.init(mode = pyb.Pin.OUT_PP, value = 0)
        self.xp.init(mode = pyb.Pin.ANALOG) 
        self.ym.init(mode = pyb.Pin.IN)
        ## ADC object reading output from y negative pin on touch panel.
        self.adc_ym = pyb.ADC(self.ym)
        ## Variable storing the z ADC output from touch panel.
        self.z_val = self.adc_ym.read()
        
        if(self.z_val < self.z_bound):
            return(True)
        else:
            return(False)
            
    def Get_Pos(self):
        '''
        @brief      Generates tuple describing contact position on touch panel.
        
        @details    This method uses the Scan_x, Scan_y, and Scan_z methods to
                    generate a tuple which indicates if there is contact and
                    the location of the contact.
        
        @return     Returns a tuple with (x_position, y_position, contact T/F).
        '''
        
        return((self.Scan_x() , self.Scan_y() ,self.Scan_z()))
    
    
if __name__ == '__main__':
    xm = pyb.Pin.cpu.A1
    xp = pyb.Pin.cpu.A7
    ym = pyb.Pin.cpu.A0
    yp = pyb.Pin.cpu.A6
    
    TP = Touch_Panel(xp, xm, yp, ym, 180, 100, 90, 50)
    init_time = utime.ticks_us()
    runs = 100
    
    for n in range(runs):
        
        scan = TP.Get_Pos()
    
    print('Average Run Time Test!')
    print('Initial Time: {:} microseconds' .format(init_time))
    print('Number of Runs: {:}' .format(runs))
    print('Final Time: {:} microseconds' .format(utime.ticks_us()))
    print('Average Run Time: {:} microseconds' .format((utime.ticks_us()-init_time)/runs))
    
        