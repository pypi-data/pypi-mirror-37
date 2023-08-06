%LOAD_DEFINITION_T
% DESCRIPTION
%
% run LOAD_DEFINITION and compare output to reference
%
% See also rundemotest
%
% TODO exit with status 0 if identical, otherwise switch to debug mode
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

load_definition();
file1=fullfile(getenv('HOME'), '.pago', 'definition_indices_vol_3zlev.mat');
file2=fullfile(getenv('PAGO'), 'mapago', 'test', 'load_definition', 'output', 'definition_indices_vol_3zlev.mat');
visdiff(file1, file2);
