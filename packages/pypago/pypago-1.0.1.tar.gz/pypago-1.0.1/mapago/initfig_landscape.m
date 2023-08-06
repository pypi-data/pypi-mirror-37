function [] = initfig_landscape()
%INITFIG_LANDSCAPE initialize landscape figure
%
% DESCRIPTION
% INITFIG_LANDSCAPE initialize landscape figure
%
% EXAMPLES
%
%   initfig_landscape();
%
%   See also INITFIG_PORTRAIT
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO
%

% JD PAGO WHOI

set(gcf, 'Units', 'normalized');
set(gcf, 'position', [0.1 0.08, 0.5, 0.8])
set(gcf, 'PaperType', 'a4letter');
set(gcf, 'PaperUnits', 'normalized');
set(gcf, 'PaperPosition', [0.03, 0.03, 0.94, 0.93]);
set(gcf, 'PaperOrientation', 'landscape');
