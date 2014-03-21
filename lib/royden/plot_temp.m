clf reset;
%clear all;

[slab_x,slab_y]=textread('interplatetopo','%n%n');

%M=dlmread('temperature_mat',' ');
xm=reshape(M(:,1),76,251);
ym=reshape(M(:,2),76,251);
tempm=reshape(M(:,3),76,251);

imagesc(xm(1,:)/1000,ym(:,1)/1000,tempm,[0,2000]), colorbar('h')
xlabel('distance  [km]')
ylabel('depth [km]')
hold on 
plot(slab_x,-slab_y,'k')
axis image
xlim([0,300])
title(['Using a=',num2str(a*(1000*365*24*3600)),'mm/y e=',num2str(e*(1000*365*24*3600)),'mm/y v=',num2str(v*(1000*365*24*3600)),' mm/y qfric=',num2str(qfric), ' mW/m^2'])
% title(['Using a=',num2str(a*(1000*365*24*3600)),'mm/y e=',num2str(e*(1000*365*24*3600)),'mm/y v=',num2str(v*(1000*365*24*3600)),' mm/y v2=',num2str(v2*(1000*365*24*3600)),' mm/y qfric=',num2str(qfric), ' mW/m^2'])
%ylim([0,150])

