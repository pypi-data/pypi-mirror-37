% predefined grid for the North Atlantic
%
% DESCRIPTION
% GRID_CORRECTIONS_ARCTIC
%
% EXAMPLES
%
%   See also GRID_CORRECTIONS_NA
%
% TODO make a function
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

switch model
        case 'GFDL'
                MODEL_grid.lonw = 181;
                MODEL_grid.lone = 180;
                MODEL_grid.lats = 160;
                MODEL_grid.latn = 200;
        case 'CNRM'
                MODEL_grid.lonw = 50;
                MODEL_grid.lone = 318;
                MODEL_grid.lats = 220;
                MODEL_grid.latn = 292;
        case 'ECEA'
                MODEL_grid.lonw = 40;
                MODEL_grid.lone = 322;
                MODEL_grid.lats = 220;
                MODEL_grid.latn = 292;
        case 'IPSL'
                MODEL_grid.lonw = 95;
                MODEL_grid.lone = 80;
                MODEL_grid.lats = 110;
                MODEL_grid.latn = 149;
        case 'CMCC'
                MODEL_grid.lonw = 95;
                MODEL_grid.lone = 94;
                MODEL_grid.lats = 110;
                MODEL_grid.latn = 149;
        case 'CCSM'
                MODEL_grid.lonw = 250;
                MODEL_grid.lone = 249;
                MODEL_grid.lats = 267;
                MODEL_grid.latn = 384;
        case 'RCHB'
                MODEL_grid.lonw = 25;
                MODEL_grid.lone = 130;
                MODEL_grid.lats = 100;
                MODEL_grid.latn = 159;
        case 'MICO'
                MODEL_grid.lonw = 275;
                MODEL_grid.lone = 274;
                MODEL_grid.lats = 320;
                MODEL_grid.latn = 383;
        case 'MPIO'
                MODEL_grid.lonw = 230;
                MODEL_grid.lone = 229;
                MODEL_grid.lats = 115;
                MODEL_grid.latn = 219;
end
