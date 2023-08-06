%LOAD_DEFINITION
%
% DESCRIPTION
% LOAD_DEFINITION
%
% EXAMPLES
%
% To produce ${HOME}/.pago/definition_indices_vol_3zlev.mat :
%
%   load_definition
%
%   See also INDICES_MODEL, VOLUMES_MODEL
%
% Release notes :
% PAGO V2.0 file saved in ${HOME}/.pago/ instead of current directory
%
% TODO make a function
% TODO add attributes to NetCDF files
% TODO hardcoded reference salinity
% TODO save error handling
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

% these may be modified according to specifications in indices_MODEL.m and
% volumes_MODEL.m
lev1 = 500;
lev2 = 1000;
lev3 = 2000;

clear definition

n = 1;
definition(n).name = 'netmt';
definition(n).unit = 'Sv';
definition(n).longname = 'Net mass transport';

n = n + 1;
definition(n).name = 'netht';
definition(n).unit = 'PW';
definition(n).longname = 'Net heat transport';

n = n + 1;
definition(n).name = 'netft';
definition(n).unit = 'mSv';
definition(n).longname = 'Net freshwater transport';
definition(n).comment = 'reference salinity S0=34.8';

n = n + 1;
definition(n).name = 'totht';
definition(n).unit = 'PW';
definition(n).longname = 'heat transport when net mass transport across section = 0';

n = n + 1;
definition(n).name = 'totft';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transport when net mass transport across section = 0';
definition(n).comment = 'reference salinity S0=34.8';

n = n + 1;
definition(n).name = 'ovmt';
definition(n).unit = 'Sv';
definition(n).longname = 'max overturning mass transport from surface';
definition(n).comment = 'calculated after removing net mass transport across section';

n = n + 1;
definition(n).name = 'dpmt';
definition(n).unit = 'm';
definition(n).longname = 'depth of max overturning mass transport';

n = n + 1;
definition(n).name = 'ovht';
definition(n).unit = 'PW';
definition(n).longname = 'heat transported by overturning circulation';
definition(n).comment = 'calculated after removing net mass transport across section : totht=ovht+bpht+bcht';

n = n + 1;
definition(n).name = 'ovft';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transported by overturning circulation';
definition(n).comment = 'calculated after removing net mass transport across section : totft=ovft+bpft+bcft';

n = n + 1;
definition(n).name = 'ovrmt_s0_1';
definition(n).unit = 'Sv';
definition(n).longname = 'max overturning mass transport in density space from surface';
definition(n).comment = 'sigma0 densities, ie potential density referenced at surface';

n = n + 1;
definition(n).name = 'dsmt_s0_1';
definition(n).unit = 'kg/m3';
definition(n).longname = 'density of max overturning mass transport';
definition(n).comment = 'sigma0 densities, ie potential density referenced at surface';

n = n + 1;
definition(n).name = 'ovrht_s0_1';
definition(n).unit = 'PW';
definition(n).longname = 'heat transported by overturning circulation in density space';
definition(n).comment = 'sigma0 densities, ie potential density referenced at surface';

n = n + 1;
definition(n).name = 'ovrft_s0_1';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transported by overturning circulation in density space';
definition(n).comment = 'sigma0 densities, ie potential density referenced at surface';

n = n + 1;
definition(n).name = 'ovrmt_s1';
definition(n).unit = 'Sv';
definition(n).longname = 'max overturning mass transport in density space from surface';
definition(n).comment = 'sigma1 densities, ie potential density referenced at 1000 m depth';

n = n + 1;
definition(n).name = 'dsmt_s1';
definition(n).unit = 'kg/m3';
definition(n).longname = 'density of max overturning mass transport';
definition(n).comment = 'sigma1 densities, ie potential density referenced at 1000 m depth';

n = n + 1;
definition(n).name = 'ovrht_s1';
definition(n).unit = 'PW';
definition(n).longname = 'heat transported by overturning circulation in density space';
definition(n).comment = 'sigma1 densities, ie potential density referenced at 1000 m depth';

n = n + 1;
definition(n).name = 'ovrft_s1';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transported by overturning circulation in density space';
definition(n).comment = 'sigma1 densities, ie potential density referenced at 1000 m depth';

n = n + 1;
definition(n).name = 'ovrmt_s2';
definition(n).unit = 'Sv';
definition(n).longname = 'max overturning mass transport in density space from surface';
definition(n).comment = 'sigma2 densities, ie potential density referenced at 2000 m depth';

n = n + 1;
definition(n).name = 'dsmt_s2';
definition(n).unit = 'kg/m3';
definition(n).longname = 'density of max overturning mass transport';
definition(n).comment = 'sigma2 densities, ie potential density referenced at 2000 m depth';

n = n + 1;
definition(n).name = 'ovrht_s2';
definition(n).unit = 'PW';
definition(n).longname = 'heat transported by overturning circulation in density space';
definition(n).comment = 'sigma2 densities, ie potential density referenced at 2000 m depth';

n = n + 1;
definition(n).name = 'ovrft_s2';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transported by overturning circulation in density space';
definition(n).comment = 'sigma2 densities, ie potential density referenced at 2000 m depth';

n = n + 1;
definition(n).name = 'bpht';
definition(n).unit = 'PW';
definition(n).longname = 'heat transported by barotropic circulation';
definition(n).comment = 'calculated after removing net mass transport across section : totht=ovht+bpht+bcht';

n = n + 1;
definition(n).name = 'bpft';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transported by barotropic circulation';
definition(n).comment = 'calculated after removing net mass transport across section : totft=ovft+bpft+bcft';

n = n + 1;
definition(n).name = 'bcht';
definition(n).unit = 'PW';
definition(n).longname = 'heat transported by baroclinic circulation';
definition(n).comment = 'calculated after removing net mass transport across section : totht=ovht+bpht+bcht';

n = n + 1;
definition(n).name = 'bcft';
definition(n).unit = 'mSv';
definition(n).longname = 'freshwater transported by baroclinic circulation';
definition(n).comment = 'calculated after removing net mass transport across section : totft=ovft+bpft+bcft';

n = n + 1;
definition(n).name = 'ht1';
definition(n).unit = 'PW';
definition(n).longname = ['heat transported by circulation from surface down to ' num2str(lev1) ' m : netht=ht1+ht2+ht3+ht4'];

n = n + 1;
definition(n).name = 'ht2';
definition(n).unit = 'PW';
definition(n).longname = ['heat transported by circulation from ' num2str(lev1) ' m down to ' num2str(lev2) ' m : netht=ht1+ht2+ht3+ht4'];

n = n + 1;
definition(n).name = 'ht3';
definition(n).unit = 'PW';
definition(n).longname = ['heat transported by circulation from ' num2str(lev2) ' m down to ' num2str(lev3) ' m : netht=ht1+ht2+ht3+ht4'];

n = n + 1;
definition(n).name = 'ht4';
definition(n).unit = 'PW';
definition(n).longname = ['heat transported by circulation from ' num2str(lev3) ' m down to bottom : netht=ht1+ht2+ht3+ht4'];

n = n + 1;
definition(n).name = 'ft1';
definition(n).unit = 'mSv';
definition(n).longname = ['freshwater transported by circulation from surface down to ' num2str(lev1) ' m : netft=ft1+ft2+ft3+ft4'];

n = n + 1;
definition(n).name = 'ft2';
definition(n).unit = 'mSv';
definition(n).longname = ['freshwater transported by circulation from ' num2str(lev1) ' m down to ' num2str(lev2) ' m : netft=ft1+ft2+ft3+ft4'];

n = n + 1;
definition(n).name = 'ft3';
definition(n).unit = 'mSv';
definition(n).longname = ['freshwater transported by circulation from ' num2str(lev2) ' m down to ' num2str(lev3) ' m : netft=ft1+ft2+ft3+ft4'];

n = n + 1;
definition(n).name = 'ft4';
definition(n).unit = 'mSv';
definition(n).longname = ['freshwater transported by circulation from ' num2str(lev3) ' m down to bottom : netft=ft1+ft2+ft3+ft4'];

n = n + 1;
definition(n).name = 'mt_bin';
definition(n).unit = 'Sv';
definition(n).longname = ['volume transport for user-defined density bin'];

n = n + 1;
definition(n).name = 'ht_bin';
definition(n).unit = 'PW';
definition(n).longname = ['heat transport for user-defined density bin'];

n = n + 1;
definition(n).name = 'ft_bin';
definition(n).unit = 'mSv';
definition(n).longname = ['freshwater transport for user-defined density bin'];

n = 1;
defvol(n).name = 'sc';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of salinity'];

n = n + 1;
defvol(n).name = 'sc1';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of salinity from surface down to ' num2str(lev1) ' m'];

n = n + 1;
defvol(n).name = 'sc2';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of salinity from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];

n = n + 1;
defvol(n).name = 'sc3';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of salinity from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];

n = n + 1;
defvol(n).name = 'S0c';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of S0=34.8'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'S0c1';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of S0=34.8 from surface down to ' num2str(lev1) ' m'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'S0c2';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of S0=34.8 from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'S0c3';
defvol(n).unit = 'psu * m3';
defvol(n).longname = ['volume integral of S0=34.8 from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'hc';
defvol(n).unit = 'J';
defvol(n).longname = ['heat content'];

n = n + 1;
defvol(n).name = 'hc1';
defvol(n).unit = 'J';
defvol(n).longname = ['heat content from surface down to ' num2str(lev1) ' m'];

n = n + 1;
defvol(n).name = 'hc2';
defvol(n).unit = 'J';
defvol(n).longname = ['heat content from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];

n = n + 1;
defvol(n).name = 'hc3';
defvol(n).unit = 'J';
defvol(n).longname = ['heat content from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];

n = n + 1;
defvol(n).name = 'vol';
defvol(n).unit = 'm3';
defvol(n).longname = ['volume'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'vol1';
defvol(n).unit = 'm3';
defvol(n).longname = ['volume from surface down to ' num2str(lev1) ' m'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'vol2';
defvol(n).unit = 'm3';
defvol(n).longname = ['volume from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'vol3';
defvol(n).unit = 'm3';
defvol(n).longname = ['volume from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'surface';
defvol(n).unit = 'm2';
defvol(n).longname = ['surface area'];
defvol(n).comment = 'constant in time - for calculation purposes';

n = n + 1;
defvol(n).name = 'min';
defvol(n).unit = 'Sv';
defvol(n).longname = ['net mass convergence in area'];

n = n + 1;
defvol(n).name = 'sin';
defvol(n).unit = 'psu * Sv';
defvol(n).longname = ['net salt convergence in area'];

n = n + 1;
defvol(n).name = 's1in';
defvol(n).unit = 'psu * Sv';
defvol(n).longname = ['net salt convergence in area from surface down to ' num2str(lev1) ' m'];

n = n + 1;
defvol(n).name = 's2in';
defvol(n).unit = 'psu * Sv';
defvol(n).longname = ['net salt convergence in area from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];

n = n + 1;
defvol(n).name = 's3in';
defvol(n).unit = 'psu * Sv';
defvol(n).longname = ['net salt convergence in area from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];

n = n + 1;
defvol(n).name = 'hin';
defvol(n).unit = 'PW';
defvol(n).longname = ['net heat convergence in area'];

n = n + 1;
defvol(n).name = 'h1in';
defvol(n).unit = 'PW';
defvol(n).longname = ['net heat convergence in area from surface down to ' num2str(lev1) ' m'];

n = n + 1;
defvol(n).name = 'h2in';
defvol(n).unit = 'PW';
defvol(n).longname = ['net heat convergence in area from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];

n = n + 1;
defvol(n).name = 'h3in';
defvol(n).unit = 'PW';
defvol(n).longname = ['net heat convergence in area from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];

n = n + 1;
defvol(n).name = 'fin';
defvol(n).unit = 'mSv';
defvol(n).longname = ['net freshwater convergence in area'];

n = n + 1;
defvol(n).name = 'f1in';
defvol(n).unit = 'mSv';
defvol(n).longname = ['net freshwater convergence in area from surface down to ' num2str(lev1) ' m'];

n = n + 1;
defvol(n).name = 'f2in';
defvol(n).unit = 'mSv';
defvol(n).longname = ['net freshwater convergence in area from ' num2str(lev1) ' m down to ' num2str(lev2) ' m'];

n = n + 1;
defvol(n).name = 'f3in';
defvol(n).unit = 'mSv';
defvol(n).longname = ['net freshwater convergence in area from ' num2str(lev2) ' m down to ' num2str(lev3) ' m'];

basedir = fullfile(getenv('HOME'), '.pago');
save(fullfile(basedir, 'definition_indices_vol_3zlev.mat'), 'definition', 'defvol');

