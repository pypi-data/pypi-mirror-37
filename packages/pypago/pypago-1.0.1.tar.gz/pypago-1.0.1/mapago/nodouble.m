function [newvecj, newveci] = nodouble(veci, vecj)
%NODOUBLE
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also NODOUBLE_TSR, NODOUBLE_V
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO


% JD PAGO WHOI

newveci(1) = veci(1);
newvecj(1) = vecj(1);
for l=2:length(veci)
    if ~(veci(l) == veci(l - 1) && vecj(l) == vecj(l - 1))
        newveci = [newveci, veci(l)];
        newvecj = [newvecj, vecj(l)];
    end
end
