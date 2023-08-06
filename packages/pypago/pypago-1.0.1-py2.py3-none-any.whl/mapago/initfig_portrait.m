function [] = initfig_portrait()
%INITFIG_PORTRAIT initialize portrait figure
%
% DESCRIPTION
% INITFIG_PORTRAIT initialize portrait figure
%
% EXAMPLES
%
%    initfig_portrait();
%
%   See also INITFIG_LANDSCAPE
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

set(gcf, 'Units', 'normalized');
set(gcf, 'position', [0.1 0.08, 0.5, 0.8])
set(gcf, 'PaperType', 'a4letter');
set(gcf, 'PaperUnits', 'normalized');
set(gcf, 'PaperPosition', [0.03, 0.03, 0.94, 0.93]);
set(gcf, 'PaperOrientation', 'portrait');
