function dist = calc_dist(utmx,utmy)

% Calculate distances of UTM xy points from the MFT.
% Location of MFT is harwired in parameters section.
% 
% Calls utm2ll3.


%%%%%%%%%%%%%%%% PARAMETERS %%%%%%%%%%%%%%%%%
% Two lon-lat points along MFT to define a line
% UTM zone 44 is 78E - 84E
% UTM zone 45 is 84E - 90E
mft_ll1 = [87.90   26.664 45]; % pt1: lon, lat, UTM zone
mft_ll2 = [85.4735 27.160 45]; % pt2: lon, lat, UTM zone
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Convert lon-lat points along MFT to UTM
[mftx(1),mfty(1),i_zone] = utm2ll3(mft_ll1(1),mft_ll1(2),mft_ll1(3),1);
[mftx(2),mfty(2),i_zone] = utm2ll3(mft_ll2(1),mft_ll2(2),mft_ll2(3),1);

x0 = mftx(1); y0 = mfty(1); x1 = mftx(2); y1 = mfty(2);

len = max(size(utmx)); % Number of xy points

% For each pair of xy values, calculate perpendicular distance from MFT line
for i =1:len
  x = utmx(1); y = utmy(i);
  dist(i,1)= ( (y0-y1)*x + (x1-x0)*y + x0*y1 - x1*y0 ) /...
	sqrt((x1-x0)^2 + (y1-y0)^2);
end
% dist is perpendicular distance in meters
