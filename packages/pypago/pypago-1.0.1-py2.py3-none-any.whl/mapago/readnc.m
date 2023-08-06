function[res] = readnc(file, var, varargin)
%READNC
%
% DESCRIPTION
%
% file is the netcdf file that has to be open,
%
% var is the name of the variable to be loaded, as it appears when doing
% ncdump on the file,
%
% varargin must be (in that order): start, end, step (each of those
% vectors has n numbers corresponding to the n dimensions of the variable,
% in the same order as the dimensions appear when doing ncdump on the file,
% (note also that indexation starts with 1 as usually in matlab).
%
% the result res has dimensions in the order of their appearance when doing
% ncdump on the file.
%
% EXAMPLES
%
%   See also LOADDATA_CCSM, LOADDATA_CNRM, LOADDATA_GFDL, LOADDATA_IPSL,
%   READNC_WRAP, SECTIONS_MODEL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD --- created on March, 18th, 2010

% checks that start, end and step are lines
if not(isempty(varargin))
    if size(varargin{1}, 1) ~= 1
        start = varargin{1}';
    else
        start = varargin{1};
    end
    if size(varargin{2}, 1) ~= 1
        endd = varargin{2}';
    else
        endd = varargin{2};
    end
    if length(varargin) < 3
        step = ones(1, length(start));
    else
        if size(varargin{3}, 1) ~= 1
            step = varargin{3}';
        else
            step = varargin{3};
        end
    end
end

ncid = netcdf.open(file, 'nc_nowrite');
varid = netcdf.inqVarID(ncid, var);
if nargin == 2
    temp = netcdf.getVar(ncid, varid);
    res = permute(temp, [ndims(temp):-1:1]);
else
    [varname, xtype, dimids, natts] = netcdf.inqVar(ncid, varid);
    take_all = find(endd == -1);
    for l=1:length(take_all)
        [dimname, dimlen] = netcdf.inqDim(ncid, dimids(end-take_all(l) + 1));
        endd(take_all(l)) = dimlen;
    end
    start = fliplr(start) - 1;
    % JD correction on 07/03/2013 as the line below does not work for step different than 1
    % count = fliplr(endd) - 1 - start + 1;
    stride = fliplr(step);
    count = (fliplr(endd) - 1 - start)./stride + 1;
    temp = netcdf.getVar(ncid, varid, start, count, stride, 'double');
    res = permute(temp, [ndims(temp):-1:1]);
end
% force res to be double
res = double(res);
% substitute missing value if defined for this variable
[varname, vartype, vardimIDs, varatts] = netcdf.inqVar(ncid, varid);
test = 0;
for l=1:varatts
    if length(netcdf.inqAttName(ncid, varid, (l - 1))) == 10%13
        if strcmp(netcdf.inqAttName(ncid, varid, (l - 1)), '_FillValue')  % 'missing_value'
            test = 1;
        end
    end
end
if test == 1
    % missval = double(netcdf.getAtt(ncid, netcdf.inqVarID(ncid, var), 'missing_value'));
    missval = double(netcdf.getAtt(ncid, netcdf.inqVarID(ncid, var), '_FillValue'));
    res(find(res == missval)) = NaN;
end
% check presence of attributes scale_factor and add_offset
test_sf = 0;
test_ao = 0;
for l=1:varatts
    if length(netcdf.inqAttName(ncid, varid, (l - 1))) == 12
        if strcmp(netcdf.inqAttName(ncid, varid, (l - 1)), 'scale_factor')
            test_sf = 1;
        end
    end
    if length(netcdf.inqAttName(ncid, varid, (l - 1))) == 10
        if strcmp(netcdf.inqAttName(ncid, varid, (l - 1)), 'add_offset')
            test_ao = 1;
        end
    end
end
if test_sf == 1
    scalefactor = double(netcdf.getAtt(ncid, netcdf.inqVarID(ncid, var), 'scale_factor'));
    res = res * scalefactor;
end
if test_ao == 1
    addoffset = double(netcdf.getAtt(ncid, netcdf.inqVarID(ncid, var), 'add_offset'));
    res = res + addoffset;
end
netcdf.close(ncid);
