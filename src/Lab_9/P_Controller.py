'''
@file       P_Controller.py

@brief      This file defines the controller class for the platform system.

@details    This class contains two methods which aid in the control of the
            platform system. The init method saves gain values inputted
            by the user, and the get_D method returns the desireable duty cycle.
'''

class P_Controller:
    '''
    @brief      
    
    @details    
    '''
    
    def __init__ (self , K1 , K2):
        '''
        @brief      Defines gain values based on user input.
        @param K1   Platform angular velocity gain
        @param K2   Platform angular position gain
        '''
        self.K1 = K1
        self.K2 = K2
        
    def get_D (self , theta_d , theta):
        '''
        @brief      Calculates duty cycle based on gear ratio and torque gain.
        @param theta_d    Platforms angular velocity
        @param theta      Platform angle
        '''
        # Calculate torque based on inputs and gains
        torque = self.K1*theta_d + self.K2*theta
        # Calculate desired motor duty based on torque
        D = (torque * 2.21 * 100)/(0.0138 * 12 * 4)
        
        return(D)