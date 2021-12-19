'''
@page       2 System Simulation Results

@brief      This page discusses the simulation results for the system.

@details    Plots showing the motion of both the platform and the ball were
            generated for multiple initial system conditions in MATLAB. This
            was accomplished by first linearizing the equations of motion and
            then simulating the linearized system at different initial ball
            and platform positions. See 
            https://bitbucket.org/chstanto/me405_labs/src/master/Lab_6/ for 
            MATLAB code and more information.

@image      html Case_A_Image.png width=1000px

@details    The results for Case A above show the response of the system at
            equilibrium. It acts exactly as we would expect because when the
            ball starts directly over the center of the platform there should
            be no movement in the system.
            
@image      html Case_B_Image.png width=1000px

@details    The results for Case B above show the response of the system when
            the ball has been offset by 5 cm. The exponential response of both
            the balls motion and platforms motion is expected because as the 
            ball rolls further from center it should cause a greater moment on
            the platform, causing the angle to increase and thus increasing
            the velocity of the ball.

@image      html Case_C_Image.png width=1000px

@details    The results for Case C above show the response of the system when
            the platform has been offset by 5 degrees. The offset causes the
            ball to begin rolling and increase velocity while the platform
            continues to rotate further in the direction of the offset.

@image      html Case_D_Image.png width=1000px

@details    The results for Case D above show the response of the system after
            experiencing a minor impulse from the motor. The results show
            that the impulse causes a small linear region in the angular
            velocity of the platform, but otherwise has minor effects except
            to get the ball rolling. All plots show the opposite results of 
            Case C and B because the motor torque causes a negative platform
            angle and thus the ball rolls in the opposite direction.

@image      html CL_Image.png width=1000px

@details    The plots above show the response of the system in closed loop. 
            Gains were applied based on the lab handout, but the response
            shows that ultimately the platform is able to balance the ball
            when it has been offset by 5 cm. With the improvement of the
            controller the system should be able to balance the ball without
            so much oscillation, because ultimately at larger initial offsets
            that motion could be harmful to the system.
'''