%SCRIPT_PAGO_IPSL_FORDEV
% prepare and run loaddata on IPSL model for indices on predefined sections
% for developers
%
% DESCRIPTION
%
% prepare and run loaddata on IPSL model for indices on predefined sections
% for developers
%
% the main difference between this program and the equivalent for end-users is
% non interactivity
%
% EXAMPLES
%
% TODO
% create_netcdf_sec on all default sections or at least ar7 ovi
%
% cf. rundemotest.rst
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% add MAPAGO to path
addpath(fullfile(getenv('PAGO'), 'mapago'));

% variable to store where files produced by PAGO are located
model = 'IPSL';
basedir = fullfile(getenv('HOME'), '.pago', getenv('HOSTNAME'), 'mapago', getenv('PAGO_SVN_RELEASE') , version('-release'), model);
[status, message, messageid] = mkdir(basedir);
if status
   msg = sprintf('mkdir(%s) ok', basedir);
   disp(msg);
else
   disp(message)
   disp(messageid)
   error('%s: mkdir %s failed', mfilename, basedir);
   exit(-1);
end

% define logfile
log = fullfile(basedir, [mfilename '.log']);
diary(log);
diary on

% step 1: extract information on grid (mask, bathymetry, scale factors...) and
% chose sections and areas
% mask is here /data/jdeshayes/piControl2_mesh_mask.nc
%sections_MODEL()
% save information into refstructfile

% list of variables to shorten the call to PAGO functions
% reference structfile that contains sections and areas information
testdir = fullfile(getenv('PAGO'), 'mapago', 'test', 'IPSL');
refstructfile= fullfile(testdir, 'IPSLCM5_piControl2_NA_refstructfile.mat');
% structfile where data is uploaded
structfile = fullfile(basedir, 'IPSLCM5_piControl2_NA_180001-184912.mat');
file_location = fullfile(testdir, 'CMIP5/IPSL/IPSL-CM5A-LR/piControl/mon/ocean/Omon/r1i1p1/latest/');
% first part of model output file name
file_prefix='Omon_IPSL-CM5A-LR_piControl_r1i1p1';
% middle part of model output file name, which usually specifies the time
% period contained in the file
file_suffix='180001-184912';


% step 2: load model output into structfile
[status,message,messageid] = copyfile(refstructfile, structfile);
if status
   msg = sprintf('copy ok');
   disp(msg);
else
   error('%s: copyfile %s %s failed', mfilename, refstructfile, structfile);
   disp(message);
   disp(messageid);
   exit(-1);
end

loaddata_IPSL(structfile, file_location, file_prefix, file_suffix);

section_name = '26n'
% eventually save model output along sections into netcdf file
create_netcdf_sec(structfile,'1800-01-01 00:00:00','IPSLCM5 piControl2 r1i1p1 NA', section_name, 'days');

% step 3: calculate indices for sections
IPSL_indices=indices_MODEL(structfile, 1);

% eventually calculate yearly averages of monthly indices
% set calendar type. see time:calendar of input netcdf files "time:calendar = "noleap"
leap = 0;
IPSL_indices_yr=yrave_indices(IPSL_indices, leap);

% eventually save indices into .mat file
save(fullfile(basedir, ['IPSL_test_', file_suffix, '_indices.mat']), 'IPSL_indices', 'IPSL_indices_yr');

% eventually save monthly indices into netcdf file
ncfile = fullfile(basedir, ['IPSL_test_' file_suffix '_indices.nc']);
create_netcdf_ind(IPSL_indices,'1800-01-01 00:00:00','IPSL test', ncfile, 'days');

% and save yearly indices
ncfile = fullfile(basedir, ['IPSL_test_' file_suffix '_indices_yr.nc']);
create_netcdf_ind(IPSL_indices_yr,'1800-01-01 00:00:00','IPSL test', ncfile, 'days');

% end
exit(0)
