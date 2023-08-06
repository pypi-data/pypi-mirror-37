function [mean_volume] = yrave_volumes(MODEL_volume, leap, varargin)
%YRAVE_VOLUMES ponderates monthly indices by the exact length of each month
%
% DESCRIPTION
%
% ponderates monthly indices by the exact length of each month,
% hence use leap to specify how many days per month:
%
% * leap = 0 : fixed number of days per month and 365 days per year
% * leap = 1 : model knows leap years and used Gregorian Calendar - hence the first year must be specified as 3rd argument
% * leap = 2 : fixed number of days per month (30) and 360 days per year
%
% EXAMPLES
%
%   See also NANSUM SCRIPT_PAGO_CCSM SCRIPT_PAGO_CNRM SCRIPT_PAGO_GFDL SCRIPT_PAGO_IPSL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD --- version last modified on June, 27th 2012

if leap == 1
   if nargin == 1
        firstyr = varargin(1);
   else
        firstyr = input('model uses Gregorian Calendar - please specify which is the first year: ');
   end
end

fields = fieldnames(MODEL_volume);
nf = length(fields);

ns = length(MODEL_volume);

if isnan(MODEL_volume(1).time(1))
    t1 = 2;
else
    t1 = 1;
end
t2 = length(MODEL_volume(1).time);

ny = length(MODEL_volume(1).time(t1:t2))/12;
if ~isint(ny)
    error('JD yrave_indices : number of time steps not compatible with year average')
end
switch leap
    case 0
        ndays = reshape(repmat([31 28 31 30 31 30 31 31 30 31 30 31]', [1 ny]), 12 * ny, 1)';
    case 1
        i = 1;
        for yr=firstyr:firstyr + (ny - 1)
            for m=1:12
                ndays(i) = daysinmonth(yr, m, 1);
                i = i + 1;
            end
        end
    case 2
        ndays = 30 * ones(1, 12 * ny);

end

for s=1:ns
    for f=1:nf
        temp = MODEL_volume(s).(char(fields(f)));
        if size(temp, 1) ~= 1
            temp = temp';
        end
        if length(temp) == length(MODEL_volume(s).time)
            mean_volume(s).(char(fields(f))) = nansum(reshape(temp(t1:t2).*ndays, [12 ny]), 1)./nansum(reshape(~isnan(temp(t1:t2)).*ndays, [12 ny]), 1);
        else
            mean_volume(s).(char(fields(f))) = temp;
        end
    end
    mean_volume(s).name = MODEL_volume(s).name;
    mean_volume(s).time = floor(MODEL_volume(s).time(t1:12:t2)/360);
    if MODEL_volume(s).time(t1 + 1) - MODEL_volume(s).time(t1) == 1  % hence MODEL_volume.time is given in months
        mean_volume(s).time = floor(MODEL_volume(s).time(t1:12:t2)/12);  % time index for mean volume given in years
    else % we assume here that MODEL_volume.time is given in days
        mean_volume(s).time = floor(MODEL_volume(s).time(t1:12:t2)/360); % time index for mean volume given in years
    end

end
