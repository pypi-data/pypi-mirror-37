function [faces, newveci, newvecj, orientation] = facesinsec(veci, vecj, dir)
%FACESINSEC
%
% DESCRIPTION
% by convention, we tend to favor the north and west side of each grid cell
% as a "face" of a sequence of gridpoints.
%
% veci and vecj are reconstructed to i) drop the points which faces are not
% used, and ii) double the grid points which faces are used twice.
%
% faces is a vector of letters:
% * N means that the north face is to be used
% * W means that the west face is to be used
%
% orientation is a vector of +1 or -1 that shall be applied to velocities
% in order to make sure that the transport is integrated in the direction
% dir, which is a two letter vector: NE, NW, SE or SW. Calculation assumes that
% vectors are originally pointing toward N or E.
%
% EXAMPLES
%
%   See also AREAINSEC, LENGTHINSEC
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO
%
% JD PAGO WHOI

if length(veci) == 1
    error('Warning from facesinsec.m (JD): only one point in sequence >> no face should be used')
end

% make sure that veci and vecj are of dimension [1, n]
[a, b] = size(veci);
if a > b
    veci = veci';
end
[a, b] = size(vecj);
if a > b
    vecj = vecj';
end

% make sure that veci and vecj are monotonous
if ~monotonous(veci)
    error('Warning from facesinsec.m (JD): sequence veci must be monotonous')
end

if ~monotonous(vecj)
    error('Warning from facesinsec.m (JD): sequence vecj must be monotonous')
end

if veci(end) == veci(1)
    newveci = veci;
    newvecj = vecj;
    faces = repmat('W', [length(newveci), 1]);
else

    % eventually change direction of both sequences in order to get veci from
    % left to right
    changedir = 0;
    if veci(end) < veci(1)
        veci = flipdim(veci, 2);
        vecj = flipdim(vecj, 2);
        changedir = 1;
    end

    indvec = 1;
    newveci = veci(indvec);
    newvecj = vecj(indvec);
    if vecj(indvec + 1) == vecj(indvec)
        faces = ['N'];
    else
        faces = ['W'];
    end
    indvec = indvec + 1;

    while indvec + 1 <= length(veci)
        if veci(indvec) == veci(indvec - 1)
            if vecj(indvec) > vecj(indvec - 1)
                newveci = [newveci veci(indvec)];
                newvecj = [newvecj vecj(indvec)];
                faces = [faces;'W'];
                if veci(indvec + 1) > veci(indvec)
                    newveci = [newveci veci(indvec)];
                    newvecj = [newvecj vecj(indvec)];
                    faces = [faces;'N'];
                end
            else %vecj(indvec) < vecj(indvec - 1)
                newveci = [newveci veci(indvec)];
                newvecj = [newvecj vecj(indvec)];
                if veci(indvec + 1) > veci(indvec)
                    faces = [faces;'N'];
                else
                    faces = [faces;'W'];
                end
            end
        else
            if veci(indvec + 1) == veci(indvec)
                % if vecj(indvec) > vecj(indvec) do nothing
                if vecj(indvec + 1) < vecj(indvec)
                    newveci = [newveci veci(indvec)];
                    newvecj = [newvecj vecj(indvec)];
                    faces = [faces;'W'];
                end
            else
                newveci = [newveci veci(indvec)];
                newvecj = [newvecj vecj(indvec)];
                faces = [faces;'N'];
            end
        end
        indvec = indvec + 1;
    end

    %when indvec == length(veci)
    % note that new sequence ends with N
    if veci(indvec) == veci(indvec - 1)
        newveci = [newveci veci(indvec)];
        newvecj = [newvecj vecj(indvec)];
        if vecj(indvec) > vecj(indvec - 1)
            newveci = [newveci veci(indvec)];
            newvecj = [newvecj vecj(indvec)];
            faces = [faces;'W';'N'];
        else
            faces = [faces;'N'];
        end
    else
        newveci = [newveci veci(indvec)];
        newvecj = [newvecj vecj(indvec)];
        faces = [faces;'N'];
    end

    if changedir == 1
        newveci = fliplr(newveci);
        newvecj = fliplr(newvecj);
        faces = flipud(faces);
    end
end

orientation = zeros(1, length(newveci));
for l=1:length(newveci)
    switch faces(l)
        case 'W'
            switch dir(2)
                case 'W'
                    orientation(l) = -1;
                case 'E'
                    orientation(l) = 1;
            end
        case 'N'
            switch dir(1)
                case 'N'
                    orientation(l) = 1;
                case 'S'
                    orientation(l) = -1;
            end
    end
end
