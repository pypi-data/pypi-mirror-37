function [] = loaddata_CCSM(structfile, file_location, file_prefix, file_suffix)
%LOADDATA_CCSM
%
% DESCRIPTION
% LOADDATA_CCSM extracts the model output, interpolates if needed on
% west and north faces, and saves
% only the data along preselected sections and areas in structfile.
%
% file_location is where the model output can be found (full path), which name is
% {file_prefix}{SALT, TEMP, UVEL, VVEL}.file_suffix.nc
%
% EXAMPLES
%
%   See also <https://sourcesup.renater.fr/pago/models.html>, NANSUM
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- last modified on May, 15th 2012

disp('enter full path to nc file that contains all information')
gridfile = input('about the model grid (scale factors, bathymetry, mask...): ', 's');

load(structfile)

% checks that all files can be found

vart = 'TEMP';
file = [file_location, file_prefix, vart, '.', file_suffix, '.nc'];  % at tracer cell center, ie lont and latt
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_CCSM: cannot find file: ' file ])
end

time = readnc(file, 'time'); % in days
nz = length(readnc(file, 'dz'));

vars = 'SALT';
file = [file_location, file_prefix, vars, '.', file_suffix, '.nc'];  % at tracer cell center, ie lont and latt
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_CCSM: cannot find file: ' file ])
end

varu = 'UVEL';
file = [file_location, file_prefix, varu, '.', file_suffix, '.nc'];  % at north west of tracer cell
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_CCSM: cannot find file: ' file ])
end

varv = 'VVEL';
file = [file_location, file_prefix, varv, '.', file_suffix, '.nc'];  % at north west of tracer cell
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_CCSM: cannot find file: ' file ])
end

% get scale factors for interpolation of the velocities

temp = readnc(gridfile, 'DXU');
[nlat, nlon] = size(temp);
dyu = 1e-2 * readnc_wrap(gridfile, 'DYU', [MODEL_grid.lats-1 MODEL_grid.lonw], [MODEL_grid.latn MODEL_grid.lone + 1], nlon); % originally in centimeters, at northwest corner of cell >> convert to meters
dxu = 1e-2 * readnc_wrap(gridfile, 'DXU', [MODEL_grid.lats-1 MODEL_grid.lonw], [MODEL_grid.latn MODEL_grid.lone + 1], nlon);% originally in centimeters, at northwest corner of cell >> convert to meteters

dz = 1e-2 * readnc(gridfile, 'dz', [1], [nz], [1]); % originally in centimeters >> convert to meters
dzu = repmat(dz, [1 size(dyu, 1) size(dyu, 2)]);
dzv = repmat(dz, [1 size(dxu, 1) size(dxu, 2)]);

dxu3D = repmat(reshape(dxu, [1 size(dxu, 1) size(dxu, 2)]), [nz 1 1]);
dyu3D = repmat(reshape(dyu, [1 size(dyu, 1) size(dyu, 2)]), [nz 1 1]);

% get data over the selected region
for t=1:length(time)

    MODEL_time = cat(1, MODEL_time, time(t));
    disp(['loading data from day ' num2str(time(t))])

    file = [file_location, file_prefix, vars, '.', file_suffix, '.nc'];  % at tracer cell center, ie lont and latt
    if MODEL_grid.latn<nlat
        sc = readnc_wrap(file, 'SALT', [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn + 1, MODEL_grid.lone], nlon);
    else
        sc = readnc_wrap(file, 'SALT', [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn, MODEL_grid.lone], nlon);
        sc = cat(2, NaN * ones(nz, 1, size(sc, 3)), sc);
    end
    sn = nansum(cat(4, sc(:, 1:(end - 1), 2:end), sc(:, 2:end, 2:end)), 4)./nansum(cat(4, ~isnan(sc(:, 1:(end - 1), 2:end)), ~isnan(sc(:, 2:end, 2:end))), 4);
    sw = nansum(cat(4, sc(:, 1:(end - 1), 1:(end - 1)), sc(:, 1:(end - 1), 2:end)), 4)./nansum(cat(4, ~isnan(sc(:, 1:(end - 1), 1:(end - 1))), ~isnan(sc(:, 1:(end - 1), 2:end))), 4);
    sc = sc(:, 1:(end - 1), 2:end);

    file = [file_location, file_prefix, vart, '.', file_suffix, '.nc'];  % at tracer cell center, ie lont and latt
    if MODEL_grid.latn<nlat
        tc = readnc_wrap(file, 'TEMP', [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn + 1, MODEL_grid.lone], nlon);
    else
        tc = readnc_wrap(file, 'TEMP', [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn, MODEL_grid.lone], nlon);
        tc = cat(2, NaN * ones(nz, 1, size(tc, 3)), tc);
    end
    tn = nansum(cat(4, tc(:, 1:(end - 1), 2:end), tc(:, 2:end, 2:end)), 4)./nansum(cat(4, ~isnan(tc(:, 1:(end - 1), 2:end)), ~isnan(tc(:, 2:end, 2:end))), 4);
    tw = nansum(cat(4, tc(:, 1:(end - 1), 1:(end - 1)), tc(:, 1:(end - 1), 2:end)), 4)./nansum(cat(4, ~isnan(tc(:, 1:(end - 1), 1:(end - 1))), ~isnan(tc(:, 1:(end - 1), 2:end))), 4);
    tc = tc(:, 1:(end - 1), 2:end);

    file = [file_location, file_prefix, varu, '.', file_suffix, '.nc'];  % originally in centimeters/s >> convert to meters/s
    unw = 1e-2 * readnc_wrap(file, 'UVEL', [t, 1, MODEL_grid.lats-1, MODEL_grid.lonw], [t, nz, MODEL_grid.latn, MODEL_grid.lone + 1], nlon);

    file = [file_location, file_prefix, varv, '.', file_suffix, '.nc'];  % originally in centimeters/s >> convert to meters/s
    vnw = 1e-2 * readnc_wrap(file, 'VVEL', [t, 1, MODEL_grid.lats - 1, MODEL_grid.lonw], [t, nz, MODEL_grid.latn, MODEL_grid.lone + 1], nlon);

    % we calculate the exact transport through each corner then split in two
    % to the center of each adjacent faces
    transw = .5 * squeeze(nansum(cat(4, unw(:, 1:(end - 1), 1:(end - 1)).*dzu(:, 1:(end - 1), 1:(end - 1)).*dyu3D(:, 1:(end - 1), 1:(end - 1)), unw(:, 2:end, 1:(end - 1)).*dzu(:, 2:end, 1:(end - 1)).*dyu3D(:, 2:end, 1:(end - 1))), 4));
    transn = .5*nansum(cat(4, vnw(:, 2:end, 1:(end - 1)).*dzv(:, 2:end, 1:(end - 1)).*dxu3D(:, 2:end, 1:(end - 1)), vnw(:, 2:end, 2:end).*dzv(:, 2:end, 2:end).*dxu3D(:, 2:end, 2:end)), 4);

    % get temperature, salinity and velocity along sections
    for sec=1:length(MODEL_sections)

        clear vect vecs vecv

        veci = MODEL_sections(sec).veci;
        vecj = MODEL_sections(sec).vecj;
        faces = MODEL_sections(sec).faces;
        orient = MODEL_sections(sec).orient;

        nl = length(MODEL_sections(sec).veci);
        for l=1:nl
            switch faces(l)
                case 'N'
                    vect(:, l) = tn(:, vecj(l), veci(l));
                    vecs(:, l) = sn(:, vecj(l), veci(l));
                    vecv(:, l) = transn(:, vecj(l), veci(l)) * orient(l)./MODEL_sections(sec).areavect(:, l);
                case 'W'
                    vect(:, l) = tw(:, vecj(l), veci(l));
                    vecs(:, l) = sw(:, vecj(l), veci(l));
                    vecv(:, l) = transw(:, vecj(l), veci(l)) * orient(l)./MODEL_sections(sec).areavect(:, l);
            end
        end

        % the interpolation from the center of the cells to the faces is such
        % that it creates temperatures and salinities in land. here we force these
        % values to NaN
        vect(find(vecv == 0)) = NaN;
        vecs(find(vecv == 0)) = NaN;

        MODEL_sections(sec).vect = cat(1, MODEL_sections(sec).vect, reshape(vect, [1 nz nl]));
        MODEL_sections(sec).vecs = cat(1, MODEL_sections(sec).vecs, reshape(vecs, [1 nz nl]));
        MODEL_sections(sec).vecv = cat(1, MODEL_sections(sec).vecv, reshape(vecv, [1 nz nl]));
    end

    % get temperature, salinity on each grid point of areas
    if exist('MODEL_area', 'var')
        for area=1:length(MODEL_area)
            clear salinity temperature
            for z=1:nz
                salinity(z, :) = diag(squeeze(sc(z, MODEL_area(area).indj, MODEL_area(area).indi)));
                temperature(z, :) = diag(squeeze(tc(z, MODEL_area(area).indj, MODEL_area(area).indi)));
            end
            MODEL_area(area).salinity = cat(1, MODEL_area(area).salinity, reshape(salinity, [1, nz, length(MODEL_area(area).indi)]));
            MODEL_area(area).temperature = cat(1, MODEL_area(area).temperature, reshape(temperature, [1, nz, length(MODEL_area(area).indi)]));
        end
    end
end

% save new structfile
if exist('MODEL_area', 'var')
    save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_area', 'MODEL_time');
else
    save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_time');
end
