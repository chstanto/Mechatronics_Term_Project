% ME 405 : Lab 09
% Author : Cole Stanton
% Date : 3/12/21

clc;
clear;
close all;

%% Platform Matrices
% Reduce fourth order system from lab 6 to second order
A_2 = [-3.0672 , 51.8396
    1 , 0];
B_2 = [-562.3217
    0];
C_2 = eye(2);
D_2 = [0;0];

%% Calculate Gains
% Select desired percent overshoot and settling time
OS_2 = 0.075;
T_s_2 = 0.25;

% Calculate constants based on selected overshoot and settling time
zeta_2 = -log(OS_2)/sqrt(pi^2+log(OS_2)^2);
wn_2 = 4/zeta_2/T_s_2;

% Calculate desired pole locations
Re_2 = zeta_2*wn_2;
Im_2 = wn_2*sqrt(1-zeta_2^2);
poles_2 = [-Re_2 + Im_2*i ; -Re_2 - Im_2*i];

% Use place function to find corresponding gains
K_2 = place(A_2 , B_2 , poles_2)

%% Simulate System with Calculated Gains
% Adjust A matrix for gains
A_gain_2 = A_2 - B_2*K_2;

% Define variables needed when using state space function
states = {'theta_y_dot (rad/s)' 'theta_y (rad)'};
inputs = {'T_x (Nm)'};

% Define state space model with existing variables
state_space_2 = ss(A_gain_2 , B_2 , C_2 , D_2 , 'statename' , states , 'inputname' , inputs , 'outputname' , states);

% Simulate system response to 15 degree offset
x_0_2 = [0 , deg2rad(15)];
sim_time_2 = 2;
figure(1);
initial(state_space_2 , x_0_2 , sim_time_2);

%% Platform + Ball Matrices
% Matrices representing ball and platform system
A = [0,0.0552097702890155,-1.62482353960573,6.07402991011214
    0,-3.06720946050086,90.2679744225403,51.8396081683732
    1,0,0,0
    0,1,0,0];
B = [10.1217912196528
    -562.321734425158
    0
    0];
C = eye(4);
D = [0;0;0;0];

%% Calculate Gains
% Select desired percent overshoot and settling time
OS = 0.075;
T_s = 3;

% Calculate constants based on selected overshoot and settling time
zeta = -log(OS)/sqrt(pi^2+log(OS)^2);
wn = 4/zeta/T_s;

% Calculate desired pole locations
Re = zeta*wn;
Im = wn*sqrt(1-zeta^2);
poles = [-Re + Im*i ; -Re - Im*i
    -10*Re + Im*i ; -10*Re - Im*i];

% Use place function to find corresponding gains
K = place(A , B , poles)

%% Simulate System with Calculated Gains
% Adjust A matrix for gains
A_gain = A - B*K;

states = {'x_dot (m/s)' 'theta_y_dot (rad/s)' 'x (m)' 'theta_y (rad)'};
inputs = {'T_x (Nm)'};

% Define state space model with existing variables
state_space = ss(A_gain , B , C , D , 'statename' , states , 'inputname' , inputs , 'outputname' , states);

% Simulate system response to 15 degree offset
x_0 = [0 , 0 , 0 , deg2rad(15)];
sim_time = 5;
figure(2);
initial(state_space , x_0 , sim_time);
