function [rep] = JDinputbin(question)
%JDINPUTBIN
%
% DESCRIPTION
%
% EXAMPLES
%
%   question = 'save data? (0 or 1)';
%   rep = JDinputbin(question);
%
%   See also INPUT
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

rep = input(question);
if rep == 0 || rep == 1
else
   disp('please answer 0 for no and 1 for yes')
   rep = JDinputbin(question);
end
