EXPCSV = csvread('tga_example_data.csv',2,0);
FDSCSV = csvread('tga_example_tga.csv',2,0);
%
figure(1)
h=plot(EXPCSV(:,2),EXPCSV(:,3),FDSCSV(:,2),FDSCSV(:,3),'--');
axis([200 500 0 1])
xlabel('T (C)');ylabel('Y');title('TGA')
%figformat(h,gca,gcf,'T (C)','Y','TGA COMPARISON',0.9,14,2);
legend('Exp','FDS')
%figsaver('Y_comparison');
%
figure(2)
h=plot(EXPCSV(:,2),EXPCSV(:,4),FDSCSV(:,2),FDSCSV(:,4),'--');
axis([200 500 0 0.003])
xlabel('T (C)');ylabel('-dY/dT');title('DTG');
%figformat(h,gca,gcf,'T (C)','-dY/dT','TGA COMPARISON',0.9,14,2);
legend('Exp','FDS')
%figsaver('dYdT_comparison')
%

