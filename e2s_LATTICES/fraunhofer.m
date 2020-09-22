%------------------------------------------------------------------------
%-----Fraunhofer diffraction from a rectangular aperture-----------------
%------------------------------------------------------------------------

clc
close all
clear all

%------------------------------------------------------------------------

lambda=500e-9; k=(2*pi)/lambda; % wavelength of light in vaccuum
a=200e-6; b=200e-6; % dimensions of diffracting rectangular aperture
                % a is along Z and b is along Y
Io=400.0; % relative intensity
R=1.5; % distance of screen from aperture
Y=(-0.025:1e-5:0.025); Z=Y ; % coordinates of screen

beta=k*b*Y/(2*R*pi);alpha=k*a*Z./(2*R*pi); % intermediate variable

 % diffracted intensity

for i=1:length(Y)
    for j=1:length(Z)
I(i,j)=Io.*((sinc(alpha(j)).^2).*(sinc(beta(i))).^2);
    end
end

%------------------------------------------------------------------------
 RI=imref2d(size(I));
 RI.XWorldLimits = [min(Y) max(Y)];
 RI.YWorldLimits = [min(Z) max(Z)];
 

 figure(1)
 imshow(I,RI,[min(min(I)) max(max(I))]);
 colormap(jet)
 colorbar
 title('Fraunhofer Diffraction','fontsize',14)
 %fh = figure(1);
 %set(fh, 'color', 'white'); 


