T = readdata('80-62-6-IR.jdx',37);
Tmp1 = mean(T(:,2:5),2);
nu = T(:,1);
Tmp2 = 1E6./(nu*100); % micron
N = length(nu);
clear Tmean lambda P
for i = 1:N
    Tmean(i) = Tmp1(N-i+1);
    lambda(i) = Tmp2(N-i+1);
end
Tmean = Tmean';
lambda = lambda';
P = planck(lambda,1200);
P_int = trapz(lambda,P);
%
Len = 0.0000945;% works for 1000 K and 2000 1/m
Len = 0.000175; % 1000 K and 
kappa = -log(Tmean)/Len;
kappa_mean=trapz(lambda,P.*kappa)/P_int
%
P_inf = planck(lambda,800);
P_inf_int = trapz(lambda,P_inf);
x = [0:0.0001:0.001 0.002:0.001:0.02];
P(:,1) = P_inf*0;
P_int(1) = 0;
for i = 2:length(x)
    P(:,i) = P_inf.*(1-exp(-kappa*x(i)));
    P_int(i) = trapz(lambda,P(:,i));
end
P_int = P_int/P_inf_int;
% figure 1
figure(1)
subplot(2,1,1)
h=plot(lambda,kappa);
ylabel('\kappa (1/m)')
title('MMA monomer')
set(gca,'XTick',[])
set(h,'Linewidth',1.3)
set(gca,'FontSize',12)
subplot(2,1,2)
%h=plot(lambda,P_inf,lambda,P(:,[11 110]));
h=plot(lambda,P_inf,lambda,P(:,[11 21]));
ylabel('h(\lambda) (W sr^{-1} \mum^{-1} m^{-2})')
xlabel('\lambda (\mu m)')
set(gca,'Position',[0.1300    0.1100    0.7750    0.4743])
legend('Planck','x = 10 mm','x = 20 mm')
set(h,'Linewidth',1.3)
set(gca,'FontSize',12)
% figure 2
figure(2)
h = semilogy(x,P_int,'-',x,(1-exp(-960*x)),x,(1-exp(-100*x)));
axis([0 0.02 0.01 1])
grid on
figformat(h,gca,gcf,'x (m)','I(\lambda)/I_b(\lambda) (-)','Emission',0.9,14,1.5)
legend('Spectral','1-exp(-960 x)','1-exp(-100 x)')