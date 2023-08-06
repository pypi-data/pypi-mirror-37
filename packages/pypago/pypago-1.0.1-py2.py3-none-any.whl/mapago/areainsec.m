function [areavect] = areainsec(veci, vecj, faces, areaW, areaN)
%AREAINSEC
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also FACESINSEC, LENGTHINSEC
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

[a, ~, ~] = size(areaN);
areavect = zeros(a, length(veci));

for l=1:length(veci)
    switch faces(l)
        case 'N'
            areavect(:, l) = squeeze(areaN(:, vecj(l), veci(l)));
        case 'W'
            areavect(:, l) = squeeze(areaW(:, vecj(l), veci(l)));
    end
end
