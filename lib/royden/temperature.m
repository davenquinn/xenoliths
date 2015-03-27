 %
%     The Steady State Thermal Structure of Eroding
%     Orogenic Belts and Accretionary Prisms
%     L. H. Royden, jgr, 1993.
%

%Needs input-file interplatetopo that has two columns, first is
%horizontal distance in kilometers, second is vertical distance
%in kilometers
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%	parameters
%
%           depth: z
%           distance along the surface: x

%	temperature at the base of the lithosphere (degrees C)
	Tm=1250;
%   thickness of the lithosphere
	l=125e3;
%   radiogenic heat production  (W/m3)
    Al=1e-6;       %lower plate
	Au=1e-6;        %upper plate
%   heat conductivity in each plate  (W/m.K)
    Kl=2.5;       %lower plate
	Ku=2.5;       %upper plate
%   depth to the base of the radiogenic layer (m)
    zr=15e3;
%   rate of accretion (m/s)
    a=1*1e-3/(365*24*3600);
%   rate of erosion (m/s)
    e=3*1e-3/(365*24*3600);
%   rate of under thrusting (m/s)
    v=20.*1e-3/(365*24*3600);
%   thermal diffusivity  (m2/s)
    alpha=1e-6;
%   heat flow due to friction on fault (tau*v) (W/m2)
    qfric=15.*1e-3;
%   dip angle of fault (degrees)
    phi=10;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
t1=clock;
tc1=cputime;
[xinter,yinter]=textread('interplatetopo','%n%n');

xinter=xinter*1e3;               %now xinter is in meters
yinter=-yinter*1e3;             %now yinter is in meters
%v2=(a-e)/tan(2*pi*phi/360); !!MAKE SURE THIS EQ IS CORRECT

%initializing:
M=zeros(251*76,3);
prog=0;
for i=-100:150
  %-------printing out progress report..-------
  progn=round((i+100)*100/length(-100:150));
  if(progn~=prog)
    if(mod(progn,5)==1)
      disp(['Progress: ',num2str(prog),' %'])
    end
  end
  prog=progn;
  %-----------------------------
  x=i*2e3;
  if(x<=0)
    h=0;
  else
%    dip angle (o)
%    teta=15.*pi/180;
%    h=x*tan(teta);
    for k=1:length(xinter)-1
      if((xinter(k)<=x) && (x <= xinter(k+1)))
	igood=k;
      end
    end
    if(xinter(length(xinter))<x)
      igood=length(xinter)-1;
    end
    %    disp(['igood = ',num2str(igood)]);
    h=yinter(igood)+(x-xinter(igood))*(yinter(igood+1)-yinter(igood))/(xinter(igood+1)-xinter(igood));
    if(h<0)
      h=-h;
    end

  end
  for j=0:75
    if(x>0)
%      disp([num2str(x/1000),' ',num2str(-h/1000),' ',num2str(j)])
    end
    z=j*2e3;
    roy=real(royden(x,z-h,h,Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric));
    %royden=igood;
    M((i+100)*76+j+1,:)=[x,z,roy];
  end
end
t2=clock;
disp(['Calculation took ',num2str(etime(t2,t1)),' sec'])
%writing to file
dlmwrite('temperature_mat',M,' ')
t3=clock;
tc2=cputime;
disp(['Writing took ',num2str(etime(t3,t2)),' sec'])
disp(['Total cpu-time ',num2str(tc2-tc1),' sec'])
