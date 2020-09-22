function Acc_y_vs_beta(gmin)

if nargin<1
    gmin = 4e-3; 
end

by_I21 = linspace(1,8,351); 
by_I22 = linspace(1,8,351);

[X Y] = meshgrid(by_I21, by_I22);


A_I21  = sqrt(X./Y) * gmin/2 * 1e3;

figure(); clf
colormap jet

[C,h] = contourf(X,Y, A_I21*2,2000);
set(h,'LineColor','none')
c = colorbar;

xlabel('\beta_y I21 (m)')
ylabel('\beta_y I22 (m)')

ylabel(c,'g_{min}(I21) (mm)')

title (['g_{min}(I21) for g_{min}(I22)=' num2str(gmin*1e3,2) ' mm'])
caxis([1.414 14.141]) 
end