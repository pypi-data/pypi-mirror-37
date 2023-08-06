% predefined grid for the North Atlantic
%
% DESCRIPTION
% GRID_CORRECTIONS_NA
%
% EXAMPLES
%
%   See also GRID_CORRECTIONS_ARCTIC
%
% TODO make a function
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

switch model
        case 'GFDL'
                MODEL_grid.lonw = 197;
                MODEL_grid.lone = 310;
                MODEL_grid.lats = 135;
                MODEL_grid.latn = 197;
        case {'CNRM', 'ECEA'}
                MODEL_grid.lonw = 205;
                MODEL_grid.lone = 318;
                MODEL_grid.lats = 186;
                MODEL_grid.latn = 280;
        case 'IPSL'
                MODEL_grid.lonw = 95;
                MODEL_grid.lone = 150;
                MODEL_grid.lats = 85;
                MODEL_grid.latn = 143;
        case 'CMCC'
                MODEL_grid.lonw = 100;
                MODEL_grid.lone = 160;
                MODEL_grid.lats = 92;
                MODEL_grid.latn = 145;
        case 'CCSM'
                MODEL_grid.lonw = 281;
                MODEL_grid.lone = 105;
                MODEL_grid.lats = 267;
                MODEL_grid.latn = 384;
        case 'RCHB'
                MODEL_grid.lonw = 25;
                MODEL_grid.lone = 130;
                MODEL_grid.lats = 100;
                MODEL_grid.latn = 159;
        case 'MICO'
                MODEL_grid.lonw = 275;
                MODEL_grid.lone = 108;
                MODEL_grid.lats = 265;
                MODEL_grid.latn = 383;
        case 'MPIO'
                MODEL_grid.lonw = 60;
                MODEL_grid.lone = 230;
                MODEL_grid.lats = 115;
                MODEL_grid.latn = 219;
end
