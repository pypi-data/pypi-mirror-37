function [tt] = inputaxis(ax)
%INPUTAXIS
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also INPUTCAXIS
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO
%

% JD PAGO WHOI
ans = JDinputbin('change axis ? (0 or 1) ');
tt = axis(ax);
if ans
    disp(['current axis: [ ' num2str(tt) ' ]'])
    while ans
        tt = str2num(JDinputbin('new axis: ', 's'));
        axis(ax, tt)
        ans = JDinputbin('change axis ? (0 or 1) ');
    end
end
