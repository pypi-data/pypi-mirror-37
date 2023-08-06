function [finalfaces, finalveci, finalvecj, finalorient, corner] = conseclr2(veci1, vecj1, faces1, orient1, veci2, vecj2, faces2, orient2, corner)
%
% DESCRIPTION
% this function ensures the connection between consecutive segments of a section
%
% EXAMPLE
% function to be called by conseclr only - not to be used independently
%
%   See also CONSEC
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

if strcmp(faces1(end), 'N')  % vec1 ends with a north face

    if strcmp(faces2(1), 'N')  % vec2 starts with a north face
        veci2 = veci2(2:end);
        vecj2 = vecj2(2:end);
        faces2 = faces2(2:end);
        orient2 = orient2(2:end);
        if veci1(end - 1) <= veci1(end)
            if veci2(1) <= veci1(end)
                veci1 = veci1(1:end - 1);
                vecj1 = vecj1(1:end - 1);
                faces1 = faces1(1:end - 1);
                orient1 = orient1(1:end - 1);
                corner(end) = corner(end) - 1;
            end
            while veci2(1) == veci1(end) & vecj2(1) == vecj1(end)
                veci2 = veci2(2:end);
                vecj2 = vecj2(2:end);
                faces2 = faces2(2:end);
                orient2 = orient2(2:end);
                veci1 = veci1(1:end - 1);
                vecj1 = vecj1(1:end - 1);
                faces1 = faces1(1:end - 1);
                orient1 = orient1(1:end - 1);
                corner(end) = corner(end) - 1;
            end
        else
            if veci2(1) >= veci1(end)
               veci1 = veci1(1:end - 1);
               vecj1 = vecj1(1:end - 1);
                faces1 = faces1(1:end - 1);
                orient1 = orient1(1:end - 1);
                corner(end) = corner(end) - 1;
            end
            while veci2(1) == veci1(end) & vecj2(1) == vecj1(end)
                veci2 = veci2(2:end);
                vecj2 = vecj2(2:end);
                faces2 = faces2(2:end);
                orient2 = orient2(2:end);
                veci1 = veci1(1:end - 1);
                vecj1 = vecj1(1:end - 1);
                faces1 = faces1(1:end - 1);
                orient1 = orient1(1:end - 1);
                corner(end) = corner(end) - 1;
            end
        end
    else % vec2 starts with a west face
        if strcmp(faces2(2), 'N') & veci2(2) == veci2(1) & vecj2(2) == vecj2(1) % vec2 starts with a west face then a north face at the same point
            veci2 = veci2(3:end);
            vecj2 = vecj2(3:end);
            faces2 = faces2(3:end);
            orient2 = orient2(3:end);
        else % vec2 starts with a west face then west face again (to the north or to the south)
            veci1 = veci1(1:end - 1);
            vecj1 = vecj1(1:end - 1);
            faces1 = faces1(1:end - 1);
            orient1 = orient1(1:end - 1);
            corner(end) = corner(end) - 1;
            if vecj2(2) > vecj2(1)
                veci2 = veci2(2:end);
                vecj2 = vecj2(2:end);
                faces2 = faces2(2:end);
                orient2 = orient2(2:end);
            end
            while veci1(end) == veci2(1) && vecj1(end) == vecj2(1)
                veci1 = veci1(1:end - 1);
                vecj1 = vecj1(1:end - 1);
                faces1 = faces1(1:end - 1);
                orient1 = orient1(1:end - 1);
                corner(end) = corner(end) - 1;
                veci2 = veci2(2:end);
                vecj2 = vecj2(2:end);
                faces2 = faces2(2:end);
                orient2 = orient2(2:end);
            end
        end
    end
else
    if veci1(end) == veci2(1) && vecj1(end) == vecj2(1)
        veci1 = veci1(1:end - 1);
        vecj1 = vecj1(1:end - 1);
        faces1 = faces1(1:end - 1);
        orient1 = orient1(1:end - 1);
        corner(end) = corner(end) - 1;
    end
end

finalveci = [veci1 veci2];
finalvecj = [vecj1 vecj2];
finalfaces = [faces1; faces2];
finalorient = [orient1 orient2];
