function [] = colorbar_l1(hc, dir, vect)
%COLORBAR_L1 plot colorbar l1
%
% DESCRIPTION
% plot colorbar l1
%
% EXAMPLES
%
%    colorbar_l1(hc, dir, vect)
%
%   See also COLORBAR_L2
%
%MAPAGO Toolbox
%Copyright 2012-2015, CNRS TODO

axes(hc)
hold on
for lev=1:length(vect)
    if strcmp(dir, 'ver')
        plot([-1 2], [vect(lev) vect(lev)], 'k', 'linewidth', 1)
    end
    if strcmp(dir, 'hor')
        plot([vect(lev) vect(lev)], [-1 2], 'k', 'linewidth', 1)
    end
end
set(hc, 'TickLength', [0 0])

step_tick = 1;
while length(vect(1:step_tick:end))>6
    step_tick = step_tick * 2;
end

if strcmp(dir, 'ver')
    set(hc, 'YTick', vect(1:step_tick:end))
end
if strcmp(dir, 'hor')
    set(hc, 'XTick', vect(1:step_tick:end))
end
