function [lengthvect] = lengthinsec(veci, vecj, faces, dw, dn)
%LENGTHINSEC
%
% DESCRIPTION
% LENGTHINSEC
%
% EXAMPLES
%
%   See also AREAINSEC, FACESINSEC
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

for l=1:length(veci)
    switch faces(l)
        case 'N'
            lengthvect(l) = squeeze(dn(vecj(l), veci(l)));
        case 'W'
            lengthvect(l) = squeeze(dw(vecj(l), veci(l)));
    end
end
