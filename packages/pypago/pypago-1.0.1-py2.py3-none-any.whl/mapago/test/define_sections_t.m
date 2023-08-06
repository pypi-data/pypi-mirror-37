%DEFINE_SECTIONS_T
% DESCRIPTION
%
% run DEFINE_SECTIONS and compare output to reference
%
% See also rundemotest
%
% TODO
% exit with status 0 if identical, otherwise switch to debug mode
%
% visdiff without returned value is may be not the best solution because only
% one is performed (the first in the loop) !
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% add MAPAGO to path
addpath(fullfile(getenv('PAGO'), 'mapago'));

basedir = fullfile(getenv('HOME'), '.pago', getenv('HOSTNAME'), 'mapago', getenv('PAGO_SVN_RELEASE') , version('-release'));
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

define_sections()
% ++region_codes = {'GL', 'NA', 'AR', 'SA'};
region_codes = {'NA', 'AR', 'SA'};
for iregion_code=1:length(region_codes)
    onefile = sprintf('sections_%s.mat', region_codes{iregion_code});
    file1=fullfile(getenv('HOME'), '.pago', onefile);
    file2=fullfile(getenv('PAGO'), 'mapago', 'test', 'define_sections', 'output', onefile);
    visdiff(file1, file2);
end
