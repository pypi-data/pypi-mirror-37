function [res] = readnc_wrap(file, var, debut, fin, nlon)
%READNC_WRAP
%
% DESCRIPTION
%
% considers that the data is cyclical for the last dimension (this program
% does not work if the data is cyclical in another dimension, or in more
% than one dimension) in case debut(end) is negative, fin(end) is larger than
% nlon, or fin(end) is smaller than debut.
%
% EXAMPLES
%
%   See also LOADDATA_CCSM LOADDATA_CNRM LOADDATA_GFDL LOADDATA_IPSL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO
%
% JD --- created on March, 22th, 2010

if size(debut, 1) > size(debut, 2)
    debut = debut';
end

if size(fin, 1) > size(fin, 2)
    fin = fin';
end

if debut(end) < 1
    res1 = readnc(file, var, [debut(1:end - 1) nlon-(abs(debut(end)))], [fin(1:end - 1) nlon], ones(size(debut)));
    res2 = readnc(file, var, [debut(1:end - 1) 1], [fin(1:end - 1) fin(end)], ones(size(debut)));
    res = cat(max(ndims(res1), ndims(res2)), res1, res2);
else
    if fin(end) > nlon
        res1 = readnc(file, var, debut, [fin(1:end - 1) nlon], ones(size(debut)));
        res2 = readnc(file, var, [debut(1:end - 1) 1], [fin(1:end - 1) fin(end)-nlon], ones(size(debut)));
        res = cat(max(ndims(res1), ndims(res2)), res1, res2);
    else
        if fin(end) < debut(end)
            res1 = readnc(file, var, debut, [fin(1:end - 1) nlon], ones(size(debut)));
            res2 = readnc(file, var, [debut(1:end - 1) 1], [fin(1:end - 1) fin(end)], ones(size(debut)));
            res = cat(max(ndims(res1), ndims(res2)), res1, res2);
        else
            res = readnc(file, var, debut, fin, ones(size(debut)));
        end
    end
end
