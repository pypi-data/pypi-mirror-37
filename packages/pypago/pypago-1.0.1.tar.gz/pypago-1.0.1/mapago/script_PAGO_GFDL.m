%SCRIPT_PAGO_GFDL
%
%   See also LOADDATA_GFDL
%
% TODO remove hard coded path
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% move to directory where all programs are located
cd /full/path/to/PAGO_v0/

% variable to store where files produced by PAGO are located
basedir = '/full/path/to/PAGO/GFDL/';

% list of variables to shorten the call to PAGO functions
refstructfile = [basedir 'GFDL_test_refstructfile.mat']; % reference structfile that contains sections and areas information
structfile = [basedir 'GFDL_test_000101-000512.mat']; % structfile where data is uploaded
URL = 'http://nomads.gfdl.noaa.gov:9192/opendap/CMIP5/output1/NOAA-GFDL/GFDL-CM3/piControl/mon/ocean/Omon/r1i1p1/v20110601/'; % location of model output
file_prefix = '_Omon_GFDL-CM3_piControl_r1i1p1_'; % first part of model output file name
file_suffix = '000101-000512'; % middle part of model output file name, which usually specifies the time period contained in the file

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

loaddata_GFDL_opendap(structfile, URL, file_prefix, file_suffix)

% eventually save model output along sections into netcdf file
create_netcdf_sec(structfile, '000101', 'GFDL test');

% step 3: calculate indices for sections
GFDL_indices = indices_MODEL(structfile);
% eventually calculate yearly averages of monthly indices
GFDL_indices_yr = yrave_indices(GFDL_indices, 2);
% eventually save indices into .mat file
save(fullfile(basedir, ['GFDL_test_000101-000512_indices.mat']), 'GFDL_indices', 'GFDL_indices_yr');
% eventually save monthly indices into netcdf file
create_netcdf_ind(GFDL_indices, '000101', 'GFDL test', [basedir 'GFDL_test_000101-000512_indices.nc'])
% or save yearly indices
create_netcdf_ind(GFDL_indices_yr, '000101', 'GFDL test', [basedir 'GFDL_test_000101-000512_indices_yr.nc'])

% step 4: calculate indices for areas
GFDL_volumes = volumes_MODEL(structfile);
% eventually calculate yearly averages of monthly indices
GFDL_volumes_yr = yrave_volumes(GFDL_volumes, 2);
% eventually save indices into matlab file
save(fullfile(basedir, ['GFDL_test_000101-000512_volumes.mat']), 'GFDL_volumes', 'GFDL_volumes_yr');
% eventually save monthly indices into netcdf file
create_netcdf_vol(GFDL_volumes, '000101', 'GFDL test', [basedir 'GFDL_test_000101-000512_volumes.nc'])
% or save yearly indices
create_netcdf_vol(GFDL_volumes_yr, '000101', 'GFDL test', [basedir 'GFDL_test_000101-000512_volumes_yr.nc'])

% plot figure of mean characteristics along section
figure_section_1l(structfile)

% done !
