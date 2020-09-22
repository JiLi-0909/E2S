addpath /home/xph53246/elegant/elegant2matlab/
addpath /home/xph53246/matlabscripts/
addpath /home/xph53246/matlabscripts/general
setpathelegant
 
 
% load data
data = eleload([ 'DTBA_21_5_1.twi']);
 
% get twiss parameters
s = elegetcolumn(data{1},'s');% indexes = [I01,I05,I09,I13,I17,I21];
 
ax = elegetcolumn(data{1},'alphax');
ay = elegetcolumn(data{1},'alphay');
bx = elegetcolumn(data{1},'betax');
by = elegetcolumn(data{1},'betay');
dx = elegetcolumn(data{1},'etax');
dxp = elegetcolumn(data{1},'etaxp');
gx = (1+ax.^2)./bx;
hx = gx.*dx.*dx + 2.*ax.*dx.*dxp + bx.*dxp.*dxp;
psix = elegetcolumn(data{1},'psix');
psiy = elegetcolumn(data{1},'psiy');
 
 
% get global parameters
qx = elegetparam(data{1},'nux');
qy = elegetparam(data{1},'nuy');
chrox = elegetparam(data{1},'dnux/dp');
chroy = elegetparam(data{1},'dnuy/dp');
dQx_dx = elegetparam(data{1},'dnux/dAx');
dQy_dx = elegetparam(data{1},'dnuy/dAx');
dQx_dy = elegetparam(data{1},'dnux/dAy');
dQy_dy = elegetparam(data{1},'dnuy/dAy');
betaxmax = elegetparam(data{1},'betaxMax');
betaymax = elegetparam(data{1},'betayMax');
alphac = elegetparam(data{1},'alphac');
alphac2 = elegetparam(data{1},'alphac2');
sdelta0 = elegetparam(data{1},'Sdelta0');
lossperturn = elegetparam(data{1},'U0');
emittance = elegetparam(data{1},'ex0');
 
sx = sqrt(bx*emittance + (sdelta0*dx).^2);
sy = sqrt(by*emittance*0.003 );
 
 
figure(100); clf
hold on
% plot(s,bx,'-b',s,by,'-r',s,dx*100,'-g');
plot(s,bx,'.-b',s,by,'.-r',s,dx*100,'.-g')