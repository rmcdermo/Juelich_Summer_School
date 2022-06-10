% Example 7: Sphere burner
% Showcase Spectral Analysis on time series from device sensing devc_val 
% (spatial volume integral).
%
% Use device data to infer puffing frequency for this problem.
%
% To translate to Python we need:
% 1. CSV reader.
% 2. Spline interpolation routine to get data for constant dt.
% 3. FFT routine.
% 4. Plotting routine.
% -------------------------------------------------------------------------
close all
clear all
clc

basedir  ='./';
casename ='Example_7';

% Import device file and define time and devc_valmf arrays:
[RES]=importdata([basedir casename '_devc.csv'],',',2);

time   =RES.data(:,1);

% Variable to test:
devc_val   =RES.data(:,3); % Soot mass on device.

% Interpolate to constant dt signal -> for Spectral Analysis:
tmin  =  2.3;                                % Discard HRR ramp phase.
tmax  =  max(time);
dt_fix=  1/100; 
nt    =  floor((tmax-tmin)/dt_fix)+1;
time_new  =linspace(tmin,tmax,nt);
devc_val_new=spline(time,devc_val,time_new); % Spline interpolation.

% Plot Signal:
figure
hold on
plot(time,devc_val)
plot(time_new,devc_val_new,'r')
xlabel('t [sec]','FontSize',16)
ylabel('DEVC var','FontSize',16)
set(gca,'FontSize',14)
box on

% Power Spectral Density, frequency:
devc_val_new = (devc_val_new-mean(devc_val_new));
devc_val_new = devc_val_new/max(abs(devc_val_new)); % Normalize.
S   = fft(devc_val_new,nt); % Signal in freq. domain.
PS  = S.*conj(S)/nt;                                % norm - PSD
nt2 = floor(nt/2);                         
f   = 1/dt_fix*1/nt*[0:nt2];                        % Frequencies Hz. 

% Plot PSD:
figure
hold on
plot(f(1:50),PS(1:50))
xlabel('f [Hz]','FontSize',16)
ylabel('PSD DEVC var','FontSize',16)
set(gca,'FontSize',14)
box on

[val,loc]=max(PS(1:end));
disp(['Freq with max(PSD)=' num2str(f(loc)) ' Hz'])
