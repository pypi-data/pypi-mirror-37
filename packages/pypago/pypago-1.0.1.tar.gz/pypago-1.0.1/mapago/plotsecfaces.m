function [] = plotsecfaces(veci, vecj, faces, orientation, color)
%PLOTSECFACES
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also SECTIONS_MODEL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

for l=1:length(veci)
    switch faces(l)
        case 'N'
            plot([(veci(l) - .5) (veci(l) + .5)], [(vecj(l) + .5) (vecj(l) + .5)], 'color', color);
            hold on
            switch orientation(l)
                case 1
                    %arrow('Start', [veci(l) vecj(l)+.25], 'Stop', [veci(l) vecj(l)+.75], 'tipangle', 30, 'baseangle', 30, 'length', 10);
                    plot(veci(l), vecj(l) + .75, '.', 'color', color);
                case -1
                    %arrow('Stop', [veci(l) vecj(l) + .25], 'Start', [veci(l) vecj(l) + .75], 'tipangle', 30, 'baseangle', 30, 'length', 10);
                    plot(veci(l), vecj(l) + .25, '.', 'color', color);
            end
        case 'W'
            plot([(veci(l) - .5) (veci(l) - .5)], [(vecj(l) - .5) (vecj(l) + .5)], 'color', color);
            hold on
            switch orientation(l)
                case 1
                    %arrow('Start', [(veci(l) - .75) vecj(l)], 'Stop', [(veci(l) - .25) vecj(l)], 'tipangle', 30, 'baseangle', 30, 'length', 10);
                    plot((veci(l) - .25), vecj(l), '.', 'color', color);
                case -1
                    %arrow('Stop', [(veci(l) - .75) vecj(l)], 'Start', [(veci(l) - .25) vecj(l)], 'tipangle', 30, 'baseangle', 30, 'length', 10);
                    plot((veci(l) - .75), vecj(l), '.', 'color', color);
            end
    end
end
