function [class] = whichclass(data, vec)
%WHICHCLASS
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also INDICES_MODEL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

edges = zeros(1, length(vec) + 1);
edges(1) = vec(1) - (.5 * (vec(2)) - vec(1));
for l=2:length(vec)
    edges(l) = 0.5 * (vec(l) + vec(l - 1));
end
edges(end) = vec(end) + .5 * (vec(end) - vec(end - 1));

if ~isnan(data)
    if vec(2) > vec(1)
        l = 2;
        while (l <= length(edges)) && (data > edges(l));
            l = l + 1;
        end
        class = l - 1;
    else % assuming that vec(2) < vec(1)
        l = 2;
        while (l <= length(edges)) && (data < edges(l));
            l = l + 1;
            class = l - 1;
        end
    end
else
    class = NaN;
end
