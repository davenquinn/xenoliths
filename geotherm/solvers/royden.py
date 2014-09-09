"""
Solver for steady-state forearc geotherm above a subducting slab.

Translated from Matlab by Daven Quinn
"""

function royden=royden(x,z,h,Tm,l,Al,Au,Kl,Ku,zr,a,e,v,alpha,qfric)
warning off MATLAB:divideByZero
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%	parameters
%
%   depth: z
%   distance along the surface: x
%	Tm ... temperature at the base of the lithosphere (degrees C)
%   l  ... thickness of the lithosphere
%   Al ... heat production in the lower plate (W/m3)
%   Au ... heat production in the upper plate (
%   Kl ... heat conductivity in the lower plate  (W/m.K)
%   Ku ... heat conductivity in the upper plate  (W/m.K)
%   zr ... depth to the base of the radiogenic layer (m)
%   a  ... rate of accretion (m/s)
%   e  ... rate of erosion (m/s)
%   v  ... rate of under thrusting (m/s) relative to (x,z)=(0,0) (m/s)
%   alpha ... thermal diffusivity  (m2/s)
%   qfric ... heat flow do to friction on fault (tau*v) (mW/m2)
    To=Tm+Al*zr*(2*l-zr)/(Kl*2);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%	calculate the temperature in the foreland (x<0)
%disp(['Starting with x=',num2str(x)])
if (x<=0)
  Tl=(To*z)/l-(Al*z^2)/(Kl*2);
  if(z>=zr)
    Tl=Tl+(Al*(z-zr)^2)/(Kl*2);
  end
  royden=Tl;
else
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %	calculate the temperature for (x>0)
  %
  if(a<e)
    d=complex(0.,e*sqrt(h)/sqrt(2*alpha*(e-a)));
    b=complex(0.,a*sqrt(h)/sqrt(2*alpha*(e-a)));
  else
    d=complex(e*sqrt(h)/sqrt(2*alpha*(a-e)),0.);
    b=complex(a*sqrt(h)/sqrt(2*alpha*(a-e)),0.);
  end
  g=h*sqrt(v)/(2*sqrt(alpha*x));
  gg=3*pi*g/8.;
  bb=b/2.;
  yr2=zr*g/h+bb*(b-d)/g;
  %
  b1=d*ierfc1(b)-b*ierfc1(d);
  b2=(Ku/Kl)*(b-d)*(-d*erfc1(b)-ierfc1(d));
  b3=ierfc1(b*(b-d)/g);
  b4=bb*(b-d)/g^2;
  b5=-g*erfc1(b*(b-d)/g);
  b6=1+qfric*l/(Kl*To);
  Bl=(b4*b2-b1*b6)/(b1*b5-b2*b3);
  Bu=(b4*b5-b3*b6)/(b1*b5-b2*b3);
  %
  c1=(Au/Ku)*(d^2-b^2)/(((b-d)^2)*(1+2*d^2));
  c2=(Au/Ku)*(i2erfc1(b)-((1+2*b^2)/(1+2*d^2))*i2erfc1(d));
  c3=(Au/Kl)*(-2*b)/((b-d)*(1+2*d^2));
  c4=(Au/Kl)*(b-d)*(-ierfc1(b)-(4*b/(1+2*d^2))*i2erfc1(d));
  c5=-(Al/Kl)*(bb^2*(b-d)^2)/g^4;
  c6=(Al/Kl)*i2erfc1(b*(b-d)/gg);
  c7=-(Al/Kl)*(2*bb*(b-d))/g^2;
  c8=-(Al/Kl)*(gg*ierfc1(b*(b-d)/gg));
  Cl=(c2*c7-c2*c3-c4*c5+c4*c1)/(c4*c6-c2*c8);
  Cu=(c1*c8-c5*c8-c3*c6+c7*c6)/(c4*c6-c2*c8);
  %
  %
  yl=(z/h)*g+b*(b-d)/g;
  yl1=(z/h)*gg+b*(b-d)/gg;
  yl2=(z/h)*g+bb*(b-d)/g;
  yu=(z/h)*(b-d)+b;
  %
  Tl=(h/l)*((yl2/g)+Bl*ierfc1(yl))+(Al*h^2/(Kl*To*2))*(Cl*i2erfc1(yl1)-(yl2/g)^2);
  if(real(yl2)>real(yr2))
    Tl=Tl+(Al*h^2/(Kl*To*2))*((yl2-yr2)/g)^2;
  end
  Tl=Tl*To;
  Tu=(h/l)*Bu*(d*ierfc1(yu)-yu*ierfc1(d))+ ...
     (Au*h^2/(Ku*To*2))*((d^2-yu^2)/((b-d)^2*(2*d^2+1))+ ...
     Cu*(i2erfc1(yu)-((2*yu^2+1)/(2*d^2+1))*i2erfc1(d)));
  Tu=Tu*To;
  if(z<0)
    royden=Tu;
  else
    royden=Tl;
  end
end

%end function royden
%---------------------------------------------
function i2erfc1=i2erfc1(x)

      i2erfc1=(0.25+0.5*x^2)*erfc1(x)-x*exp(-x^2)/(2*sqrt(pi));
%---------------------------------------------
function ierfc1=ierfc1(x)

ierfc1 = -x*erfc1(x)+exp(-x^2)/sqrt(pi);
%---------------------------------------------
function erfc1=erfc1(x)

erfc1=1-erf1(x);
%---------------------------------------------
function erf1=erf1(x)

if (imag(x)~=0)
  erf1=complex(0,2*dawson(imag(x))/(sqrt(pi)*exp(-imag(x)^2)));
else
  if(real(x)<0)
    erf1=complex(-gammp(0.5,x^2),0);
  else
    erf1=complex(gammp(0.5,x^2),0);
  end
end
%---------------------------------------------
function dawson=dawson(x)

NMAX=6;
H=0.4;
A1=2./3.;
A2=0.4;
A3=2./7.;

i=linspace(1,NMAX,NMAX);
c=exp(-((2*i-1)*H).^2);

if(abs(x)<0.2)
  x2=x^2;
  dawson=x*(1.-A1*x2*(1.-A2*x2*(1.-A3*x2)));
else
  xx=abs(x);
  n0=2*round(0.5*xx/H);
  xp=xx-n0*H;
  e1=exp(2.*xp*H);
  e2=e1^2;
  d1=n0+1;
  d2=d1-2.;
  sum=0.;
  for i=1:NMAX
    sum=sum+c(i)*(e1/d1+1./(d2*e1));
    d1=d1+2.;
    d2=d2-2.;
    e1=e2*e1;
  end
  dawson=0.5641895835*abs(exp(-xp^2))*sign(x)*sum;
end
%---------------------------------------------
function gammp=gammp(a,x)
if ((x<0) || (a<=0))
  error('MATLAB:gammap','bad arguments in gammp')
end
if (x<(a+1))
 ITMAX=200;
 EPS=3.e-7;
 gln=gammln(a);
 if(x<=0)
   if(x<0.)
     error('MATLAB:gammap','x < 0 in gser');
   else
     gamser=0;
   end
 else
   ap=a;
   sum=1./a;
   del=sum;
   for n=1:ITMAX
     ap=ap+1;
     del=del*x/ap;
     sum=sum+del;
     if(abs(del)<(abs(sum)*EPS))
       break;
     end
   end
   if(n==ITMAX)
     error('MATLAB:gammap','a too large, ITMAX too small in gser');
   end
   gamser=sum*exp(-x+a*log(x)-gln);
   %return gamser
 end
 gammp=gamser;
else
  % call gcf(gammcf,a,x,gln)
  ITMAX=200;
  EPS=3.e-7;
  FPMIN=1.e-30;
  gln=gammln(a);
  b=x+1.-a;
  c=1./FPMIN;
  d=1./b;
  h=d;
  for i=1:ITMAX
    an=-i*(i-a);
    b=b+2.;
    d=an*d+b;
    if(abs(d)<FPMIN)
      d=FPMIN;
    end
    c=b+an/c;
    if(abs(c)<FPMIN)
      c=FPMIN;
    end
    d=1/d;
    del=d*c;
    h=h*del;
    if(abs(del-1)<EPS)
      break;
    end
  end
  if(i==ITMAX)
    error('MATLAB:gammp','a too large, ITMAX too small in gcf')
  end
  gammcf=exp(-x+a*log(x)-gln)*h;
  %return gammcf
  gammp=1.-gammcf;
end
%---------------------------------------------
function gammln=gammln(xx)
cof=[76.18009172947146,-86.50532032941677,24.01409824083091,- ...
     1.231739572450155,.1208650973866179e-2,-.5395239384953e-5];
stp=2.5066282746310005;

      x=xx;
      y=x;
      tmp=x+5.5;
      tmp=(x+0.5)*log(tmp)-tmp;
      ser=1.000000000190015;
      for j=1:6
        y=y+1;
        ser=ser+cof(j)/y;
      end

      gammln=tmp+log(stp*ser/x);
