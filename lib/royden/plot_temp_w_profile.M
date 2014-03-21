clf reset;
close all;
clc;

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

%Profile
start_point_x = 100;
start_point_y = 0;

e = e*(365*24*3600);
a = a*(365*24*3600);

u = -(a-e)/tan(2*pi*phi/360);

dx = u*cosd(phi);
dy = a + u*sind(phi);


x1 = start_point_x;
y1 = start_point_y;

x2 = x1 + dx;
y2 = y1 + dy;
Coef = inv([x1,1;x2,1])*[y1;y2];
Coef_slab = inv([slab_x(1),1;slab_x(2),1])*[-slab_y(1);-slab_y(2)];
x_intersect = (Coef_slab(2) - Coef(2)) / (Coef(1) - Coef_slab(1));
x = [x1:round(x_intersect)];
y = Coef(1)*x + Coef(2);
plot(x,y,'k')

line = zeros(1,length(x));
for n = 1: length(x),
    
    ind_x = min(find(abs(xm(1,:)/1000 - x(n)) <= 1 ));%assumes that the grid size is 2km in x
    ind_y = min(find(abs(ym(:,1)/1000 - y(n)) <= 1 ));%assumes that the grid size is 2km in y
    
    line(n) = tempm(ind_y, ind_x );
end

figure
plot(y/(dy/1e3),line)
xlabel('Time y')
ylabel('Temperature ^\circ C')



