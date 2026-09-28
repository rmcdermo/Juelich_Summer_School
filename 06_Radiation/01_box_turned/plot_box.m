Exact_Phi = csvread('exact_f.csv',1,0);
Exact_F = Exact_Phi;
xyz = Exact_F(:,1);
%
M = csvread('radiation_box__50__100_devc.csv',2,0);
M_x = M(2,2:21);
M = csvread('radiation_box__50__100_y_devc.csv',2,0);
M_y = M(2,22:41);
M = csvread('radiation_box__50__100_z_devc.csv',2,0);
M_z = M(2,42:61);
h = plot(xyz,Exact_F(:,2),'ko',...
    xyz,M_x,'k-',xyz,M_y,'r.',xyz,M_z,'-.');
set(h(3),'LineWidth',2)
legend('Exact','X','Y','Z','location','south')
