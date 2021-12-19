'''
@file       PB_Controller.py

@brief      This file defines the controller class for the ball/platform system.

@details    This class contains two methods which aid in the control of the
            ball and platform system. The init method saves gain values inputted
            by the user, and the get_D method returns the desireable duty cycle.
'''

class PB_Controller:
    '''
    @brief      
    
    @details    
    '''
    
    def __init__ (self , K1 , K2 , K3 , K4):
        '''
        @brief      Defines gain values based on user input.
        @param K1   Ball velocity gain
        @param K2   Platform angular velocity gain
        @param K3   Ball position gain
        @param K4   Platform angle gain
        '''
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.K4 = K4
        
    def get_D (self , pos_d , theta_d , pos , theta):
        '''
        @brief      Calculates duty cycle based on gear ratio and torque gain.
        @parram x_d       Balls linear velocity along platform
        @param theta_d    Platforms angular velocity
        @param x          Balls position
        @param theta      Platform angle
        '''
        # Calculate torque based on inputs and gains
        torque = self.K1*pos_d + self.K2*theta_d + self.K3*pos + self.K4*theta
        # Calculate desired motor duty based on torque
        D = (torque * 2.21 * 100)/(0.0138 * 12 * 4)
        
        return(D)