function [newvectsr] = nodouble_tsr(veci, vecj, vectsr)
%NODOUBLE_TSR
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also NODOUBLE, NODOUBLE_V
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

newvectsr(1) = vectsr(1);
for l=2:length(veci)
    if ~(veci(l) == veci(l - 1) && vecj(l) == vecj(l - 1))
        newvectsr = [newvectsr, vectsr(l)];
    end
end
