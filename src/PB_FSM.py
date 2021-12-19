'''
@file       PB_FSM.py

@brief      This file defines the platform and ball finite state machine.

@details    This file sets up the platform and ball finite state machine used
            to balance the ball on the platform. At the bottom of the file is
            test code which runs the finite state machine at a frequency of 
            20 Hz. The following link contains video of the system performance
            with a brief explanation of its functions. https://bit.ly/3qVk4E3
            
@image      html Lab_9_P_Sim.png width=1000px

@details    The plot above shows the simulation results for the platform only
            when gains were calculated using a percent overshoot of 0.075 and
            a settling time of 0.25 seconds. The resulting gains were as 
            follows: K1 = -0.05, K2 = -1.22.

@image      html Lab_9_PB_Sim.png width=1000px

@details    The plot above shows the simulation results for the platform and
            ball system when gains were calculated using a percent overshoot
            of 0.075 and a settling time of 3 seconds. The resulting gains were
            as follows: K1 = -0.15, K2 = -0.05, K3 = -0.36, K4 = -0.55.
'''

import utime
import pyb

from Motor_Driver import MotorDriver as MD
from P_Controller import P_Controller as PC
from PB_Controller import PB_Controller as PBC
from Touch_Panel_Driver import Touch_Panel as TPD
from bno055 import BNO055 as BNO

class Platform_Ball_Task:
    ## Constant defining state 0 - Initialization
    S0_INIT                    = 0
    
    ## Constant defining state 1 - Zero the Platform
    S1_PLATFORM_ZERO           = 1
    
    ## Constant defining state 2 - Balance the Ball
    S2_BALANCE                 = 2
    
    ## Constant defining state 3 - Fault Correction
    S3_FAULT                   = 3
    
    def Fault_Detection(self , pin):
        '''
        @brief      This method manages fault and prevents danger to user.
        @details    When this method is called by the FSM or external interrupt
                    both motors are disabled and the FSM moves into state
                    3 which waits for a user input before resuming operation.
        '''
        
        self.mot1.disable()
        self.mot2.disable()
        
        self.state = self.S3_FAULT
        
        print('Fault triggered, move platform toward equilibrium and \n'
              'press Nucleo input button to resume operation.')
        
        self.run()
    
    def __init__(self , interval):
        '''
        @brief     Defines variables and objects needed for FSM. 
        @param     interval     Input for time between runs in microseconds
        '''
        
        ##  The amount of time in microseconds between runs of the task
        self.interval = int(interval)

        ## The state to run on the next iteration of the task.
        self.state = self.S0_INIT
        
        ## The timestamp for the first iteration
        self.start_time = utime.ticks_us()
        
        ## The "timestamp" for when the task should run next
        self.next_time = self.start_time + self.interval
        
        ## Defining nucleo user input button as external interrupt
        #self.Fault_Interrupt = pyb.ExtInt(pyb.Pin.board.PB2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, self.Fault_Detection)
        
        ## Setting up Nucleo user button for fault reset
        self.User_Button = pyb.Pin(pyb.Pin.board.PC13,pyb.Pin.IN)
        
        ## Define motor 2, controls rotation about X axis
        self.mot1 = MD(3 , 'PA15' , 'PB4' , 'PB5' , 1 , 2)
        
        ## Define motor 1, controls rotation about Y axis
        self.mot2 = MD(3 , 'PA15' , 'PB0' , 'PB1' , 3 , 4)
        
        ## Define touch panel driver
        self.Touch_Panel = TPD(pyb.Pin.cpu.A1 , pyb.Pin.cpu.A7 , pyb.Pin.cpu.A0 , pyb.Pin.cpu.A6 , 180 , 100 , 90 , 50)
        
        ## Define Initialized Platform Controller
        self.Platform = PC(-0.0515 , -1.2171)
        
        # The calculated gains for the platform ball system
        #self.Platform_Ball = PBC(-0.1518 , -0.0494 , -0.3616 , -0.5509)
        
        ## Define Initialized Platform and Ball Controller
        self.Platform_Ball = PBC(-2 , -0.2 , -2.6 , -2.2)
        
        ## Define BNO055 sensor object
        self.IMU = BNO(0x28)
        
        ## Variable storing two most recent X contact positions
        self.pos_X = [0,0]
        
        ## Variable storing two most recent Y contact positions
        self.pos_Y = [0,0]
        
        ## Variable storing two most recent angles about X
        self.theta_X = [0,0]
        
        ## Variable storing two most recent angles about Y
        self.theta_Y = [0,0]
        
        ## Variable storing number of loops through Platform/Ball control
        self.runs = 0
        
    def run(self):
        '''
        @brief      Runs one iteration of the platform ball task.
        '''
        ## Updates current time
        self.curr_time = utime.ticks_us()
        
        ## Variable storing current touch panel data for each loop
        self.Touch_Data = self.Touch_Panel.Get_Pos()
        
        ## Variable storing current IMU sensor data for each loop
        self.IMU_Data = self.IMU.Get_Data()
        
        # Check to see that platform angle is within operation range which
        # was determined through testing (+- 0.2 radians)
        if(-0.2 <= self.IMU_Data[0] <= 0.2 and -0.2 <= self.IMU_Data[1] <= 0.2):
            pass
        else:
            self.Fault_Detection(1)
        
        # Check that an interval has passed before looping again
        if(self.curr_time >= self.next_time):
            
            if(self.state == self.S0_INIT):
                # Enable and zero duty cycle of both motors
                self.mot1.enable()
                self.mot1.set_duty(0)
                self.mot2.enable()
                self.mot2.set_duty(0)
                # Transition to state 2 where platform will be balanced
                self.transitionTo(self.S1_PLATFORM_ZERO)
                print('INIT State')
                
            elif(self.state == self.S1_PLATFORM_ZERO):
                if(self.Touch_Data[2] == False):
                    # Update angle data and ensure that first velocity value no skewed
                    if(self.runs == 0):
                        self.theta_X[0] = self.IMU_Data[0]
                        self.theta_X[1] = self.IMU_Data[0]
                        self.theta_Y[0] = self.IMU_Data[1]
                        self.theta_Y[1] = self.IMU_Data[1]
                    else:
                        self.theta_X[0] = self.theta_X[1]
                        self.theta_X[1] = self.IMU_Data[0]
                        self.theta_Y[0] = self.theta_Y[1]
                        self.theta_Y[1] = self.IMU_Data[1]
                    
                    # Calculate angular velocity based on last two positions and interval
                    theta_D_X = (self.theta_X[1] - self.theta_X[0])/(self.interval*10^(-6))
                    theta_D_Y = (self.theta_Y[1] - self.theta_Y[0])/(self.interval*10^(-6))
                    
                    # Increment runs
                    self.runs += 1
                    
                    # No ball contact, find motor duty cycles to level
                    duty1 = self.Platform.get_D(theta_D_X , self.IMU_Data[0])
                    duty2 = self.Platform.get_D(theta_D_Y , self.IMU_Data[1])
                    
                    # Adjust duty calculation for motor deadzone 0-20%
                    if(duty1 > 0):
                        duty1 = duty1*80/100 + 20
                    else:
                        duty1 = duty1*80/100 - 20
                    if(duty2 > 0):
                        duty2 = duty2*80/100 + 20
                    else:
                        duty2 = duty2*80/100 - 20
                    
                    # Set duty cycles of both motors, check range
                    if(-100 <= duty1 <= 100 and -100 <= duty1 <= 100):
                        self.mot1.set_duty(-duty1)
                        self.mot2.set_duty(-duty2)
                    else:
                        self.runs = 0
                        # Duty is greater than 100%, run fault method
                        self.Fault_Detection(1)
                else:
                    # When contact is detected FSM will transition to ball control
                    self.transitionTo(self.S2_BALANCE)
                    self.runs = 0
                
            elif(self.state == self.S2_BALANCE):
                # Update position and angle data, avoid invalid velocity calc on first run
                if(self.runs == 0):
                    self.pos_X[0] = self.Touch_Data[0]
                    self.pos_X[1] = self.Touch_Data[0]
                    self.pos_Y[0] = self.Touch_Data[1]
                    self.pos_Y[1] = self.Touch_Data[1]
                    
                    self.theta_X[0] = self.IMU_Data[0]
                    self.theta_X[1] = self.IMU_Data[0]
                    self.theta_Y[0] = self.IMU_Data[1]
                    self.theta_Y[1] = self.IMU_Data[1]
                else:
                    self.pos_X[0] = self.pos_X[1]
                    self.pos_X[1] = self.Touch_Data[0]
                    self.pos_Y[0] = self.pos_Y[1]
                    self.pos_Y[1] = self.Touch_Data[1]
                    
                    self.theta_X[0] = self.theta_X[1]
                    self.theta_X[1] = self.IMU_Data[0]
                    self.theta_Y[0] = self.theta_Y[1]
                    self.theta_Y[1] = self.IMU_Data[1]
                    
                # Calculate ball velocity and platform angular velocity
                vel_X = (self.pos_X[1] - self.pos_X[0])/(self.interval*10^(-6))
                vel_Y = (self.pos_Y[1] - self.pos_Y[0])/(self.interval*10^(-6))
                
                theta_D_X = (self.theta_X[1] - self.theta_X[0])/(self.interval*10^(-6))
                theta_D_Y = (self.theta_Y[1] - self.theta_Y[0])/(self.interval*10^(-6))
                
                if(self.Touch_Data[2] == True):
                    
                    # Use controller driver to find motor duty cycles
                    duty1 = self.Platform_Ball.get_D(vel_X , theta_D_X , self.Touch_Data[0] , self.IMU_Data[0])
                    duty2 = self.Platform_Ball.get_D(vel_Y , theta_D_Y , self.Touch_Data[1] , self.IMU_Data[1])
                    
                    # Adjust duty calculation for motor deadzone 0-20%
                    if(duty1 > 0):
                        duty1 = duty1*80/100 + 20
                    else:
                        duty1 = duty1*80/100 - 20
                    if(duty2 > 0):
                        duty2 = duty2*80/100 + 20
                    else:
                        duty2 = duty2*80/100 - 20
                    
                    # Set duty cycles of both motors, check range
                    if(-100 <= duty1 <= 100 and -100 <= duty2 <= 100):
                        self.mot1.set_duty(-duty1)
                        self.mot2.set_duty(-duty2)
                    else:
                        self.runs = 0
                        # Duty is greater than 100%, run fault method
                        self.Fault_Detection(1)
                        
                    # Increment runs variable
                    self.runs += 1
                    
                else:
                    self.runs = 0
                    # No contact on platform, return to platform level state
                    self.transitionTo(self.S1_PLATFORM_ZERO)
                    
            elif(self.state == self.S3_FAULT):
                if(self.User_Button.value() == 0):
                    # User has pressed button, return to state 0
                    self.transitionTo(self.S0_INIT)
                else:
                    pass
                
            # Specifying the next time the task will run
            self.next_time = utime.ticks_add(self.next_time, self.interval)

        else:
                # Invalid state code (error handling)
                pass
        
    def transitionTo(self, newState):
        '''
        @brief      Sets new state
        @param      newState    Variable representing the desired new state
        '''
        self.state = newState
        
# Test code will run above class when file is executed by Nucleo
if __name__ == '__main__':
    
    ## Defines FSM task to run at 5000 microsecond interval, 20 Hz
    test = Platform_Ball_Task(5000)
    
    # Task will run until keyboard interrupt
    while True:
        test.run()
    