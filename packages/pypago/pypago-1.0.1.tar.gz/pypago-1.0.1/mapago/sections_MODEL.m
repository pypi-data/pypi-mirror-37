function [] = sections_MODEL(varargin)
%SECTIONS_MODEL creates sections and areas from any model grid
%
% DESCRIPTION
%
% standalone function that creates sections and areas from any model grid
% files.
%
% EXAMPLES
%
%   See also ALMANAC DISTANCE AXESM PCOLORM PLOTM NANSUM SCRIPT_PAGO_CCSM SCRIPT_PAGO_CNRM SCRIPT_PAGO_GFDL
%
%
% TODO do not use almanac (not recommended function)
%
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI --- last modified on May, 15th, 2012

model = input('input the model (GFDL, CCSM, MPIO, NEMO, ROMS, HYCO, OFAM, MICO): ', 's');

switch model
    case 'RCHB'
        gridfile = input('enter full path to nc file that contains some gridded observations: ', 's');
    case {'GFDL', 'CCSM', 'NEMO', 'MPIO', 'ROMS', 'MICO'}
        disp('enter full path to nc file that contains all information')
        gridfile = input('about the model grid (scale factors, bathymetry, mask...): ', 's');
    case {'HYCO', 'OFAM'}
        disp('enter full path to mat file that contains all information')
        gridfile = input('about the model grid(scale factors, bathymetry, mask...): ', 's');
    otherwise
        error('JD PAGO error: sections_MODEL undefined for this model');
end

% load location of center of grid cells, bathymetry and masks
switch model
    case 'GFDL'
        lont = readnc(gridfile, 'geolon_t');
        latt = readnc(gridfile, 'geolat_t');
        bathy = readnc(gridfile, 'ht');
        mask = readnc(gridfile, 'wet');
        mask(find(isnan(mask))) = 0;
    case 'CCSM'
        lont = readnc(gridfile, 'TLONG');
        latt = readnc(gridfile, 'TLAT');
        bathy = readnc(gridfile, 'HT') * 1e-2;  % originally in centimeters >> convert to meters
        mask = readnc(gridfile, 'REGION_MASK');
        % JD commented on March 18th 2015
        % lont(:, 1:36) = lont(:, 1:36) - 360; % because of discontinuity in longitude
    case 'RCHB'
        [lont, latt, zt, bathy, mask, dxt, dyt, dzt] = grid_HYDROBASE(gridfile);
    case 'NEMO'
        lont = readnc(gridfile, 'glamt');
        % JD commented on March 18th 2015
        % lont(:, 53:end) = lont(:, 53:end) + 360; % because of discontinuity in longitude % assumes that the grid is global, ORCA2 ?!?
        latt = readnc(gridfile, 'gphit');
        try
            zt = readnc(gridfile, 'gdept_0');
        catch exception
            zt = readnc(gridfile, 'gdept');
        end
        try
            bathy = readnc(gridfile, 'deptho');
        catch exception
            bathy_temp = readnc(gridfile, 'mbathy');
            bathy_temp(find(bathy_temp < 0)) = 0;
            bathy = reshape(zt(bathy_temp(:) + 1), size(bathy_temp));
        end
        mask_temp = readnc(gridfile, 'tmask');
        mask = squeeze(mask_temp(1, :, :));
    case 'MPIO'
        lont = flipdim(readnc(gridfile, 'lon'), 1); % flip direction in y to get north in top of figures
        latt = flipdim(readnc(gridfile, 'lat'), 1);
        zt = readnc(gridfile, 'depth_2');
        bathy = flipdim(readnc(gridfile, 'depto'), 1); % in meters
        mask = readnc(gridfile, 'amsup');
        mask = flipdim(squeeze(mask(1, :, :)), 1);
        mask(find(isnan(mask))) = 0;
    case 'HYCO'
        load(gridfile, 'plon');
        lont = plon;
        clear plon
        load(gridfile, 'plat');
        latt = plat;
        clear plat
        load(gridfile, 'depth');
        bathy = depth;
        clear depth
        mask = zeros(size(bathy));
        mask(find(bathy > 0)) = 1;
    case 'ROMS'
        lont = readnc(gridfile, 'lon_rho');
        latt = readnc(gridfile, 'lat_rho');
        bathy = readnc(gridfile, 'h');
        mask = readnc(gridfile, 'mask_rho');
    case 'OFAM'
        load(gridfile, 'x_T');
        lont = x_T;
        clear x_T
        load(gridfile, 'y_T');
        latt = y_T;
        clear y_T
        load(gridfile, 'depth_t');
        bathy = depth_t;
        clear depth_t
        load(gridfile, 'wet');
        mask = wet;
        clear wet
    % case 'MICO' % previous version of MICOM as used in BCM
    %     lont = flipdim(readnc(gridfile, 'plon')', 1);  % turning the grid by 90 deg to get x direction parallel to longitudes and y direction parallel to latitudes, with first indices at the south west corner
    %     latt = flipdim(readnc(gridfile, 'plat')', 1);
    %     bathy = flipdim(readnc(gridfile, 'pbath')', 1);
    %     mask = flipdim(readnc(gridfile, 'pmask')', 1);
    case 'MICO'
        lont = readnc(gridfile, 'plon');
        % lont(find(lont < -360)) = lont(find(lont < -360)) + 360;
        latt = readnc(gridfile, 'plat');
        bathy = readnc(gridfile, 'pdepth');
        mask = readnc(gridfile, 'pmask');
end
[nj, ni] = size(mask);

% select geographical area of interest to load from netcdf files
% cyclic boundary conditions are taken into account
figure(10);
clf;
hold on
contour(mask, [1 1], 'k')
hold on
xlabel('grid points')
ylabel('grid points')

ans_atl = JDinputbin('use predefined grid in the North Atlantic? (0 or 1) ');
if ans_atl
    ans_arctic = 0;
    run grid_corrections_NA
    disp('selected area indicated in blue: (numbers are grid indices)')
    disp(['lonw = ' num2str(MODEL_grid.lonw) ', lone = ' num2str(MODEL_grid.lone) ', lats = ' num2str(MODEL_grid.lats) ', latn = ' num2str(MODEL_grid.latn)]);
else
    ans_arctic = JDinputbin('use predefined grid in the Arctic? (0 or 1) ');
    if ans_arctic
        run grid_corrections_arctic
        disp('selected area indicated in blue: (numbers are grid indices)')
        disp(['lonw = ' num2str(MODEL_grid.lonw) ', lone = ' num2str(MODEL_grid.lone) ', lats = ' num2str(MODEL_grid.lats) ', latn = ' num2str(MODEL_grid.latn)]);
    else
        if JDinputbin(['use predefined grid file? (0 or 1) '])
            gridname = input(['enter name of grid file with full path ... '], 's');
            while ~exist(gridname)
                gridname = input(['error in name --- please re-enter ... '], 's');
            end
            load(gridname);
            disp('selected area indicated in blue: (numbers are grid indices)')
            disp(['lonw = ' num2str(MODEL_grid.lonw) ', lone = ' num2str(MODEL_grid.lone) ', lats = ' num2str(MODEL_grid.lats) ', latn = ' num2str(MODEL_grid.latn)]);
        else
            disp(['enter grid points defining area (1 <= {lonw, lone} <= ' num2str(size(mask, 2)) ', but 1 < {lats, latn} < ' num2str(size(mask, 1)) ')'])
            disp(['(note for GFDL and NEMO based models : latn may equal ' num2str(size(mask, 1)) ' : folding along the northernmost grid line of the model is assumed)'])
            disp(['(note for global diagnostics: the western edge of the maps will be set at lonw ; also avoid the arctic region for plotting issues)'])
            MODEL_grid.lonw = input('lonw = ');
            MODEL_grid.lone = input('lone = ');
            MODEL_grid.lats = input('lats = ');
            MODEL_grid.latn = input('latn = ');
            disp('selected area indicated in blue.')
        end
    end
end

figure(10)
plot([MODEL_grid.lonw MODEL_grid.lonw], [MODEL_grid.lats MODEL_grid.latn], 'b')
plot([MODEL_grid.lone MODEL_grid.lone], [MODEL_grid.lats MODEL_grid.latn], 'b')
if MODEL_grid.lone < MODEL_grid.lonw
    plot([MODEL_grid.lonw ni], [MODEL_grid.lats MODEL_grid.lats], 'b')
    plot([MODEL_grid.lonw ni], [MODEL_grid.latn MODEL_grid.latn], 'b')
    plot([0 MODEL_grid.lone], [MODEL_grid.latn MODEL_grid.latn], 'b')
    plot([0 MODEL_grid.lone], [MODEL_grid.lats MODEL_grid.lats], 'b')
else
    plot([MODEL_grid.lonw MODEL_grid.lone], [MODEL_grid.lats MODEL_grid.lats], 'b')
    plot([MODEL_grid.lonw MODEL_grid.lone], [MODEL_grid.latn MODEL_grid.latn], 'b')
end

while ~JDinputbin('ok with selected area? (0 or 1) ')
    disp(['enter grid points defining new area (1 <= {lonw, lone} <= ' num2str(size(mask, 2)) ', but 1 < {lats, latn} < ' num2str(size(mask, 1)) ')'])
    disp(['(note for GFDL and NEMO based models : latn may equal ' num2str(size(mask, 1)) ' : folding along the northernmost grid line of the model is assumed)'])
    disp(['(note for global diagnostics: the western edge of the maps will be set at lonw ; also avoid the arctic region for plotting issues)'])
    MODEL_grid.lonw = input('lonw = ');
    MODEL_grid.lone = input('lone = ');
    MODEL_grid.lats = input('lats = ');
    MODEL_grid.latn = input('latn = ');
    while MODEL_grid.latn < MODEL_grid.lats
        disp('latn must be larger than lats');
        MODEL_grid.lats = input('lats = ');
        MODEL_grid.latn = input('latn = ');
    end
    if exist('pl1')
        set(pl1, 'visible', 'off');
        set(pl2, 'visible', 'off');
        set(pl3, 'visible', 'off');
        set(pl4, 'visible', 'off');
    end
    if exist('pl5')
        set(pl5, 'visible', 'off');
        set(pl6, 'visible', 'off')
    end
    figure(10)
    pl1 = plot([MODEL_grid.lonw MODEL_grid.lonw], [MODEL_grid.lats MODEL_grid.latn], 'r');
    pl2 = plot([MODEL_grid.lone MODEL_grid.lone], [MODEL_grid.lats MODEL_grid.latn], 'r');
    if MODEL_grid.lone < MODEL_grid.lonw
        pl3 = plot([MODEL_grid.lonw ni], [MODEL_grid.lats MODEL_grid.lats], 'r');
        pl4 = plot([MODEL_grid.lonw ni], [MODEL_grid.latn MODEL_grid.latn], 'r');
        pl5 = plot([0 MODEL_grid.lone], [MODEL_grid.latn MODEL_grid.latn], 'r');
        pl6 = plot([0 MODEL_grid.lone], [MODEL_grid.lats MODEL_grid.lats], 'r');
    else
        pl3 = plot([MODEL_grid.lonw MODEL_grid.lone], [MODEL_grid.lats MODEL_grid.lats], 'r');
        pl4 = plot([MODEL_grid.lonw MODEL_grid.lone], [MODEL_grid.latn MODEL_grid.latn], 'r');
    end
    disp('new area indicated in red:')
    disp(['lonw = ' num2str(MODEL_grid.lonw) ', lone = ' num2str(MODEL_grid.lone) ', lats = ' num2str(MODEL_grid.lats) ', latn = ' num2str(MODEL_grid.latn)]);
end

if JDinputbin('save area? (0 or 1) ')
    gridname = input('save filename (including full path) to save area (.mat file): ', 's');
    disp(['save ' gridname ])
    save(gridname,'MODEL_grid');
end

% load scale factors and select for geographical areas + interpolate scale factors on north and west face of grid cells
switch model
    case 'GFDL'
        dxt = readnc(gridfile, 'dxt'); % at center
        dyt = readnc(gridfile, 'dyt'); % at center
        dye = readnc(gridfile, 'dyte'); % at eastern face of cell
        dxn = readnc(gridfile, 'dxtn'); % at northern face of cell
        dzt = readnc(gridfile, 'dz_t'); % at center
        dzc = readnc(gridfile, 'dz_c'); % at north WEST corner of cell
        dzt(find(dzt == 0)) = NaN;
        dzc(find(dzc == 0)) = NaN;
        disp('default configuration for GFDL defines Corner points at the north west corner of cell')
        disp('cf http://data1.gfdl.noaa.gov:9192/opendap/gfdl_cm2_0/ocean_grid_doc.html')
        disp('warning: CMIP5 GFDL-CM3 defines Corner points at the north east corner of cell !')
        if ~JDinputbin('use default configuration of GFDL which is Corner point at north west corner of cell? (0 or 1) ')
            disp('hence we assume here that Corner point is located at the north east corner of cell')
            dzc = cat(3, dzc(:, :, end), dzc(:, :, 1:end - 1));
        end
    case 'CCSM'
        dxt = readnc(gridfile, 'DXT') * 1e-2;  % originally in centimeters >> convert to meters
        dyt = readnc(gridfile, 'DYT') * 1e-2;  % originally in centimeters >> convert to meters
        dye = readnc(gridfile, 'HTE') * 1e-2;  % originally in centimeters >> convert to meters
        dxn = readnc(gridfile, 'HTN') * 1e-2;  % originally in centimeters >> convert to meters
        dzt = readnc(gridfile, 'dz') * 1e-2;  % originally in centimeters >> convert to meters
        dzw = dzt; % no partial steps
        dzn = dzt; % no partial steps
    case {'NEMO'}
        dxt = readnc(gridfile, 'e1t'); % at center
        dyt = readnc(gridfile, 'e2t'); % at center
        dye = readnc(gridfile, 'e2u'); % at eastern face of cell
        dxn = readnc(gridfile, 'e1v'); % at northern face of cell
        try
            dzt = readnc(gridfile, 'e3t').*double(readnc(gridfile, 'tmask')); % at center
        catch exception
            dzt = readnc(gridfile, 'e3t_0').*double(readnc(gridfile, 'tmask')); % at center
        end
        if ndims(dzt) == 2
            dzw = dzt; % no partial steps
            dzn = dzt; % no partial steps
        else
            try
                dze = readnc(gridfile, 'e3u_0');
            catch exception
                dze = readnc(gridfile, 'e3u');
            end
            try
                dze=dze.*double(readnc(gridfile, 'umask'));
            end
            try
                dzn = readnc(gridfile, 'e3v_0');
            catch exception
                dzn = readnc(gridfile, 'e3v');
            end
            try
                dzn=dzn.*double(readnc(gridfile, 'vmask'));
            end
            dzw = cat(3, dze(:, :, end), dze(:, :, 1:end - 1));
        end
    case 'RCHB'
        dxn = cat(1, 0.5 * (dxt(2:end, :) + dxt(1:end - 1, :)), zeros(1, size(dxt, 2)));
        dye = cat(2, 0.5 * (dyt(:, 2:end) + dyt(:, 1:end - 1)), zeros(size(dyt, 1), 1));
        dzw = dzt;
        dze = cat(3, min(dzt(:, :, 2:end), dzt(:, :, 1:end - 1)), zeros(size(dzt, 1), size(dzt, 2), 1));
        dzn = cat(2, min(dzt(:, 2:end, :), dzt(:, 1:end - 1, :)), zeros(size(dzt, 1), 1, size(dzt, 3)));
    case 'MPIO'
        dxt = flipdim(readnc(gridfile, 'dlxp'), 1);
        dyt = flipdim(readnc(gridfile, 'dlyp'), 1);
        dxn = flipdim(readnc(gridfile, 'dlxv'), 1);
        dye = flipdim(readnc(gridfile, 'dlyu'), 1);
        dzt = flipdim(readnc(gridfile, 'ddpo'), 2);
        dzw = dzt.*flipdim(readnc(gridfile, 'amsuo'), 2);
        dzn = dzt.*flipdim(readnc(gridfile, 'amsue'), 2);
    case 'HYCO'
        load(gridfile, 'scux');
        dxt = scux;
        clear scux % at center
        load(gridfile, 'scvy');
        dyt = scvy;
        clear scvy % at center
        load(gridfile, 'scqx'); % at southern face of cell
        dxn = cat(1, scqx(2:end, :), NaN * ones(size(scqx(end, :))));
        clear scqx % missing information, at northern boundary of domain
        load(gridfile, 'scqy');
        dyw = scqy;
        clear scqy;    % at western face of cell
        load(gridfile, 'layer_index'); % to get the number of vertical levels
        dzt = ones(length(layer_index), size(dxt, 1), size(dxt, 2));
        clear layer_index
        dze = dzt;
        dzn = dzt;
        dzw = dzt;
    case 'ROMS'
        dxt = 1./readnc(gridfile, 'pm_rho'); % at center [m]
        dyt = 1./readnc(gridfile, 'pn_rho'); % at center
        dxn = 1./readnc(gridfile, 'pm_v'); % at northern face of cell
        dxn = cat(1, dxn, NaN * ones(1, ni));
        dye = 1./readnc(gridfile, 'pn_u'); % at eastern face of cell
        dzt = readnc(gridfile, 'z_rho', [1 1 1 1], [1 -1 -1 -1]);
        dze = readnc(gridfile, 'z_u', [1 1 1 1], [1 -1 -1 -1]);
        dzn = readnc(gridfile, 'z_v', [1 1 1 1], [1 -1 -1 -1]);
        dzw = cat(3, NaN * ones(size(dzt, 1), nj, ni), dze);
    case 'OFAM'
        load(gridfile, 'ds_01_21_T');
        dxt = ds_01_21_T;
        clear ds_01_21_T
        load(gridfile, 'ds_10_12_T');
        dyt = ds_10_12_T;
        clear ds_10_12_T
        load(gridfile, 'ds_00_02_T');
        dyw = ds_00_02_T;
        clear ds_00_02_T
        load(gridfile, 'ds_02_22_T');
        dxn = ds_02_22_T;
        clear ds_02_22_T
        load(gridfile, 'zb');
        dzt = diff([0;zb]);
        clear zb
        dzw = dzt;
        dzn = dzt;
%    case 'MICO'% previous version of MICOM as used in BCM
%        dxt = flipdim(readnc(gridfile, 'pscaley')', 1); % same operations as on grid lon/lat below
%        dyt = flipdim(readnc(gridfile, 'pscalex')', 1);
%        dxn = flipdim(readnc(gridfile, 'uscaley')', 1);
%        dyw = flipdim(readnc(gridfile, 'vscalex')', 1);
%        nz = length(readnc(gridfile, 'sigma'));
%        dzt = ones(nz, 1);
%        dzn = ones(nz, 1);
%        dzw = ones(nz, 1);
    case 'MICO'
        dxt = readnc(gridfile, 'pdx');
        dyt = readnc(gridfile, 'pdy');
        dxs = readnc(gridfile, 'vdx'); % at southern face of cell
        dxn = zeros(size(dxs));
        dxn(1:end - 1, :) = dxs(2:end, :);
        dyw = readnc(gridfile, 'udy');
        side = JDinputbin('diagnosing MICOM isopycnic outputs (answer 1) or depth-interpolated outputs (answer 0) ? ');
        switch side
            case 1
                nz = str2num(input('please enter the number of levels : ', 's'));
                dzt = ones(nz, 1);
                dzn = ones(nz, 1);
                dzw = ones(nz, 1);
            case 0
                zfile = input('please enter name of .nc file where variable depth available : ', 's');
                depth_bnds = readnc(zfile, 'depth_bnds'); % position of the boundaries of the levels
                dzt = depth_bnds(:, 2) - depth_bnds(:, 1);
                dzw = dzt;
                dzn = dzt;
        end
end

if MODEL_grid.lone < MODEL_grid.lonw
%    if max(max(lont(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end))) <= min(min(lont(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone)))
        MODEL_grid.lont = cat(2, lont(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), lont(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
%    else
%        MODEL_grid.lont = cat(2, lont(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end) - 360, lont(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
%    end
    MODEL_grid.latt = cat(2, latt(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), latt(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    MODEL_grid.bathy = cat(2, bathy(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), bathy(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    MODEL_grid.mask = cat(2, mask(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), mask(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    dxt = cat(2, dxt(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dxt(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    dxn = cat(2, dxn(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dxn(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    dyt = cat(2, dyt(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dyt(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    if ~exist('dyw', 'var')
        if MODEL_grid.lone > 1
            dyw = cat(2, dye(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw - 1:end), dye(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone - 1));
        else
            dyw = dye(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw - 1:end);
        end
    else
        dyw = cat(2, dyw(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dyw(MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
    end
    if ndims(dzt) > 2
        switch model
            case 'GFDL'
                dzc = cat(3, dzc(:, MODEL_grid.lats - 1:MODEL_grid.latn, MODEL_grid.lonw:end), dzc(:, MODEL_grid.lats - 1:MODEL_grid.latn, 1:MODEL_grid.lone + 1));
                dzw = 0.5 * squeeze(nansum(cat(4, dzc(:, 2:end, 1:end - 1), dzc(:, 1:end - 1, 1:end - 1)), 4)); % cf GFDL userguide
                dzn = 0.5 * squeeze(nansum(cat(4, dzc(:, 2:end, 2:end), dzc(:, 2:end, 1:end - 1)), 4)); % cf GFDL userguide
                dzt = cat(3, dzt(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dzt(:, MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
            otherwise
                dzt = cat(3, dzt(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dzt(:, MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
                dzw = cat(3, dzw(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dzw(:, MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
                dzn = cat(3, dzn(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:end), dzn(:, MODEL_grid.lats:MODEL_grid.latn, 1:MODEL_grid.lone));
        end
    end
else % MODEL_grid.lonw < MODEL_grid.lone
    MODEL_grid.lont = lont(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    MODEL_grid.latt = latt(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    MODEL_grid.bathy = bathy(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    MODEL_grid.mask = mask(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
%    if max(max(MODEL_grid.lont > 360))
%        MODEL_grid.lont = MODEL_grid.lont - 360;
%    end
%    if min(min(MODEL_grid.lont < -360))
%        MODEL_grid.lont = MODEL_grid.lont + 360;
%    end
    dxt = dxt(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    dxn = dxn(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    dyt = dyt(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    if ~exist('dyw', 'var')
    if MODEL_grid.lonw > 1
        dyw = dye(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw - 1:MODEL_grid.lone - 1);
    else
        dyw = cat(2, dye(MODEL_grid.lats:MODEL_grid.latn, end), dye(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone - 1));
    end
    else
        dyw = dyw(MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
    end
    if ndims(dzt) > 2
        if strcmp(model, 'GFDL')
            if MODEL_grid.lone < size(mask, 2)
                dzc = dzc(:, MODEL_grid.lats - 1:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone + 1);
            else
                dzc = cat(3, dzc(:, MODEL_grid.lats - 1:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone), dzc(:, MODEL_grid.lats - 1:MODEL_grid.latn, 1));
            end
            dzw = 0.5 * squeeze(nansum(cat(4, dzc(:, 2:end, 1:end - 1), dzc(:, 1:end - 1, 1:end - 1)), 4));
            dzn = 0.5 * squeeze(nansum(cat(4, dzc(:, 2:end, 2:end), dzc(:, 2:end, 1:end - 1)), 4));
            dzt = dzt(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
        else
            dzt = dzt(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
            dzw = dzw(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
            dzn = dzn(:, MODEL_grid.lats:MODEL_grid.latn, MODEL_grid.lonw:MODEL_grid.lone);
        end
    end
end

if ndims(dzt) == 2
    nz = length(dzt);
    [nj, ni] = size(dxt);
    if size(dzt, 1) == 1
        dzt = dzt';
    end
    if size(dzw, 1) == 1
        dzw = dzw';
    end
    if size(dzn, 1) == 1
        dzn = dzn';
    end
    dzt = repmat(dzt, [1 nj ni]);
    dzw = repmat(dzw, [1 nj ni]);
    dzn = repmat(dzn, [1 nj ni]);
else
    [nz, nj, ni] = size(dzt);
end

areaW = dzw.*repmat(reshape(dyw, [1 nj ni]), [nz 1 1]); % in m2
areaN = dzn.*repmat(reshape(dxn, [1 nj ni]), [nz 1 1]); % in m2
areaW(find(isnan(areaW))) = 0;
areaN(find(isnan(areaN))) = 0;
volume = dzt.*repmat(reshape(dxt.*dyt, [1 nj ni]), [nz 1 1]); % in m3
volume(find(isnan(volume))) = 0;
surface = dxt.*dyt; % in m2

% JD removed on March 18th 2015 and replaced by the additional test below
% check longitude for cutting the map (avoid cutting in the middle of a region of interest)
%disclon = 180;
%    if ~JDinputbin('ok with cutting the map at longitude 180 ? (0 or 1) ');
%        disclon = input('enter longitude for cutting the map (from 0 to 360): ');
%    end
%MODEL_grid.lont(find(MODEL_grid.lont > disclon)) = MODEL_grid.lont(find(MODEL_grid.lont > disclon)) - 360;
% additional test to remove any discontinuity in longitude
% only if the first figure does not look correct !
%for j=1:nj
%        ind = min(find(abs(diff(MODEL_grid.lont(j, :))) > 10)) + 1;
%        MODEL_grid.lont(j, ind:end) = MODEL_grid.lont(j, ind:end) + 360;
%end

figure(11)
clf
if ans_arctic % plotting for the Arctic region
        axesm('vperspec', 'Frame', 'off', 'Grid', 'off', 'origin', [55 320 0]);
        atracer = MODEL_grid.bathy;
        atracer(find(MODEL_grid.mask == 0)) = NaN;
        h = pcolorm(MODEL_grid.latt, MODEL_grid.lont, atracer);
        set(h, 'linestyle', 'none')
else
        atracer = MODEL_grid.bathy;
        atracer(find(MODEL_grid.mask == 0)) = NaN;
        h = pcolor(MODEL_grid.lont, MODEL_grid.latt, atracer);
        set(h, 'linestyle', 'none')
        if ~JDinputbin('does the figure look good ? (0 or 1) ')
            disp('PAGO assumes that this is due to discontinuities in longitude.')
            disp('if the problem persists, a manual check of MODEL_grid.lont is necessary...')
            for j=1:nj
                ind = min(find(abs(diff(MODEL_grid.lont(j, :))) > 10)) + 1;
                MODEL_grid.lont(j, ind:end) = MODEL_grid.lont(j, ind:end) + 360;
            end
            clf
            atracer = MODEL_grid.bathy;
            atracer(find(MODEL_grid.mask == 0)) = NaN;
            h = pcolor(MODEL_grid.lont, MODEL_grid.latt, atracer);
            set(h, 'linestyle', 'none')
        end
        xlabel('longitude')
        ylabel('latitude')
end
hc = colorbar;
ylabel(hc, 'Bathymetry (m)');

% get endpoints of sections
basedir = fullfile(getenv('HOME'), '.pago');
if ans_atl || ans_arctic || JDinputbin('load predefined lat/lon of section endpoints? (0 or 1) ')
    if ans_atl
        load(fullfile(basedir, ['sections_NA.mat']));
    else
        if ans_arctic
           load(fullfile(basedir, ['sections_AR.mat']));
        else
            file = input('enter filename (including full path): ', 's');
            load(file);
        end
    end
    nsec = length(sections);
    for sec=1:nsec
        MODEL_sections(sec).name = sections(sec).name;
        [vecj, veci] = locingrid(sections(sec).lon, sections(sec).lat, MODEL_grid.lont, MODEL_grid.latt);
        sections(sec).i = veci;
        sections(sec).j = vecj;
        if sections(sec).i(end) < sections(sec).i(1)
            sections(sec).i = fliplr(sections(sec).i);
            sections(sec).j = fliplr(sections(sec).j);
            sections(sec).dir = flipud(sections(sec).dir);
        end
    end
% built-in corrections for some models for sections in North Atlantic
    if ans_atl
        if JDinputbin('use built-in correction of sections from JD --- only if proper GRID area selected --- (0 or 1) ')
            run section_corrections_NA
        end
    end
    if ans_arctic
        if JDinputbin('use built-in correction of sections from JD --- only if proper GRID area selected --- (0 or 1) ')
            run section_corrections_arctic
        end
    end

    figure(11);
    hold on
    if ~ans_arctic
            for sec=1:nsec
                plot(sections(sec).lon, sections(sec).lat, 'k.')
                plot(sections(sec).lon, sections(sec).lat, 'k')
            end
    else
            for sec=1:nsec
                h = plotm(sections(sec).lat, sections(sec).lon);
                set(h, 'color', 'k')
                h = plotm(sections(sec).lat, sections(sec).lon);
                set(h, 'color', 'k')
            end
    end
    figure(12);
    clf;
    hold on
    contour(MODEL_grid.mask, [1 1], 'k')
    for sec=1:nsec
        plot(sections(sec).i, sections(sec).j, 'r.')
        plot(sections(sec).i, sections(sec).j, 'r')
    end
    title('end points of sections')
    grid on
    xlabel('grid points')
    ylabel('grid points')
end

while (~ans_arctic) & JDinputbin('add section? (0 or 1) ');
    if exist('MODEL_sections', 'var')
        nsec = length(MODEL_sections);
    else
        nsec = 0;
        figure(12)
        clf
        contour(MODEL_grid.mask, [1 1], 'k')
        hold on
        title('end points of sections')
        grid on
        xlabel('grid points')
        ylabel('grid points')
    end
    MODEL_sections(nsec + 1).name = input('short name for section (3 letters only, a25 for example): ', 's');
    while length(MODEL_sections(nsec + 1).name) ~= 3
        MODEL_sections(nsec + 1).name = input('please type again the name for section : it must be 3 letters (a25 for example)... ', 's');
    end
    disp('select end points and corners by clicking on the figure (within black dots), then press return key')
    figure(11)
    hold on
    plot(MODEL_grid.lont(1, :), MODEL_grid.latt(1, :), 'k.');
    plot(MODEL_grid.lont(end, :), MODEL_grid.latt(end, :), 'k.');
    plot(MODEL_grid.lont(:, 1), MODEL_grid.latt(:, 1), 'k.');
    plot(MODEL_grid.lont(:, end), MODEL_grid.latt(:, end), 'k.');
    [lon, lat] = ginputJD;
    plot(lon, lat, 'r')
    [vecj, veci] = locingrid(lon, lat, MODEL_grid.lont, MODEL_grid.latt);
    sections(nsec + 1).i = veci;
    sections(nsec + 1).j = vecj;

    figure(12)
    plot(sections(end).i, sections(end).j, 'r.')
    plot(sections(end).i, sections(end).j, 'r')
    for l=1:length(sections(end).i) - 1
        text(.5 * (sections(end).i(l + 1) + sections(end).i(l)), .5 * (sections(end).j(l + 1) + sections(end).j(l)), num2str(l))
    end

    disp(['enter directions (NW, NE, SW or SE) for the segment(s) of section ' MODEL_sections(nsec + 1).name])
    disp('(directions being defined in distorted grid)')
    disp('(press enter after each segment)')
    sections(nsec + 1).dir = [];
    for l=1:length(sections(nsec + 1).i) - 1
        temp = input(['segment #' num2str(l) ': '], 's');
        while length(temp) > 2
            temp = input('(re-enter only 2 letters: NE NW SE or SW): ', 's');
        end
        sections(nsec + 1).dir = cat(1, sections(nsec + 1).dir, temp);
    end

    if sections(nsec + 1).i(end) < sections(nsec + 1).i(1)
        sections(nsec + 1).i = fliplr(sections(nsec + 1).i);
        sections(nsec + 1).j = fliplr(sections(nsec + 1).j);
        sections(nsec + 1).dir = flipud(sections(nsec + 1).dir);
    end
end

if exist('sections', 'var')
    figure(12);
    clf;
    hold on
    contour(MODEL_grid.mask, [1 1], 'k')
    for sec=1:length(sections)
        plot(sections(sec).i, sections(sec).j, 'r.')
        plot(sections(sec).i, sections(sec).j, 'r')
        text(.5 * (sections(sec).i(2) + sections(sec).i(1)), .5 * (sections(sec).j(2) + sections(sec).j(1)), MODEL_sections(sec).name, 'color', 'r', 'fontweight', 'bold')
    end
    title('end points of sections')
    grid on
    xlabel('grid points')
    ylabel('grid points')

    % check for each section whether endpoint is in land
    nsec = length(sections);
    for sec=1:nsec
        test1 = MODEL_grid.mask(sections(sec).j(1), sections(sec).i(1));
        test2 = MODEL_grid.mask(sections(sec).j(end), sections(sec).i(end));
        if ~test1 && ~test2
        else
            if test1
                if sections(sec).i(1) - 1 > 0 & ~MODEL_grid.mask(sections(sec).j(1), sections(sec).i(1) - 1)
                    sections(sec).i(1) = sections(sec).i(1) - 1;
                else
                    if sections(sec).j(1) - 1 > 0 & ~MODEL_grid.mask(sections(sec).j(1) - 1, sections(sec).i(1))
                        sections(sec).j(1) = sections(sec).j(1) - 1;
                    else
                        if sections(sec).j(1) + 1 < size(MODEL_grid.mask, 1) & ~MODEL_grid.mask(sections(sec).j(1) + 1, sections(sec).i(1))
                            sections(sec).j(1) = sections(sec).j(1) + 1;
                        else
                            disp(['section ' MODEL_sections(sec).name ' : 1st point in water'])
                            ans1 = JDinputbin('change location of point? (0 or 1) ');
                            if ans1
                                disp(['j-index = ' num2str(sections(sec).j(1)) ' , i-index = ' num2str(sections(sec).i(1)) ])
                                sections(sec).j(1) = input('new j-index = ');
                                sections(sec).i(1) = input('new i-index = ');
                            end
                        end
                    end
                end
            end
            if test2 > 0
                if sections(sec).i(end) - 1 > 0 & ~MODEL_grid.mask(sections(sec).j(end), sections(sec).i(end) - 1)
                    sections(sec).i(end) = sections(sec).i(end) - 1;
                else
                    if sections(sec).j(end) - 1 > 0 & ~MODEL_grid.mask(sections(sec).j(end) - 1, sections(sec).i(end))
                        sections(sec).j(end) = sections(sec).j(end) - 1;
                    else
                        if sections(sec).j(end) + 1 < size(MODEL_grid.mask, 1) & ~MODEL_grid.mask(sections(sec).j(end) + 1, sections(sec).i(end))
                            sections(sec).j(end) = sections(sec).j(end) + 1;
                        else
                            disp(['section ' MODEL_sections(sec).name ' : last point in water'])
                            ans1 = JDinputbin('change location of point? (0 or 1) ');
                            if ans1
                                disp(['j-index = ' num2str(sections(sec).j(end)) ' , i-index = ' num2str(sections(sec).i(end)) ])
                                sections(sec).j(end) = input('new j-index = ');
                                sections(sec).i(end) = input('new i-index = ');
                            end
                        end
                    end
                end
            end
        end
    end

    figure(12)
    clf
    contour(MODEL_grid.mask, [1 1], 'k')
    hold on
    for sec=1:nsec
        plot(sections(sec).i, sections(sec).j, 'r.')
        plot(sections(sec).i, sections(sec).j, 'r')
        text(.5 * (sections(sec).i(2) + sections(sec).i(1)), .5 * (sections(sec).j(2) + sections(sec).j(1)), MODEL_sections(sec).name, 'color', 'r', 'fontweight', 'bold')
    end
    title('end points of sections')
    grid on
    xlabel('grid points')
    ylabel('grid points')

    if JDinputbin('save (lon/lat) end points and corners of sections? (0 or 1) ')
        for s=1:length(sections)
            newsections(s).name = MODEL_sections(s).name;
            newsections(s).lon = diag(MODEL_grid.lont(sections(s).j, sections(s).i));
            newsections(s).lat = diag(MODEL_grid.latt(sections(s).j, sections(s).i));
            newsections(s).dir = sections(sec).dir;
        end
        sections_keep = sections;
        sections = newsections;
        sectionsname = input('save filename (including full path) to save sections (.mat file): ', 's');
        disp(['save ' sectionsname])
        save(sectionsname, 'sections');
        sections = sections_keep;
        clear sections_keep newsections
    end

    % get all points along sections + information for all points
    earthell = almanac('earth', 'ellipsoid');
    nsec = length(sections);
    for sec=1:nsec
        [vecj, veci] = secingrid(sections(sec).i(1), sections(sec).j(1), sections(sec).i(2), sections(sec).j(2));
        [faces, newveci, newvecj, orientation] = facesinsec(veci, vecj, sections(sec).dir(1, :));
        MODEL_sections(sec).veci = newveci;
        MODEL_sections(sec).vecj = newvecj;
        MODEL_sections(sec).faces = faces;
        MODEL_sections(sec).orient = orientation;
        nl1 = floor(length(newveci)/2);
        sections(sec).corner = []; % variable created to keep track of the changes in section direction
        if length(sections(sec).i) > 2
            for l=3:length(sections(sec).i)
                sections(sec).corner = cat(1, sections(sec).corner, length(MODEL_sections(sec).veci));
                [vecj, veci] = secingrid(sections(sec).i(l - 1), sections(sec).j(l - 1), sections(sec).i(l), sections(sec).j(l));
                [faces, newveci, newvecj, orientation] = facesinsec(veci, vecj, sections(sec).dir(l - 1, :));
                [finalfaces, finalveci, finalvecj, finalorient] = consec(MODEL_sections(sec).veci, MODEL_sections(sec).vecj, MODEL_sections(sec).faces, MODEL_sections(sec).orient, newveci, newvecj, faces, orientation, sections(sec).corner);
                MODEL_sections(sec).veci = finalveci;
                MODEL_sections(sec).vecj = finalvecj;
                MODEL_sections(sec).faces = finalfaces;
                MODEL_sections(sec).orient = finalorient;
                nl2 = floor(length(newveci)/2);
            end
        end

        % in case section is closed
        if MODEL_sections(sec).veci(1) == MODEL_sections(sec).veci(end) && MODEL_sections(sec).vecj(1) == MODEL_sections(sec).vecj(end)
            [finalfaces, finalveci, finalvecj, finalorient] = consec(MODEL_sections(sec).veci(end - nl2:end), MODEL_sections(sec).vecj(end - nl2:end), MODEL_sections(sec).faces(end - nl2:end), MODEL_sections(sec).orient(end - nl2:end), ...
                                                        MODEL_sections(sec).veci(1:nl1), MODEL_sections(sec).vecj(1:nl1), MODEL_sections(sec).faces(1:nl1), MODEL_sections(sec).orient(1:nl1));
            MODEL_sections(sec).veci = [MODEL_sections(sec).veci(nl1 + 1:end - nl2 - 1) finalveci];
            MODEL_sections(sec).vecj = [MODEL_sections(sec).vecj(nl1 + 1:end - nl2 - 1) finalvecj];
            MODEL_sections(sec).faces = [MODEL_sections(sec).faces(nl1 + 1:end - nl2 - 1);finalfaces];
            MODEL_sections(sec).orient = [MODEL_sections(sec).orient(nl1 + 1:end - nl2 - 1) finalorient];
        end

        MODEL_sections(sec).areavect = areainsec(MODEL_sections(sec).veci, MODEL_sections(sec).vecj, MODEL_sections(sec).faces, areaW, areaN);
        MODEL_sections(sec).lengthvect = lengthinsec(MODEL_sections(sec).veci, MODEL_sections(sec).vecj, MODEL_sections(sec).faces, dyw, dxn);
        MODEL_sections(sec).depthvect = areainsec(MODEL_sections(sec).veci, MODEL_sections(sec).vecj, MODEL_sections(sec).faces, dzw, dzn);

        % length in km along section for visualization
        nl = length(find(~isnan(MODEL_sections(sec).veci)));
        [vecj, veci] = nodouble(MODEL_sections(sec).veci(1:nl), MODEL_sections(sec).vecj(1:nl));
        MODEL_sections(sec).lvect(1) = 0;
        for l=2:length(veci)
            MODEL_sections(sec).lvect(l) = MODEL_sections(sec).lvect(l - 1) + distance(latt(vecj(l), veci(l)), lont(vecj(l), veci(l)), latt(vecj(l - 1), veci(l - 1)), lont(vecj(l - 1), veci(l - 1)), earthell);
        end

        % prepare space to load data
        MODEL_sections(sec).vect = NaN * ones(1, nz, length(MODEL_sections(sec).veci));
        MODEL_sections(sec).vecs = NaN * ones(1, nz, length(MODEL_sections(sec).veci));
        MODEL_sections(sec).vecv = NaN * ones(1, nz, length(MODEL_sections(sec).veci));
    end

    % in North Atlantic, check connection between ifo and fso: if no land point at crossover,
    % remove the end point of section ifo if same as start point of section fso
    for l=1:length(MODEL_sections)
        vecname(l, :) = MODEL_sections(l).name;
    end
    ifo = find(strcmp(vecname(:, 1), 'i') & strcmp(vecname(:, 2), 'f') & strcmp(vecname(:, 3), 'o'));
    fso = find(strcmp(vecname(:, 1), 'f') & strcmp(vecname(:, 2), 's') & strcmp(vecname(:, 3), 'o'));
    if not(isempty(ifo)) && not(isempty(fso))
        if (MODEL_sections(ifo).veci(end) == MODEL_sections(fso).veci(1)) & (MODEL_sections(ifo).vecj(end) == MODEL_sections(fso).vecj(1))
            MODEL_sections(ifo).veci = MODEL_sections(ifo).veci(1:end - 1);
            MODEL_sections(ifo).vecj = MODEL_sections(ifo).vecj(1:end - 1);
            MODEL_sections(ifo).faces = MODEL_sections(ifo).faces(1:end - 1);
            MODEL_sections(ifo).orient = MODEL_sections(ifo).orient(1:end - 1);
            MODEL_sections(ifo).areavect = MODEL_sections(ifo).areavect(:, 1:end - 1);
            MODEL_sections(ifo).lengthvect = MODEL_sections(ifo).lengthvect(1:end - 1);
            MODEL_sections(ifo).depthvect = MODEL_sections(ifo).depthvect(:, 1:end - 1);
            MODEL_sections(ifo).lvect = MODEL_sections(ifo).lvect(1:end - 1);
            MODEL_sections(ifo).vect = MODEL_sections(ifo).vect(:, :, 1:end - 1);
            MODEL_sections(ifo).vecs = MODEL_sections(ifo).vecs(:, :, 1:end - 1);
            MODEL_sections(ifo).vecv = MODEL_sections(ifo).vecv(:, :, 1:end - 1);
        end
    end

    figure(12)
    clf
    contour(MODEL_grid.mask, [1 1], 'k')
    hold on
    for sec=1:nsec
        plotsecfaces(MODEL_sections(sec).veci, MODEL_sections(sec).vecj, MODEL_sections(sec).faces, MODEL_sections(sec).orient, 'b');
        text(.5 * (sections(sec).i(2) + sections(sec).i(1)), .5 * (sections(sec).j(2) + sections(sec).j(1)), MODEL_sections(sec).name, 'color', 'b', 'fontweight', 'bold')
    end
    title('sections in grid')
    xlabel('grid points')
    ylabel('grid points')

    disp('please check carefully that the direction of transport across each section is correct using the dots : ')
    disp('the dots may be viewed as the head of arrows normal to each section, ')
    disp('heading in the direction defined as positive for the mass transport.')
    count = 1;
    while ~JDinputbin('ok with the direction of each section ? (0 or 1) ')
        if count == 1
            disp(['recall name of sections:'])
            for sec=1:length(MODEL_sections)
                disp(MODEL_sections(sec).name)
            end
            count = count + 1;
        end
        wrongdirsec_allnames = input('enter list of sections with incorrect direction (list of names separated by space): ', 's');
        wrongdirsec = [];
        temp = find(wrongdirsec_allnames == ' ');
        temp = cat(2, 0, temp);
        for ind=1:length(temp)
            wrongdirsec = cat(1, wrongdirsec, findsecnum(MODEL_sections, wrongdirsec_allnames(temp(ind) + 1:temp(ind)+3)));
        end

        for sec=1:length(wrongdirsec)
            disp(['enter directions (NW, NE, SW or SE) for the segment(s) of section ' MODEL_sections(wrongdirsec(sec)).name])
            disp('(press enter after each segment)')
            for l=1:length(sections(wrongdirsec(sec)).i) - 1
                text(.5 * (sections(wrongdirsec(sec)).i(l + 1) + sections(wrongdirsec(sec)).i(l)), .5 * (sections(wrongdirsec(sec)).j(l + 1) + sections(wrongdirsec(sec)).j(l)), num2str(l))
                temp = input(['segment #' num2str(l) ': '], 's');
                while length(temp) > 2
                    temp = input('(re-enter only 2 letters: NE NW SE or SW): ', 's');
                end
                if sections(wrongdirsec(sec)).dir(l, 1) ~= temp(1)
                    if isempty(sections(wrongdirsec(sec)).corner)
                        MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces == 'N')) = -MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces == 'N'));
                    else
                        switch l
                            case 1
                                MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces(1:sections(wrongdirsec(sec)).corner(1)) == 'N')) = -MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces(1:sections(wrongdirsec(sec)).corner(1)) == 'N'));
                            otherwise
                                if l == length(sections(wrongdirsec(sec)).corner) + 1
                                    MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(end) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(end) + 1:end) == 'N')) = -MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(end) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(end) + 1:end) == 'N'));
                                else
                                    MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(l - 1) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(l - 1) + 1:sections(wrongdirsec(sec)).corner(l)) == 'N')) = -MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(l - 1) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(l - 1) + 1:sections(wrongdirsec(sec)).corner(l)) == 'N'));
                                end
                         end
                    end
                end
                if sections(wrongdirsec(sec)).dir(l, 2) ~= temp(2)
                    if isempty(sections(wrongdirsec(sec)).corner)
                        MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces == 'W')) = -MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces == 'W'));
                    else
                        switch l
                            case 1
                                MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces(1:sections(wrongdirsec(sec)).corner(1)) == 'W')) = -MODEL_sections(wrongdirsec(sec)).orient(find(MODEL_sections(wrongdirsec(sec)).faces(1:sections(wrongdirsec(sec)).corner(1)) == 'W'));
                            otherwise
                                if l == length(sections(wrongdirsec(sec)).corner) + 1
                                    MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(end) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(end) + 1:end) == 'W')) = -MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(end) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(end) + 1:end) == 'W'));
                                else
                                    MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(l - 1) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(l - 1) + 1:sections(wrongdirsec(sec)).corner(l)) == 'W')) = -MODEL_sections(wrongdirsec(sec)).orient(sections(wrongdirsec(sec)).corner(l - 1) + find(MODEL_sections(wrongdirsec(sec)).faces(sections(wrongdirsec(sec)).corner(l - 1) + 1:sections(wrongdirsec(sec)).corner(l)) == 'W'));
                                end
                        end
                    end
                end
            end

            figure(12);
            clf;
            hold on
            contour(MODEL_grid.mask, [1 1], 'k')
            for sec=1:nsec
                plotsecfaces(MODEL_sections(sec).veci, MODEL_sections(sec).vecj, MODEL_sections(sec).faces, MODEL_sections(sec).orient, 'b');
                text(.5 * (sections(sec).i(2) + sections(sec).i(1)), .5 * (sections(sec).j(2) + sections(sec).j(1)), MODEL_sections(sec).name, 'color', 'b', 'fontweight', 'bold')
            end
            title('sections in grid')
            xlabel('grid points')
            ylabel('grid points')
        end
    end

end  % test whether sections have been defined

% save information in matlab file

MODEL_time = NaN;

if JDinputbin('save data? (0 or 1) ')
   if nargin > 0
        structfile = varargin{1};
   else
       structfile = input('enter filename (including full path) to be used (.mat file): ', 's');
   end
   save(structfile, 'MODEL_grid', 'MODEL_sections', 'MODEL_time');
   disp(['saved ' structfile])
end
