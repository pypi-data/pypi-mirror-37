function [atracer, zvect, lvect, atracer_pcol, zvect_pcol, lvect_pcol] = preplot(secstruct, secdata)
%PREPLOT
%
% DESCRIPTION
% PREPLOT
%
% EXAMPLES
%
%   See also PREPLOTV, FIGURE_SECTION_1L
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI
nz = length(secstruct.depthvect(:, 1));
nl = length(secstruct.lvect);

for z=1:nz
    atracer(z, :) = nodouble_tsr(secstruct.veci, secstruct.vecj, secdata(z, :));
    zvect(z, :) = nodouble_tsr(secstruct.veci, secstruct.vecj, secstruct.depthvect(z, :));
end
zvect(find(zvect == 0)) = NaN;
zvect = -cumsum(zvect, 1);
lvect = repmat(secstruct.lvect, [nz 1]);

lvect_pcol = [1.5 * lvect(:, 1) - 0.5 * lvect(:, 2), ...
               .5 * (lvect(:, 1:(end - 1)) + lvect(:, 2:end)), ...
              1.5 * lvect(:, end) - 0.5 * lvect(:, (end - 1))];
lvect_pcol = [lvect_pcol(1, :);lvect_pcol];

for l=1:length(secstruct.lvect)
    zl = length(find(~isnan(zvect(:, l))));
    if zl > 1
        zvect_pcol_temp(:, l) = [0;...
                                 .5 * (zvect(1:(zl - 1), l) + zvect(2:zl, l));...
                                 1.5 * zvect(zl, l) - 0.5 * zvect((zl - 1), l);
        zvect(zl + 1:nz, l)];
    else
        zvect_pcol_temp(:, l) = [0;zvect(1, l);zvect(2:nz, l)];
    end
end

zvect_pcol(:, 1) = zvect_pcol_temp(:, 1);
for l=2:length(zvect_pcol_temp(1, :))
    z = 1;
    zmin = min(length(find(~isnan(zvect_pcol_temp(:, l)))), length(find(~isnan(zvect_pcol_temp(:, (l - 1))))));
    zmax = max(length(find(~isnan(zvect_pcol_temp(:, l)))), length(find(~isnan(zvect_pcol_temp(:, (l - 1))))));
    zvect_pcol(1:zmin, l) = .5 * (zvect_pcol_temp(1:zmin, (l - 1)) + zvect_pcol_temp(1:zmin, l));
    for z=zmin + 1:zmax
       if isnan(zvect_pcol_temp(z, l))
           zvect_pcol(z, l) = zvect_pcol_temp(z, (l - 1));
       else
           zvect_pcol(z, l) = zvect_pcol_temp(z, l);
       end
    end
    if zmax + 1 <= nz + 1
        zvect_pcol(zmax + 1:nz + 1, l) = NaN;
    end
end
zvect_pcol = [zvect_pcol, zvect_pcol(:, end)];

atracer_pcol = [atracer, NaN * ones(nz, 1)];
atracer_pcol = [atracer_pcol;NaN * ones(1, length(atracer_pcol(1, :)))];
atracer_pcol(find(isnan(zvect_pcol))) = NaN;
