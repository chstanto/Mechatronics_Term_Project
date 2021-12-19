% ME 405 : Lab 06
% Author : Cole Stanton
% Date : 2/24/21

clc;
clear;
close all;

%% Define all numerical parameters according to lab handout
rm = 60/1000;            %m
lr = 50/1000;            %m
rb = 10.5/1000;          %m
rg = 42/1000;            %m
lp = 110/1000;           %m
rp = 32.5/1000;          %m
rc = 50/1000;            %m
mb = 30/1000;            %kg
mp = 400/1000;           %kg
Ip = (1.88e6)/1000^3;    %kg*m^2
Ib = (2*mb*rb^2)/5;      %kg*m^2
b  = 10/1000;            %Nm*s/rad
g  = 9.81;               %m/s^2

%% Linearize existing matrices
% Define symbolic variables needed for matrices
syms x x_d x_dd theta_y theta_y_d theta_y_dd T_x;

% Define M matrix
M = [-(mb*rb^2+mb*rc*rb+Ib)/rb , -(Ib*rb+Ip*rb+mb*rb^3+mb*rb*rc^2+2*mb*rb^2+mp*rb*rg^2+mb*rb*x^2)/rb
    -(mb*rb^2+Ib)/rb , -(mb*rb^3+mb*rb*rb^2+Ib*rb)/rb];

% Define f matrix
f = [b*theta_y_d - g*mb*(sin(theta_y)*(rb+rc)+x*cos(theta_y))+T_x*lp/rm+2*mb*theta_y_d*x*x_d-g*mp*rg*sin(theta_y)
    -mb*rb*x*theta_y_d^2-g*mb*rb*sin(theta_y)];

% Define state space vector, X
X = [x_d; theta_y_d; x; theta_y];

% Define g matrix using state space, M, and f
g = [inv(M)*f
    X(1:2,1)];

% Define jacobian matrices
Jx = [diff(g(1),X(1)) , diff(g(1),X(2)) , diff(g(1),X(3)) , diff(g(1),X(4))
      diff(g(2),X(1)) , diff(g(2),X(2)) , diff(g(2),X(3)) , diff(g(2),X(4))
      diff(g(3),X(1)) , diff(g(3),X(2)) , diff(g(3),X(3)) , diff(g(3),X(4))
      diff(g(4),X(1)) , diff(g(4),X(2)) , diff(g(4),X(3)) , diff(g(4),X(4))];

Ju = [diff(g(1),T_x)
      diff(g(2),T_x)
      diff(g(3),T_x)
      diff(g(4),T_x)];

% Define equilibrium values
eqbm_vars = [x_d , theta_y_d , x , theta_y , T_x];
eqbm_vals = [0 , 0 , 0 , 0 , 0];

% Replace varaibles in Jacobian matrices with values
Jx = subs(Jx , eqbm_vars , eqbm_vals);
Ju = subs(Ju , eqbm_vars , eqbm_vals);

% Double the precision of both Jacobian matrices
A = double(Jx);
B = double(Ju);

% Define C and D matrices for state space model
C = eye(4);
D = [0;0;0;0];

%% Case A simulation
% Define variables needed when using state space function
states = {'x_dot (m/s)' 'theta_y_dot (rad/s)' 'x (m)' 'theta_y (rad)'};
inputs = {'T_x (Nm)'};

% Define state space model with existing variables
state_space = ss(A , B , C , D , 'statename' , states , 'inputname' , inputs , 'outputname' , states);

% Open new figure for Case A plot
figure(1);

% Plot response of system based on initial conditions
t_s = 1;
X0 = [0 , 0 , 0 , 0];
initial(state_space , X0 , t_s);
title('Case A Simulation Results');

%% Case B simulation
% Open new figure for Case B plot
figure(2);

% Plot response of system based on initial conditions
t_s = 0.4;
X0 = [0 , 0 , 0.05 , 0];
initial(state_space , X0 , t_s);
title('Case B Simulation Results - 5 cm Ball Offset');

%% Case C simulation
% Open new figure for Case C plot
figure(3);

% Plot response of system based on initial conditions
t_s = 0.4;
X0 = [0 , 0 , 0 , deg2rad(5)];
initial(state_space , X0 , t_s);
title('Case C Simulation Results - 5 deg Platform Angle');

%% Case D Simulation
% Open new figure for Case D plot
figure(4);

% Define initial conditions and impulse
t_s = [0:0.001:0.4];
X0 = [0 , 0 , 0 , 0];
T_x = [[1/1000]*ones(1,5) , zeros(1 , length(t_s)-5)];

% Simulate effect of impulse on defines state space model
response = lsim(state_space , T_x , t_s , X0);

% Plot data in 4 subplots
subplot(4,1,1);
plot(t_s , response(: , 1));
title('Case D Simulation Results - Motor Impulse');
ylabel('Velocity, x_d (m/s)');
xlabel('Time, t (s)');

subplot(4,1,2);
plot(t_s , response(: , 2));
ylabel('Angular Velocity, Theta_y_d (rad/s)');
xlabel('Time, t (s)');

subplot(4,1,3);
plot(t_s , response(: , 3));
ylabel('Position, x (m)');
xlabel('Time, t (s)');

subplot(4,1,4);
plot(t_s , response(: , 4));
ylabel('Angular Position, Theta_y (rad/s)');
xlabel('Time, t (s)');

%% Simulate Closed Loop System with Provided Gains
figure(5);
X0 = [0 , 0 , 0.05 , 0];
t_s = 20;

% Define gain values from lab handout
k = [-0.05 , -0.02 , -0.3 , -0.2];

% Find A to reflect closed loop gains
A_cl = A-B*k;

cl_state_space = ss(A_cl , B , C , D , 'statename' , states , 'inputname' , inputs , 'outputname' , states);

t_s = [0:0.01:20];
u = zeros(1 , length(t_s));
lsim(cl_state_space , u , t_s , X0)
title('Closed Loop Simulation - 5 cm Ball Offset');



