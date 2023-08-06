%SECTION_CORRECTIONS_ARCTIC
%
% DESCRIPTION
% SECTION_CORRECTIONS_ARCTIC built-in corrections for the Arctic sections
%
% EXAMPLES
%
%   SECTION_CORRECTIONS_ARCTIC
%
%   See also GRID_CORRECTIONS_ARCTIC
%
% TODO make a function
% TODO add attributes to NetCDF files
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO
switch model
    case 'GFDL'
        sections(1).dir = ['NE'];
        sections(3).i(1) = 316;
        sections(3).j(1) = 41;
        sections(3).i(2) = 276;
        sections(3).j(2) = 41;
    case 'CCSM'
        sections(1).j(end) = 67;
        sections(1).i(end) = 275;
        sections(2).i(1) = 299;
        sections(2).j(1) = 81;
        sections(2).i(end) = 245;
        sections(2).j(end) = 71;
        sections(2).dir = ['NE';'NW'];
        sections(3).dir = ['NW';'NW';'SW'];
        sections(4).j(end) = 102;
        sections(5).j(end) = 102;
        sections(5).i(1) = 117;
        sections(5).j(1) = 117;
        sections(6).i(1) = 42;
        sections(6).j(1) = 90;
        sections(4).dir = ['SE'];
        sections(5).dir = ['NE';'NE'];
    case 'IPSL'
        sections(1).j(end) = 14;
        sections(1).i(end) = 146;
        sections(3).i(1) = 157;
        sections(3).j(1) = 40;
        sections(3).i(2) = 140;
        sections(3).j(2) = 40;
        sections(6).dir = ['SE'];
        sections(7).dir = ['SW'];
    case 'CMCC'
        sections(1).i(end) = 146;
        sections(1).j(end) = 14;
        sections(3).i(1) = 157;
        sections(3).j(1) = 40;
        sections(3).i(2) = 140;
        sections(3).j(2) = 40;
        sections(6).dir = ['SE'];
        sections(7).dir = ['SW'];
    case 'CNRM'
        sections(3).i(end) = 83;
        sections(3).j(end) = 73;
        sections(6).dir = ['SE'];
        sections(7).dir = ['SW'];
        sections(5).dir = ['NW';'NW'];
    case 'ECEA'
        sections(3).i(end) = 93;
        sections(3).j(end) = 73;
        sections(6).dir = ['SE'];
        sections(7).dir = ['SW'];
        sections(5).dir = ['NW';'NW'];
    case 'MICO'
        sections(5).j(1) = 64;
        sections(5).dir = ['NE';'NE'];
        sections(4).dir = ['SE'];
        sections(3).dir = ['NW';'NW';'SW'];
    case 'MPIO'
        sections(3).dir = ['NW';'NW';'SW'];
        sections(4).dir = ['SE'];
        sections(5).dir = ['NE';'SE'];
        sections(6).dir = ['NE'];
        sections(7).dir = ['SE'];
end

