function [b, n] = isint(x)
%ISINT Tests if an array is composed of integers.
%
%    B = ISINT(X) returns a boolean array B of the same size as X, with
%    each element equal to one if the corresponding element of X is an
%    integer, and zero otherwise.
%
%   See also ISINTEGER
%
% TODO beware license contamination
%
%Author: J.M. Lilly, 3/15/2001
%         software@jmlilly.net

resid = x - floor(real(x));
b = abs(resid) == 0;
