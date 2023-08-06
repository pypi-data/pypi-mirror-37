function [finalfaces, finalveci,finalvecj,finalorient,corner] = consec(veci1,vecj1,faces1,orient1,veci2,vecj2,faces2,orient2,corner)
%CONSEC
%
% DESCRIPTION
%
% EXAMPLES
%
%   See also SECTIONS_MODEL
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

if isempty(find(veci2 > veci1(end - 1)))
    if length(corner) > 1
        corner(end) = corner(end - 1) + length(veci2);
    else
        corner = length(veci2);
    end
    [faces, veci, vecj, orient, corner] = conseclr2(fliplr(veci2), fliplr(vecj2), flipud(faces2), fliplr(orient2), fliplr(veci1), fliplr(vecj1), flipud(faces1), fliplr(orient1), corner);
    finalfaces = flipud(faces);
    finalveci = fliplr(veci);
    finalvecj = fliplr(vecj);
    finalorient = fliplr(orient);
else
    [finalfaces, finalveci, finalvecj, finalorient, corner] = conseclr2(veci1, vecj1, faces1, orient1, veci2, vecj2, faces2, orient2, corner);
end
