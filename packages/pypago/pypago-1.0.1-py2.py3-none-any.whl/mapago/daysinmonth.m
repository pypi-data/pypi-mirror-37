function [dim] = daysinmonth(year, month, leap)
%DAYSINMONTH returns the number of days in a given month and year.
%
% DESCRIPTION
% DAYSINMONTH returns the number of days in a given month and year.
%
% * leap = 0 : fixed number of days per month and 365 days per year
% * leap = 1 : uses Gregorian Calendar
% * leap = 2 : fixed number of days per month (30)
%
%   Examples
%
%    % days in mont February 2012 if no leap calendar ?
%    year = 2012;
%    month = 2;
%    leap = 0;
%    dim = daysinmonth(year, month, leap);
%    dim
%
%    % days in mont February 2012 if leap calendar ?
%    year = 2012;
%    month = 2;
%    leap = 1;
%    dim = daysinmonth(year, month, leap);
%    dim
%
%    % days in mont February 2012 if fixed number of days per month (30) ?
%    year = 2012;
%    month = 2;
%    leap = 2;
%    dim = daysinmonth(year, month, leap);
%    dim
%
%   See also ISLEAP
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

days = [31 28 31 30 31 30 31 31 30 31 30 31];
switch leap
    case 0
        dim = days(month);
    case 1
        dim = days(month) + ( month == 2 & isleap(year) );
    case 2
        dim = 30;
end
