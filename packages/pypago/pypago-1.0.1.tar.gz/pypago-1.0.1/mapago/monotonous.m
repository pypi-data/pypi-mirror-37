function [res] = monotonous(vect)
%MONOTONOUS checks if vector is monotonic (gives 1) or not (gives 0)
%
% DESCRIPTION
% MONOTONOUS checks if vector is monotonic (gives 1) or not (gives 0)
%
% EXAMPLES
%
%   See also FACESINSEC
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

if ndims(vect) == 2 & min(size(vect)) == 1
    vect = vect(find(~isnan(vect)));
    temp = diff(vect);
    temp = temp(find(abs(temp) > 1e-3));
    temp = sum(diff(sign(temp)));
    if temp == 0
        res = 1;
    else
        res = 0;
    end
else
    error('JD:"misuse of function monotonous: vector must be 1D"')
end
