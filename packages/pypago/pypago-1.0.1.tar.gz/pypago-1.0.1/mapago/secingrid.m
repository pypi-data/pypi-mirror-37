function [vecj, veci] = secingrid(fromi, fromj, toi, toj)
%SECINGRID calculates the sequence of gridpoints
%
% DESCRIPTION
%
% calculates the sequence of gridpoints to go from (fromj, fromi) to
% (toj, toi), by following the straight line that joins the two end points.
% adjacent grid points have one side in common.
%
% EXAMPLES
%
%   See also LOCINGRID
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

if (toi - fromi) == 0
    vecj = [fromj:1 * sign(toj - fromj):toj];
    veci = fromi * ones(1, length(vecj));
else

    if (toj - fromj) == 0
        veci = [fromi:1 * sign(toi - fromi):toi];
        vecj = fromj * ones(1, length(veci));
    else
        veci = [fromi];
        vecj = [fromj];
        a = (toj - fromj)/(toi - fromi);
        b = toj - toi * a;

        while ~((veci(end) == toi) & (vecj(end) == toj))

            newi = veci(end) + 1 * sign(toi - fromi);
            newj = vecj(end) + 1 * sign(toj - fromj);

            y = a * newi + b;
            x = (newj - b)/a;

            if abs(x - veci(end)) >= abs(y - vecj(end))
                veci = [veci newi];
                vecj = [vecj vecj(end)];
            else
                veci = [veci veci(end)];
                vecj = [vecj newj];
            end

        end

    end
end
