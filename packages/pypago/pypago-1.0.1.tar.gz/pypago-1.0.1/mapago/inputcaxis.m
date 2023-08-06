function [] = inputcaxis(ax, hc)
%INPUTCAXIS
%
% DESCRIPTION
% INPUTCAXIS
%
% EXAMPLES
%
%   See also INPUTAXIS
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI
ans = JDinputbin('change caxis ? (0 or 1) ');
if ans
    tt = caxis(ax);
    disp(['current caxis: [ ' num2str(tt) ' ]'])
    while ans
        tt = input('new axis: ', 's');
        tempX = get(hc, 'XAxisLocation');
        tempY = get(hc, 'YAxisLocation');
        caxis(ax, str2num(tt))
        set(hc, 'XAxisLocation', tempX);
        set(hc, 'YAxisLocation', tempY);
        ans = JDinputbin('change caxis ? (0 or 1) ');
    end
end
