function [] = create_netcdf_sec(structfile, debut_str, simu, varargin)
%CREATE_NETCDF_SEC saves data along section from .mat structfile into a NetCDF file
%
% DESCRIPTION
% saves data along section from .mat structfile into a NetCDF file
%
% debut_str is a comment precising the starting date of the simulation
%
% simu is a comment precising the full name of the simulation
%
% additional arguments are name of the sections to be saved, and
% unit of the time vector ('days', 'months', 'years',...)
%
% EXAMPLES
%
%   See also CREATE_NETCDF_IND, CREATE_NETCDF_VOL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- modified on July, 10th 2012

load(structfile);

nsec = length(MODEL_sections);

time_unit = [];
if nargin > 0
    time_unit = varargin{2};
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

if not(isempty(varargin))
    secsave = findsecnum(MODEL_sections, varargin{1});
else
    disp('available sections:')
    for sec=1:nsec
        disp([MODEL_sections(sec).name])
    end
    secsave_allnames = input('enter list of sections to save (list of names separated by space): ', 's');
    secsave = [];
    temp = find(strcmp(secsave_allnames, ' '));
    temp = cat(2, 0, temp);
    for ind=1:length(temp)
        secsave = cat(1, secsave, findsecnum(MODEL_sections, secsave_allnames(temp(ind) + 1:temp(ind) + 3)));
    end
end

for s=1:length(secsave)
    filen = [structfile(1:end - 4) '_' MODEL_sections(secsave(s)).name '.nc'];
    fn = netcdf.create(filen, 'clobber');
    dim_time = netcdf.defDim(fn, 'time', netcdf.getConstant('NC_UNLIMITED'));
    dim_z = netcdf.defDim(fn, 'z',size(MODEL_sections(secsave(s)).areavect,1));
    dim_l = netcdf.defDim(fn, 'l', size(MODEL_sections(secsave(s)).areavect, 2));

    var_time = netcdf.defVar(fn, 'time', 'float', [dim_time]);
    netcdf.putAtt(fn, var_time, 'standard_name', 'time');
    netcdf.putAtt(fn, var_time, 'long_name', 'time');
    netcdf.putAtt(fn, var_time, 'MissingValue', 'NaN');
    netcdf.putAtt(fn, var_time, 'units', [time_unit ' since ' debut_str]);

    var_areavect = netcdf.defVar(fn, 'areavect', 'float', [dim_l dim_z]);
    netcdf.putAtt(fn, var_areavect, 'units', ['m*m']);
    netcdf.putAtt(fn, var_areavect, 'long_name', 'area dz*dl of each cell along section');

    var_lengthvect = netcdf.defVar(fn, 'lengthvect', 'float', [dim_l]);
    netcdf.putAtt(fn, var_lengthvect, 'units', 'm');
    netcdf.putAtt(fn, var_lengthvect, 'long_name', 'length dl of each cell along section');

    var_depthvect = netcdf.defVar(fn, 'depthvect', 'float', [dim_l dim_z]);
    netcdf.putAtt(fn, var_depthvect, 'units', 'm');
    netcdf.putAtt(fn, var_depthvect, 'long_name', 'thickness dz of each cell along section');

    var_vect = netcdf.defVar(fn, 'vect', 'float', [dim_l dim_z dim_time]);
    netcdf.putAtt(fn, var_vect, 'units', 'C');
    netcdf.putAtt(fn, var_vect, 'long_name', 'potential temperature along section');

    var_vecs = netcdf.defVar(fn, 'vecs', 'float', [dim_l dim_z dim_time]);
    netcdf.putAtt(fn, var_vecs, 'units', 'psu');
    netcdf.putAtt(fn, var_vecs, 'long_name', 'salinity along section');

    var_vecv = netcdf.defVar(fn, 'vecv', 'float', [dim_l dim_z dim_time]);
    netcdf.putAtt(fn, var_vecv, 'units', 'm/s');
    netcdf.putAtt(fn, var_vecv, 'long_name', 'velocity normal to section');

    if isfield(MODEL_sections, 'vech')
        var_vech = netcdf.defVar(fn, 'vech', 'float', [dim_l dim_z dim_time]);
        netcdf.putAtt(fn, var_vech, 'units', 'm');
        netcdf.putAtt(fn, var_vech, 'long_name', 'thickness of layers');
    end

    % add details about the creation of the file
    netcdf.putAtt(fn,netcdf.getConstant('GLOBAL'), 'title', 'PAGO sections');
    netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'simulation', simu);
    netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'institution', 'LOCEAN-CNRS, WHOI');
    netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'CreationDate', datestr(now, 'yyyy/mm/dd HH:MM:SS'));
    netcdf.putAtt(fn, netcdf.getConstant('GLOBAL'), 'CreatedBy', 'Julie Deshayes');

    % end of definition of nc file
    netcdf.endDef(fn)

    if isnan(MODEL_time(1))
        start = 2;
    else
        start = 1;
    end
    nt = length(MODEL_time(start:end));
    netcdf.putVar(fn, var_time, 0, nt, single(MODEL_time(start:end)));
    netcdf.putVar(fn, var_areavect, single(MODEL_sections(secsave(s)).areavect'));
    netcdf.putVar(fn, var_lengthvect, single(MODEL_sections(secsave(s)).lengthvect'));
    netcdf.putVar(fn, var_depthvect, single(MODEL_sections(secsave(s)).depthvect'));
    netcdf.putVar(fn, var_vect, permute(single(reshape(MODEL_sections(secsave(s)).vect(start:end, :, :), [length(MODEL_time) - start + 1 size(MODEL_sections(secsave(s)).areavect, 1) size(MODEL_sections(secsave(s)).areavect, 2)])), [3 2 1]));
    netcdf.putVar(fn, var_vecs, permute(single(reshape(MODEL_sections(secsave(s)).vecs(start:end, :, :), [length(MODEL_time) - start + 1 size(MODEL_sections(secsave(s)).areavect, 1) size(MODEL_sections(secsave(s)).areavect, 2)])), [3 2 1]));
    netcdf.putVar(fn, var_vecv, permute(single(reshape(MODEL_sections(secsave(s)).vecv(start:end, :, :), [length(MODEL_time) - start + 1 size(MODEL_sections(secsave(s)).areavect, 1) size(MODEL_sections(secsave(s)).areavect, 2)])), [3 2 1]));

    if isfield(MODEL_sections, 'vech')
        netcdf.putVar(fn, var_vech, permute(single(reshape(MODEL_sections(secsave(s)).vech(start:end, :, :), [length(MODEL_time) - start + 1 size(MODEL_sections(secsave(s)).areavect, 1) size(MODEL_sections(secsave(s)).areavect, 2)])), [3 2 1]));
    end

    netcdf.close(fn)

end
