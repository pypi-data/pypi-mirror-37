function [] = loaddata_GFDL_opendap(structfile, URL, file_prefix, file_suffix)
%LOADDATA_GFDL_OPENDAP
%
% DESCRIPTION
% LOADDATA_GFDL_OPENDAP extracts the model output, interpolates if needed on west and north faces, and saves
% only the data along preselected sections and areas in structfile.
%
% URL is where the model output can be find (through opendap protocol), filename is
% {so, thetao, umo, vmo}{file_prefix}{file_suffix}.nc
%
% EXAMPLES
%
%   See also <https://sourcesup.renater.fr/pago/models.html>, NANSUM
%
% TODO
% conversion °C to K : 273.15 not 273
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- last modified on July, 10th, 2012

load(structfile);

vart = 'thetao';
vars = 'so';
varh = 'thkcello';
varu = 'umo';
varv = 'vmo';

file = [URL vart '/' vart file_prefix file_suffix '.nc'];

nz = length(readdap(file, 'lev'));
[nlat, nlon] = size(readdap(file, 'lon'));

time = readdap(file, 'time');

% add variable thickness if does not exist
if exist('MODEL_area', 'var')
    if ~isfield('MODEL_area', 'volt')
        for area=1:length(MODEL_area)
            MODEL_area(area).volt = NaN * zeros(size(MODEL_area(area).temperature));
        end
    end
end

% get data over the selected region
for t=1:length(time)

    MODEL_time = cat(1, MODEL_time, time(t));
    disp(['loading data from day ' num2str(time(t)) ])

    file = [URL vars '/' vars file_prefix file_suffix '.nc'];% at tracer cell center, ie lont and latt
    sc = readdap(file, vars, [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn + 1, MODEL_grid.lone], [1, 1, 1, 1]);
    sn = nansum(cat(4, sc(:, 1:(end - 1), 2:end), sc(:, 2:end, 2:end)), 4)./nansum(cat(4, ~isnan(sc(:, 1:(end - 1), 2:end)), ~isnan(sc(:, 2:end, 2:end))), 4);
    sw = nansum(cat(4, sc(:, 1:(end - 1), 1:(end - 1)), sc(:, 1:(end - 1), 2:end)), 4)./nansum(cat(4, ~isnan(sc(:, 1:(end - 1), 1:(end - 1))), ~isnan(sc(:, 1:(end - 1), 2:end))), 4);
    sc = sc(:, 1:(end - 1), 2:end);

    file = [URL vart '/' vart file_prefix file_suffix '.nc']; % at tracer cell center, ie lont and latt, in K
    tc = readdap(file, vart, [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn + 1, MODEL_grid.lone], [1 1 1 1]) - 273; % in C
    tn = nansum(cat(4, tc(:, 1:(end - 1), 2:end), tc(:, 2:end, 2:end)), 4)./nansum(cat(4, ~isnan(tc(:, 1:(end - 1), 2:end)), ~isnan(tc(:, 2:end, 2:end))), 4);
    tw = nansum(cat(4, tc(:, 1:(end - 1), 1:(end - 1)), tc(:, 1:(end - 1), 2:end)), 4)./nansum(cat(4, ~isnan(tc(:, 1:(end - 1), 1:(end - 1))), ~isnan(tc(:, 1:(end - 1), 2:end))), 4);
    tc = tc(:, 1:(end - 1), 2:end);

    file = [URL varh '/' varh file_prefix file_suffix '.nc']; % at tracer cell center, ie lont and latt
    dhtc = readdap(file, varh, [t, 1, MODEL_grid.lats, MODEL_grid.lonw], [t, nz, MODEL_grid.latn, MODEL_grid.lone], [1 1 1 1]);

    file = [URL varv '/' varv file_prefix file_suffix '.nc'];  % at center of north face, ie lont and latv
    tvn = readdap(file, varv, [t, 1, MODEL_grid.lats, MODEL_grid.lonw], [t, nz, MODEL_grid.latn, MODEL_grid.lone], [1 1 1 1]); % unit: kg/s

    file = [URL varu '/' varu file_prefix file_suffix '.nc'];  % at center of east face, ie lonu and latt
    tuw = readdap(file, varu, [t, 1, MODEL_grid.lats, MODEL_grid.lonw - 1], [t, nz, MODEL_grid.latn, MODEL_grid.lone - 1], [1 1 1 1]); % unit: kg/s

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
                    vecv(:, l) = squeeze(tvn(:, vecj(l), veci(l))) * orient(l)./MODEL_sections(sec).areavect(:, l) * 1e-3; % m/s
               case 'W'
                    vect(:, l) = tw(:, vecj(l), veci(l));
                    vecs(:, l) = sw(:, vecj(l), veci(l));
                    vecv(:, l) = squeeze(tuw(:, vecj(l), veci(l))) * orient(l)./MODEL_sections(sec).areavect(:, l) * 1e-3; % m/s
           end
        end

        % the interpolation from the center of the cells to the faces is such
        % that it creates temperatures and salinities in land. here we force these
        % values to NaN
        vect(find(MODEL_sections(sec).areavect == 0)) = NaN;
        vecs(find(MODEL_sections(sec).areavect == 0)) = NaN;
        % vecv(find(isnan(vect))) = NaN;
        MODEL_sections(sec).vect = cat(1, MODEL_sections(sec).vect, reshape(vect, [1 nz nl]));
        MODEL_sections(sec).vecs = cat(1, MODEL_sections(sec).vecs, reshape(vecs, [1 nz nl]));
        MODEL_sections(sec).vecv = cat(1, MODEL_sections(sec).vecv, reshape(vecv, [1 nz nl]));

    end

    % get temperature, salinity on each grid point of areas
    % get thickness of each layer also

    if exist('MODEL_area', 'var')
        for area=1:length(MODEL_area)
            clear salinity temperature thickness
            for z=1:nz
                salinity(z, :) = diag(squeeze(sc(z, MODEL_area(area).indj, MODEL_area(area).indi)));
                temperature(z, :) = diag(squeeze(tc(z, MODEL_area(area).indj, MODEL_area(area).indi)));
                thickness(z, :) = diag(squeeze(dhtc(z, MODEL_area(area).indj, MODEL_area(area).indi)));
            end
            MODEL_area(area).salinity = cat(1, MODEL_area(area).salinity, reshape(salinity, [1, nz, length(MODEL_area(area).indi)]));
            MODEL_area(area).temperature = cat(1, MODEL_area(area).temperature, reshape(temperature, [1, nz, length(MODEL_area(area).indi)]));
            MODEL_area(area).volt = cat(1, MODEL_area(area).volt, reshape(thickness.*repmat(MODEL_area(area).surface', [nz, 1]), [1, nz, length(MODEL_area(area).indi)]));
        end
    end
end

% save new structfile
if exist('MODEL_area', 'var')
    save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_area', 'MODEL_time');
else
    save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_time');
end
