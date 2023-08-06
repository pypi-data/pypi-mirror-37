%SECTION_CORRECTIONS_NA
%
% DESCRIPTION
% SECTION_CORRECTIONS_NA built-in corrections for the North Atlantic sections
%
% EXAMPLES
%
%   SECTION_CORRECTIONS_NA
%
%   See also GRID_CORRECTIONS_NA
%
% TODO make a function
% TODO add attributes to NetCDF files
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO
switch model
    case 'GFDL'
    case 'CCSM'
        sections(1).i(1) = 27;
        sections(1).j(1) = 56;
        sections(2).i(1) = 37;
        sections(2).j(1) = 92;
        sections(4).j(end) = 102;
        sections(5).j(end) = 102;
        sections(5).i(1) = 117;
        sections(5).j(1) = 117;
        sections(7).i(1) = 11;
        sections(7).j(1) = 90;
        sections(15).i(1) = 4;
        sections(4).dir = ['SE'];
        sections(5).dir = ['NE';'NE'];
    case 'IPSL'
        sections(6).dir = ['NE';'NW'];
        sections(7).dir = ['SE'];
        sections(8).dir = ['SW'];
        sections(11).i(1) = sections(11).i(1) + 1;
    case 'CMCC'
        sections(15).j(1) = 5;
        sections(15).i(1) = 2;
        sections(15).dir = ['NE'];
        sections(7).dir = ['SE'];
        sections(8).dir = ['SW'];
    case 'CNRM'
        sections(1).i(1) = 31;
        sections(1).j(1) = 32;
        sections(12).i(1) = 76;
        sections(12).j(1) = 42;
        sections(7).dir = ['SE'];
        sections(8).dir = ['SW'];
        sections(6).dir = ['NE';'NW'];
        sections(5).dir = ['NW';'NW'];
    case 'ECEA'
        sections(1).i(1) = 31;
        sections(1).j(1) = 32;
        sections(10).i(2) = 75;
        sections(10).j(2) = 55;
        sections(11).i(1) = 75;
        sections(11).j(1) = 55;
        sections(12).i(1) = 76;
        sections(12).j(1) = 42;
        sections(7).dir = ['SE'];
        sections(8).dir = ['SW'];
        sections(6).dir = ['NE';'NW'];
        sections(5).dir = ['NW';'NW'];
    case 'RCHB'
        sections(1).i(1) = 32;
        sections(1).j(1) = 29;
        sections(11).i(2) = 82;
        sections(11).j(2) = 39;
        sections(13).i(1) = 83;
        sections(13).j(1) = 38;
        sections(13).i(2) = 94;
        sections(13).j(2) = 43;
%    case 'MICO' % previous version of MICOM as used in BCM
%        sections(15).j(1) = 6;
%        sections(15).j(2) = 6;
%        sections(15).dir = ['NE'];
%        sections(14).dir = ['NW';'NE';'NW'];
%        sections(2).dir = ['NW'];
%        sections(5).dir = ['NW';'SW'];
%        sections(6).dir = ['NW';'NW'];
%        sections(10).dir = ['NW'];
    case 'MICO'
        sections(5).j(1) = 119;
        sections(5).dir = ['NE';'NE'];
        sections(4).dir = ['SE'];
    case 'MPIO'
        sections(4).dir = ['SE'];
        sections(5).dir = ['NE';'SE'];
        sections(6).dir = ['SE';'NE'];
        sections(10).j(2) = 55;
        sections(10).i(2) = 103;
        sections(11).j(2) = 55;
        sections(11).i(2) = 103;
        sections(11).dir = ['SE'];
end
