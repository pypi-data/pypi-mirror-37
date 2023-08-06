function [] = create_netcdf_ind(indices, debut_str, simu, ncfile, varargin)
%CREATE_NETCDF_IND saves indices into NetCDF file named ncfile
%
% DESCRIPTION
%
% CREATE_NETCDF_IND saves indices into NetCDF file named ncfile
%
% debut_str is a comment precising the starting date of the simulation
%
% simu is a comment precising the full name of the simulation
%
% additional argument is the unit of the time vector
% ('days', 'months', 'years', ...)
%
% EXAMPLES
%
%   See also CREATE_NETCDF_SEC, CREATE_NETCDF_VOL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- modified on July, 10th 2012

load definition_indices_vol_3zlev.mat

nt = length(indices(1).time);

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
dim_section = netcdf.defDim(fn, 'section', length(indices));
dim_l = netcdf.defDim(fn, 'l', 3);

% create axes with appropriate attributes

var_time = netcdf.defVar(fn, 'time', 'float', [dim_time]);
netcdf.putAtt(fn, var_time, 'standard_name', 'time');
netcdf.putAtt(fn, var_time, 'long_name', 'time');
netcdf.putAtt(fn, var_time, 'MissingValue', 'NaN');
netcdf.putAtt(fn, var_time, 'units', [time_unit ' since ' debut_str]);

var_section_name = netcdf.defVar(fn, 'section_name', 'char', [dim_l dim_section]);

% load variable names and attributes from load_definition.m if they exist in
% indices
for n=1:length(definition)
    if isfield(indices, definition(n).name)
        varid = netcdf.defVar(fn, definition(n).name, 'float', [dim_section dim_time]);
        var(n) = varid;
        netcdf.putAtt(fn, var(n), 'units', definition(n).unit);
        netcdf.putAtt(fn, var(n), 'long_name', definition(n).longname);
        if not(isempty(definition(n).comment))
            netcdf.putAtt(fn, var(n), 'comment', definition(n).comment);
        end
    end
end

% add details about the creation of the file

netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'title', 'PAGO time series');
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'simulation', simu);
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'institution', 'LPO-CNRS, WHOI');
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'CreationDate', datestr(now, 'yyyy/mm/dd HH:MM:SS'));
netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'CreatedBy', 'Julie Deshayes');

netcdf.endDef(fn)
% load data into nc file

for sec=1:length(indices)
    name(sec, :) = indices(sec).name;
end
netcdf.putVar(fn, var_section_name, name');

if isnan(indices(1).time(1))
    start = 2;
else
    start = 1;
end
netcdf.putVar(fn, var_time, 0, length(indices(1).time(start:end)), indices(1).time(start:end));

temp = [];
for n=1:length(definition)
    if isfield(indices, definition(n).name)
        for sec=1:length(indices)
            eval(['temp = indices(sec).' definition(n).name ';'])
            if isempty(temp)
                temp = NaN * ones(1, length(indices(1).time));
            end
            tempmat(sec, :) = temp(start:end);
        end
        netcdf.putVar(fn, var(n), tempmat);
    end
end

% close nc file
netcdf.close(fn)
