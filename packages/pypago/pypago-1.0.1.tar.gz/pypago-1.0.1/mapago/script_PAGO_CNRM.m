%SCRIPT_PAGO_CNRM
%
%   See also LOADDATA_CNRM
%
% TODO remove hard coded path
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% move to directory where all programs are located
cd /full/path/to/PAGO_v0/

% variable to store where files produced by PAGO are located
basedir = '/full/path/to/PAGO/CNRM/';

% list of variables to shorten the call to PAGO functions
refstructfile = [basedir 'CNRM_test_refstructfile.mat']; % reference structfile that contains sections and areas information
structfile = [basedir 'CNRM_test_185001-185912.mat']; % structfile where data is uploaded
file_location = ['/full/path/to/CNRM/data/'];
file_prefix = '_Omon_CNRM-CM5_piControl_r1i1p1'; % first part of model output file name
file_suffix = '185001-185912'; % middle part of model output file name, which usually specifies the time period contained in the file

% step 1: extract information on grid (mask, bathymetry, scale factors...) and chose sections and areas
sections_MODEL()
% save information into refstructfile

% step 2: load model output into structfile
[status,message,messageid] = copyfile(refstructfile, structfile);
if status
   msg = sprintf('copy ok');
   disp(msg);
else
   disp(message);
   disp(messageid);
   error('%s: copyfile %s %s failed', mfilename, refstructfile, structfile);
end

loaddata_CNRM(structfile, file_location, file_prefix, file_suffix);

%eventually save model output along sections into netcdf file
create_netcdf_sec(structfile, '185001', 'CNRM test')

% step 3: calculate indices for sections
CNRM_indices = indices_MODEL(structfile);
% eventually calculate yearly averages of monthly indices
CNRM_indices_yr = yrave_indices(CNRM_indices);
% eventually save indices into .mat file
save(fullfile(basedir, ['CNRM_test_', file_suffix, '_indices.mat']), 'CNRM_indices', 'CNRM_indices_yr');
% eventually save monthly indices into netcdf file
create_netcdf_ind(CNRM_indices, '185001', 'CNRM test', [basedir 'CNRM_test_' file_suffix '_indices.nc'])
% or save yearly indices
create_netcdf_ind(CNRM_indices, '185001', 'CNRM test', [basedir 'CNRM_test_' file_suffix '_indices_yr.nc'])

% step 4: calculate indices for areas
CNRM_volumes = volumes_MODEL(structfile);
% eventually calculate yearly averages of monthly indices
CNRM_volumes_yr = yrave_volumes(CNRM_volumes, 2);
% eventually save indices into matlab file
save(fullfile(basedir, ['CNRM_test', file_suffix, '_volumes.mat']), 'CNRM_volumes', 'CNRM_volumes_yr');
% eventually save monthly indices into netcdf file
create_netcdf_vol(CNRM_volumes, '185001', 'CNRM test', [basedir 'CNRM_test_' file_suffix '_volumes.nc'])
% or save yearly indices
create_netcdf_vol(CNRM_volumes, '185001', 'CNRM test', [basedir 'CNRM_test_' file_suffix '_volumes_yr.nc'])

% plot figure of mean characteristics along section
figure_section_1l(structfile);

% done !
