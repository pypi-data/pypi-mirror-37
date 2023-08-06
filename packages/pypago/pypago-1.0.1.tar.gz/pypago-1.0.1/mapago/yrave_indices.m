function [mean_indices] = yrave_indices(MODEL_indices, leap, varargin)
%YRAVE_INDICES ponderates monthly indices by the exact length of each month
%
% DESCRIPTION
%
% ponderates monthly indices by the exact length of each month,
% hence use leap to specify how many days per month:
%
% * leap = 0 : fixed number of days per month and 365 days per year
% * leap = 1 : model knows leap years and uses Gregorian Calendar - hence the first year must be specified as 3rd argument
% * leap = 2 : fixed number of days per month (30) and 360 days per year
%
% EXAMPLES
%
%   See also NANSUM, script_PAGO_CCSM
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- version last modified on June, 27th 2012

if leap == 1
    if nargin == 1
        firstyr = varargin(1);
    else
        firstyr = input('model uses Gregorian Calendar - please specify which is the first year: ');
    end
end

fields = fieldnames(MODEL_indices);
nf = length(fields);

ns = length(MODEL_indices);

if isnan(MODEL_indices(1).time(1))
    t1 = 2;
else
    t1 = 1;
end
t2 = length(MODEL_indices(1).time);

ny = length(MODEL_indices(1).time(t1:t2))/12;
if ~isint(ny)
    error('JD PAGO error in yrave_indices : number of time steps not compatible with year average')
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
    mean_indices(s).name = MODEL_indices(s).name;
    if MODEL_indices(s).time(t1 + 1) - MODEL_indices(s).time(t1) == 1   % hence MODEL_indices.time is given in months
        mean_indices(s).time = floor(MODEL_indices(s).time(t1:12:t2)/12);  % time index for mean indices given in years
    else % we assume here that MODEL_indices.time is given in days
        mean_indices(s).time = floor(MODEL_indices(s).time(t1:12:t2)/360); % time index for mean indices given in years
    end
    for f=3:nf
        temp = MODEL_indices(s).(char(fields(f)));
        if not(isempty(temp))
            if size(temp, 1) == 1
                mean_indices(s).(char(fields(f))) = nansum(reshape(temp(t1:t2).*ndays, [12 ny]), 1)./nansum(reshape(~isnan(temp(t1:t2)).*ndays, [12 ny]), 1);
            else
                mean_indices(s).(char(fields(f))) = squeeze(nansum(reshape(temp(t1:t2, :).*repmat(ndays', 1, size(temp, 2)), [12 ny size(temp, 2)]), 1)./nansum(reshape(~isnan(temp(t1:t2, :)).*repmat(ndays', 1, size(temp, 2)), [12 ny size(temp, 2)]), 1));
            end
        end
    end
end
