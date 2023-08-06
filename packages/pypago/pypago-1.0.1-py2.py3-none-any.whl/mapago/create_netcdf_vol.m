function [] = create_netcdf_vol(volumes, debut_str, simu, ncfile, varargin)
%CREATE_NETCDF_VOL saves volumes into NetCDF file named ncfile
%
% DESCRIPTION
% CREATE_NETCDF_VOL saves volumes into NetCDF file named ncfile
%
% debut_str is a comment precising the starting date of the simulation
%
% simu is a comment precising the full name of the simulation
%
% additional argument is the unit of the time vector ('days', 'months', 'years'...)
%
% EXAMPLES
%
% TODO
% missing value must not be NaN
%
%   See also CREATE_NETCDF_IND, CREATE_NETCDF_SEC
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- modified on May, 15th 2012
load definition_indices_vol_3zlev.mat

nt = length(volumes(1).time);

time_unit = [];
if nargin > 0
    time_unit = varargin{:};
else
    disp(['MODEL_time = ' num2str(indices(1).time(1:min(20, nt))') ])
end
while isempty(time_unit)
    freq = input('in days (d), months (m) or years (y) ? ', 's');
    switch freq
        case 'd'
            time_unit = 'days';
        case 'm'
            time_unit = 'months';
        case 'y'
            time_unit = 'years';
        otherwise
            freq = input('in days (d), months (m) or years (y) ? ', 's');
    end
end

% create nc file
fn = netcdf.create(ncfile, 'clobber');

% create the dimensions with the appropriate names: depth, latitude,
% longitude, time ...

dim_time = netcdf.defDim(fn, 'time', netcdf.getConstant('NC_UNLIMITED'));
dim_area = netcdf.defDim(fn, 'area', length(volumes));
dim_l = netcdf.defDim(fn, 'l', 6);

% create axes with appropriate attributes

var_time = netcdf.defVar(fn, 'time', 'float', [dim_time]);
netcdf.putAtt(fn, var_time, 'standard_name', 'time');
netcdf.putAtt(fn, var_time, 'long_name', 'time');
netcdf.putAtt(fn, var_time, 'MissingValue', 'NaN');
netcdf.putAtt(fn, var_time, 'units', [time_unit ' since ' debut_str]);

var_area_name = netcdf.defVar(fn, 'area_name', 'char', [dim_l dim_area]);

% load variable names and attributes from load_definition.m if they exist in
% volume
for n=1:length(defvol)
    if isfield(volumes, defvol(n).name)
        varid = netcdf.defVar(fn, defvol(n).name, 'float', [dim_area dim_time]);
        var(n) = varid;
        netcdf.putAtt(fn, var(n), 'units', defvol(n).unit);
        netcdf.putAtt(fn, var(n), 'long_name', defvol(n).longname);
        if not(isempty(defvol(n).comment))
            netcdf.putAtt(fn, var(n), 'comment', definition(n).comment);
        end
    end
end

% add details about the creation of the file
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'title', 'PAGO volume indices');
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'simulation', simu);
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'institution', 'LPO-CNRS, WHOI');
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'CreationDate', datestr(now, 'yyyy/mm/dd HH:MM:SS'));
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'CreatedBy', 'Julie Deshayes');

netcdf.endDef(fn)
% load data into nc file

for sec=1:length(volumes)
    name(sec, :) = volumes(sec).name;
end
netcdf.putVar(fn, var_area_name, name');

if isnan(volumes(1).time(1))
    start = 2;
else
    start = 1;
end
netcdf.putVar(fn, var_time, 0, length(volumes(1).time(start:end)), volumes(1).time(start:end));

temp = [];
for n=1:length(defvol)
    if isfield(volumes, defvol(n).name)
        for sec=1:length(volumes)
            eval(['temp = volumes(sec).' defvol(n).name ';'])
            if isempty(temp)
                temp = NaN * ones(1, length(volumes(1).time));
            end
            if length(temp) > 1
                tempmat(sec, :) = temp(start:end);
            else
                tempmat(sec, :) = temp;
            end
        end
        netcdf.putVar(fn, var(n), tempmat);
    end
end

% close nc file
netcdf.close(fn)
