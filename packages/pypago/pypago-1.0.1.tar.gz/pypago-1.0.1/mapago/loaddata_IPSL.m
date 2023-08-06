function[] = loaddata_IPSL(structfile, file_location, file_prefix, file_suffix)
%LOADDATA_IPSL
%
% DESCRIPTION
% LOADDATA_IPSL extracts the model output, interpolates if needed
% on west and north faces,
% and saves only the data along preselected sections and areas in structfile.
%
% file_location is where the model output can be found (full path), which name is
% {variable}/{variable}_{file_prefix}_{file_suffix}.nc
%
% EXAMPLES
%
%   See also <https://sourcesup.renater.fr/pago/models.html>, NANSUM
%
% TODO
% hardcoded directory separator
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- last modified on September, 14th 2012

load(structfile);

% checks that all files can be found

vart = 'thetao';
file = [file_location, vart, '/', vart, '_', file_prefix, '_', file_suffix, '.nc'];
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_IPSL: cannot find file: ' file ])
end

nz = size(MODEL_sections(1).depthvect, 1);
time = readnc(file, 'time');
[ny, nx] = size(readnc(file, 'lon'));

vars = 'so';
file = [file_location, vars, '/', vars, '_', file_prefix, '_', file_suffix, '.nc'];
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_IPSL: cannot find file: ' file ])
end

varu = 'uo';
file = [file_location, varu, '/', varu, '_', file_prefix, '_', file_suffix, '.nc'];
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_IPSL: cannot find file: ' file ])
end

varv = 'vo';
file = [file_location, varv, '/', varv, '_', file_prefix, '_', file_suffix, '.nc'];
if ~exist(file, 'file')
    error(['JD PAGO error in loaddata_IPSL: cannot find file: ' file ])
end

% get data over the selected region
for t = 1:length(time)

    MODEL_time = cat(1, MODEL_time, time(t));
    disp(['loading data from day ' num2str(time(t))]) % warning : IPSL unformatted model output may give time in seconds rather than day

    file = [file_location, vars, '/', vars, '_', file_prefix, '_', file_suffix, '.nc'];  % at tracer cell center, ie lont and latt, in PSU
    sc = readnc_wrap(file, vars, [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn + 1, MODEL_grid.lone], nx);
    % replace supposed missing values with NaN
    sc(find(abs(sc) > 100)) = NaN;
    sc(find(sc == 0)) = NaN;
    % interpolate to the faces
    sn = nansum(cat(4, sc(:, 1:(end - 1), 2:end), sc(:, 2:end, 2:end)), 4)./nansum(cat(4, ~isnan(sc(:, 1:(end - 1), 2:end)), ~isnan(sc(:, 2:end, 2:end))), 4);
    sw = nansum(cat(4, sc(:, 1:(end - 1), 1:(end - 1)), sc(:, 1:(end - 1), 2:end)), 4)./nansum(cat(4, ~isnan(sc(:, 1:(end - 1), 1:(end - 1))), ~isnan(sc(:, 1:(end - 1), 2:end))), 4);
    sc = sc(:, 1:(end - 1), 2:end);

    file = [file_location, vart, '/', vart, '_', file_prefix, '_', file_suffix, '.nc'];  % at tracer cell center, ie lont and latt, in K
    tc = readnc_wrap(file, vart, [t, 1, MODEL_grid.lats, (MODEL_grid.lonw - 1)], [t, nz, MODEL_grid.latn + 1, MODEL_grid.lone], nx) - 273.15;
    % replace supposed missing values with NaN
    tc(find(abs(tc) > 100)) = NaN;
    tc(find(tc == 0)) = NaN;
    % interpolate to the faces
    tn = nansum(cat(4, tc(:, 1:(end - 1), 2:end), tc(:, 2:end, 2:end)), 4)./nansum(cat(4, ~isnan(tc(:, 1:(end - 1), 2:end)), ~isnan(tc(:, 2:end, 2:end))), 4);
    tw = nansum(cat(4, tc(:, 1:(end - 1), 1:(end - 1)), tc(:, 1:(end - 1), 2:end)), 4)./nansum(cat(4, ~isnan(tc(:, 1:(end - 1), 1:(end - 1))), ~isnan(tc(:, 1:(end - 1), 2:end))), 4);
    tc = tc(:, 1:(end - 1), 2:end);

    file = [file_location, varu, '/', varu, '_', file_prefix, '_', file_suffix, '.nc'];  % zonal current at middle of eastern face, in m/s
    uw = readnc_wrap(file, varu, [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn, MODEL_grid.lone - 1], nx);

    file = [file_location, varv, '/', varv, '_', file_prefix, '_', file_suffix, '.nc'];  % meridional current at middle of northern face, in m/s
    vn = readnc_wrap(file, varv, [t, 1, MODEL_grid.lats, MODEL_grid.lonw], [t, nz, MODEL_grid.latn, MODEL_grid.lone], nx);

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
                    vecv(:, l) = vn(:, vecj(l), veci(l)) * orient(l);
                case 'W'
                    vect(:, l) = tw(:, vecj(l), veci(l));
                    vecs(:, l) = sw(:, vecj(l), veci(l));
                    vecv(:, l) = uw(:, vecj(l), veci(l)) * orient(l);
            end
        end

        vecv(find(isnan(vect))) = NaN;

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
%
% save new structfile
if exist('MODEL_area', 'var')
    save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_area', 'MODEL_time');
else
    save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_time');
end
