function [secplot] = findsecnum(MODEL_sections, secplotname)
%FINDSECNUM determines the index of a section in a list of sections
%
% DESCRIPTION
%
% FINDSECNUM determines the index of a section in a list of sections
%
% EXAMPLES
%
%   See also CREATE_NETCDF_SEC INDICES_MODEL SECTIONS_MODEL VOLUMES_MODEL
%
%
% TODO hide this function from end-users
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

secplot = 0;
for s=1:length(MODEL_sections)
    if MODEL_sections(s).name == secplotname
        secplot = s;
    end
end
if secplot == 0
    error(['JD PAGO error: section ' secplotname ' does not exist'])
end
