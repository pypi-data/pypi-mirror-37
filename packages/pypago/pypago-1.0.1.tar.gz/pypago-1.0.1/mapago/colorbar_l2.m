function [] = colorbar_l2(hc, dir, vect)
%COLORBAR_L2 plot colorbar l2
%
% DESCRIPTION
% colorbar_l2 plot colorbar l2
%
% EXAMPLES
%
%   colorbar_l2(hc, dir, vect);
%
%   See also COLORBAR_L1
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

axes(hc)
hold on
for lev=1:length(vect)
    if strcmp(dir, 'ver')
        plot([-1 2], [vect(lev) vect(lev)], 'k', 'linewidth', 2)
    end
    if strcmp(dir, 'hor')
        plot([vect(lev) vect(lev)], [-1 2], 'k', 'linewidth', 2)
    end
end
set(hc, 'TickLength', [0 0])
