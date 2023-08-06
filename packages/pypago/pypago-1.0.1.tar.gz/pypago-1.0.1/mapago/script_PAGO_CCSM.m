%SCRIPT_PAGO_CCSM
%
%   See also LOADDATA_CCSM
%
% TODO remove hard coded path
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% move to directory where all programs are located
cd /full/path/to/PAGO_v0/

% variable to store where files produced by PAGO are located
basedir = '/full/path/to/PAGO/CCSM/';

% list of variables to shorten the call to PAGO functions
refstructfile = [basedir 'b40_test_refstructfile.mat']; % reference structfile that contains sections and areas information
structfile = [basedir 'b40_test_000101-000112.mat']; % structfile where data is uploaded
file_location = ['/full/path/to/CCSM/data/']; % location of model output
file_prefix = 'b40_test.'; % first part of model output file name
file_suffix = '000101-000112'; % middle part of model output file name, which usually specifies the time period contained in the file

% step 1: extract information on grid (mask, bathymetry, scale factors...) and chose sections and areas
sections_MODEL()
% save information into refstructfile

% step 2: load model output into structfile
[status,message,messageid] = copyfile( refstructfile, structfile);
if status
   msg = sprintf('copy ok');
   disp(msg);
else
   disp(message);
   disp(messageid);
   error('%s: copyfile %s %s failed', mfilename, refstructfile, structfile);
end

loaddata_CCSM(structfile, file_location, file_prefix, file_suffix);

% eventually save model output along sections into netcdf file
create_netcdf_sec(structfile, '000101', 'CCSM b40 test')

% step 3: calculate indices for sections
CCSM_indices = indices_MODEL(structfile);
% eventually calculate yearly averages of monthly indices
CCSM_indices_yr = yrave_indices(CCSM_indices, 2);
% eventually save indices into .mat file
save(fullfile(basedir, ['b40_test_000101-000112_indices.mat CCSM_indices CCSM_indices_yr']));
% eventually save monthly indices into netcdf file
create_netcdf_ind(CCSM_indices, '000101', 'CCSM b40 test', [basedir 'b40_test_000101-000112_indices.nc'])
% or save yearly indices
create_netcdf_ind(CCSM_indices_yr, '000101', 'CCSM b40 test', [basedir 'b40_test_000101-000112_indices_yr.nc'])

% step 4: calculate indices for areas
CCSM_volumes = volumes_MODEL(structfile);
% eventually calculate yearly averages of monthly indices
CCSM_volumes_yr = yrave_volumes(CCSM_volumes, 2);
% eventually save indices into matlab file
save(fullfile(basedir, ['b40_test_000101-000112_volumes.mat CCSM_volumes CCSM_volumes_yr']));
% eventually save monthly indices into netcdf file
create_netcdf_vol(CCSM_volumes, '000101', 'CCSM b40 test', [basedir 'b40_test_000101-000112_volumes.nc'])
% or save yearly indices
create_netcdf_vol(CCSM_volumes_yr, '000101', 'CCSM b40 test', [basedir 'b40_test_000101-000112_volumes_yr.nc'])

% plot figure of mean characteristics along section
figure_section_1l(structfile);

% done !
