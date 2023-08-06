function [vecj, veci] = locingrid(lon, lat, matlon, matlat)
%LOCINGRID locates the nearest grid point point (lon, lat) within grid defined by matlon and matlat
%
% DESCRIPTION
% LOCINGRID locates the nearest grid point point (lon, lat) within grid defined by matlon and matlat
%
% EXAMPLES
%
%   See also sections_MODEL, secingrid, almanac
%
% TODO do not use almanac (not recommended function)
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

a = max(max(diff(matlon)));
b = max(max(diff(matlon')));
step_x = max(a, b);
c = max(max(diff(matlat)));
d = max(max(diff(matlat')));
step_y = max(c, d);

for l=1:length(lon)

    if lon(l) < min(min(matlon))
        lon(l) = lon(l) + 360;
    end
    if lon(l) > max(max(matlon))
        lon(l) = lon(l) - 360;
    end

    [j, i] = find((matlon <= lon(l) + step_x) & (matlon >= (lon(l) - step_x)) & (matlat <= lat(l) + step_y) & (matlat >= (lat(l) - step_y)));

    clear dis
    if length(j) > 1
        for ii=1:length(j)
            ee = almanac('earth', 'ellipsoid');
            dis(ii) = distance(lat(l), lon(l), matlat(j(ii), i(ii)), matlon(j(ii), i(ii)), ee);
        end
        [val, ind] = min(dis);
    else
        if length(j) == 1
            ind = 1;
        else
            error(['JD locingrid: please check that (' num2str(lat(l)) 'N, ' num2str(lon(l)) 'E) point is within grid boundaries'])
        end
    end

    vecj(l) = j(ind);
    veci(l) = i(ind);

end
