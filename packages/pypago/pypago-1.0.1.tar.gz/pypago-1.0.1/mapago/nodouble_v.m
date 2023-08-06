function [newvecv] = nodouble_v(veci, vecj, vecv)
%NODOUBLE_V
%
% DESCRIPTION
%
% warning: relies on the assumption that all sections go from west to east
%
% EXAMPLES
%
%   See also NODOUBLE, NODOUBLE_TSR
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

newvecv(1) = vecv(1);
for l=2:length(veci)
    if ~(veci(l) == veci(l - 1) && vecj(l) == vecj(l - 1))
        newvecv = [newvecv, vecv(l)];
    else
        temp = atan(vecv(l)/-vecv(l - 1));
        if -vecv(l - 1) < 0
            if vecv(l) >= 0
                temp = temp + pi;
            else
                temp = temp-pi;
            end
        end
        if (temp > pi/4) || (temp < ((-3/4) * pi))
            signe = +1;
        else
            signe = -1;
        end
        newvecv(end) = signe * sqrt(vecv(l - 1)*vecv(l - 1) + vecv(l)*vecv(l));
    end
end
