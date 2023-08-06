function [MODEL_volume] = volumes_MODEL(varargin)
%VOLUMES_MODEL calculates the integral of tracers over volumes
%
% DESCRIPTION
%
% calculates the integral of tracers over volumes defined by MODEL_area and the convergence of fluxes at the boundaries
% uses only one argument : the structfile that contains MODEL_area and MODEL_sections
%
% the output, MODEL_volume, contains only time series of the indices relative to those integrals
% present function calibrated for North Atlantic subpolar gyre and nordic seas - for customisation in other regions, adapt variable vecsecin below
%
% units are as follows : heat content (J) and haline content (psu*m3)
%
% EXAMPLES
%
%   See also <https://sourcesup.renater.fr/pago/overview.html>, NANSUM
%
% TODO
% test validity of arg (file exists ?)
% rename arg
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD --- modified on May, 8th, 2012

% loads structfile to get the number of time iterations nt and the number of vertical levels nz
load(varargin{1})
[nt, nz, nl] = size(MODEL_sections(1).vect);

% sections for mass heat and salt transport into areas of the North Atlantic
% to be modified in order to apply to other regions, with vecsecin.sign positive when sign convention directed toward the area of interest

% for subpolar gyre
vecsecin(1).name = ['42n';'hud';'baf';'dso';'ifo';'fso'];
disp('sections used for convergence calculation into the subpolar gyre: ');
for s=1:size(vecsecin(1).name, 1)
    disp(vecsecin(1).name(s, :))
    vecsecin(1).sec(s) = findsecnum(MODEL_sections, vecsecin(1).name(s, :));
end
vecsecin(1).sign = [1 1 1 -1 -1 -1];
disp(['please verify that the sections listed above correspond to the actual boundaries of the subpolar gyre (check whether a section in between Ireland and Scotland is needed, for example)...'])
disp(['if this is not the case, correct variable vecsecin in function volumes_MODEL.m directly and re-run the program.'])

% for nordic seas
vecsecin(2).name = ['bar';'non';'dso';'ifo';'fso';'mdn'];
disp(['sections used for convergence calculation into the Nordic Seas: '])
for s=1:size(vecsecin(2).name, 1)
    disp(vecsecin(2).name(s, :))
    vecsecin(2).sec(s) = findsecnum(MODEL_sections, vecsecin(2).name(s, :));
end
vecsecin(2).sign = [-1 -1 1 1 1 1];
disp(['please verify that the sections listed above correspond to the actual boundaries of the Nordic Seas...'])
disp(['if this is not the case, correct variable vecsecin in function volumes_MODEL.m directly and re-run the program.'])

if ~isfield(MODEL_sections, 'vecv')
    if isfield(MODEL_sections, 'transv')
        % in case of GFDL model, transv is extracted from the model output then vecv must be calculated
        for s=1:length(MODEL_sections)
            MODEL_sections(s).vecv = 1e6 * MODEL_sections(s).transv./repmat(reshape(MODEL_sections(s).areavect, [1 size(MODEL_sections(s).areavect, 1) size(MODEL_sections(s).areavect, 2)]), [size(MODEL_sections(s).transv, 1) 1 1]);
        end
    else
        for s=1:length(MODEL_sections)
            MODEL_sections(s).vecv = NaN * ones(size(MODEL_sections(s).vect));
        end
    end
end

% in case the thickness of layers changes over time
if isfield(MODEL_sections, 'vech')
    vech = 1;
    if JDinputbin('is model outputs on isopycnic levels ? (0 or 1) ')
        isopycnic = 1;
    else
        isopycnic = 0;
    end
else
    vech = 0;
    isopycnic = 0;
end

if ~isopycnic
    % integral of tracers done for depth intervals also, defined as follows
    % for other depth intervals, it is possible to change the three variables below directly, but pay attention that the same variables defined in function indices_MODEL.m are modified accordingly
    lev1 = 500; % first depth interval from surface down to 500 m
    lev2 = 1000; % second depth interval from 500 m down to 1000 m
    lev3 = 2000; % third depth interval from 1000 m down to 2000 m
    % fourth depth interval from 2000 m down to bottom

    % identifies the vertical levels that correspond to the depth intervals
    for l=1:length(MODEL_sections(1).veci)
        temp = find((abs(cumsum(MODEL_sections(1).depthvect(:, l))) <= lev1) & (MODEL_sections(1).depthvect(:, l) ~= 0));
        if isempty(temp)
            zlev1(l) = 1;
        else
            zlev1(l) = temp(end);
        end
        temp = find((abs(cumsum(MODEL_sections(1).depthvect(:, l))) <= lev2) & (MODEL_sections(1).depthvect(:, l) ~= 0));
        if isempty(temp)
            zlev2(l) = max(min(nz, zlev1(l) + 1), 1);
        else
            zlev2(l) = max(min(nz, zlev1(l) + 1), temp(end));
        end
        temp = find((abs(cumsum(MODEL_sections(1).depthvect(:, l))) <= lev3) & (MODEL_sections(1).depthvect(:, l) ~= 0));
        if isempty(temp)
            zlev3(l) = max(min(nz, zlev2(l) + 1), 1);
        else
            zlev3(l) = max(min(nz, zlev2(l) + 1), temp(end));
        end
    end
    % vertical level is constant along the section and the same for all sections
    % ie we neglect partial steps and z-star effects
    zlev1 = max(zlev1);
    zlev2 = max(zlev2);
    zlev3 = max(zlev3);

    disp('Volume diagnostics give indices for the following depth intervals:')
    disp(['surface - ' num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev1, :), 1)))) 'm, which is represented by ' num2str(zlev1) ' levels, '])
    disp([num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev1, :), 1)))) 'm - ' num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev2, :), 1)))) 'm, which is represented by ' num2str(zlev2 - zlev1) ' levels, '])
    disp([num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev2, :), 1)))) 'm - ' num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev3, :), 1)))) 'm, which is represented by ' num2str(zlev3 - zlev2) ' levels, '])
    disp([num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev3, :), 1)))) 'm - bottom, which is represented by up to ' num2str(nz - zlev3) ' levels.'])
end % if ~isopycnic

% beginning of the calculation, for each area
for area=1:length(MODEL_area)
    disp(['volumetric census for area ' MODEL_area(area).name])
    S0 = 34.8; % reference salinity for freshwater budget calculation
    disp([' Freshwater calculations based on reference salinity of ' num2str(S0) ])

    time = MODEL_time;

    % beginning of the loop for each time step
    for t=1:nt
        if isfield(MODEL_area, 'volt')    % in case of GFDL model, the thickness of each layer changes in time and is stored in MODEL_area.volt
            volume = squeeze(MODEL_area(area).volt(t, :, :));
            volume(find(MODEL_area(area).volume == 0)) = NaN;
        else
            volume = MODEL_area(area).volume;
            volume(find(isnan(squeeze(MODEL_area(area).salinity(t, :, :))))) = NaN;
            volume(find(isnan(squeeze(MODEL_area(area).temperature(t, :, :))))) = NaN;
        end

        salinity = squeeze(MODEL_area(area).salinity(t, :, :));
        salinity(find(MODEL_area(area).volume == 0)) = NaN;
        temperature = squeeze(MODEL_area(area).temperature(t, :, :));
        temperature(find(MODEL_area(area).volume == 0)) = NaN;

        MODEL_volume(area).sc(t) = nansum(nansum(salinity.*volume)); % salt content in psu*m3
        MODEL_volume(area).S0c(t) = nansum(nansum(S0.*volume.*~isnan(salinity(:, :))));
        MODEL_volume(area).hc(t) = 4.186e6 * nansum(nansum(temperature.*volume)); % heat content in J

        MODEL_volume(area).min(t) = 0;
        MODEL_volume(area).sin(t) = 0;
        MODEL_volume(area).hin(t) = 0;
        MODEL_volume(area).fin(t) = 0;

        if ~isopycnic
            MODEL_volume(area).sc1(t) = nansum(nansum(salinity(1:zlev1, :).*volume(1:zlev1, :)));
            MODEL_volume(area).sc2(t) = nansum(nansum(salinity(zlev1 + 1:zlev2, :).*volume(zlev1 + 1:zlev2, :)));
            MODEL_volume(area).sc3(t) = nansum(nansum(salinity(zlev2 + 1:zlev3, :).*volume(zlev2 + 1:zlev3, :)));
            MODEL_volume(area).S0c1(t) = nansum(nansum(S0.*volume(1:zlev1, :).*~isnan(salinity(1:zlev1, :))));
            MODEL_volume(area).S0c2(t) = nansum(nansum(S0.*volume(zlev1 + 1:zlev2, :).*~isnan(salinity(zlev1 + 1:zlev2, :))));
            MODEL_volume(area).S0c3(t) = nansum(nansum(S0.*volume(zlev2 + 1:zlev3, :).*~isnan(salinity(zlev2 + 1:zlev3, :))));
            MODEL_volume(area).hc1(t) = 4.186e6 * nansum(nansum(temperature(1:zlev1, :).*volume(1:zlev1, :)));
            MODEL_volume(area).hc2(t) = 4.186e6 * nansum(nansum(temperature(zlev1 + 1:zlev2, :).*volume(zlev1 + 1:zlev2, :)));
            MODEL_volume(area).hc3(t) = 4.186e6 * nansum(nansum(temperature(zlev2 + 1:zlev3, :).*volume(zlev2 + 1:zlev3, :)));

            MODEL_volume(area).s1in(t) = 0;
            MODEL_volume(area).s2in(t) = 0;
            MODEL_volume(area).s3in(t) = 0;
            MODEL_volume(area).h1in(t) = 0;
            MODEL_volume(area).h2in(t) = 0;
            MODEL_volume(area).h3in(t) = 0;
            MODEL_volume(area).f1in(t) = 0;
            MODEL_volume(area).f2in(t) = 0;
            MODEL_volume(area).f3in(t) = 0;
        end

        if isfield(MODEL_area, 'serr')
                serr = squeeze(MODEL_area(area).serr(t, :, :));
                serr(find(isnan(salinity))) = NaN;
                MODEL_volume(area).serr(t) = nansum(nansum(serr.*volume)); % psu*m3
        end

        % convergence of tracer transport at the boundaries of the area
        for l=1:length(vecsecin(area).sec)
            sec = vecsecin(area).sec(l);
            if vech
                MODEL_sections(sec).depthvect = squeeze(MODEL_sections(sec).vech(t, :, :));
                MODEL_sections(sec).depthvect(find(isnan(MODEL_sections(sec).depthvect))) = 0;
                MODEL_sections(sec).areavect = repmat(MODEL_sections(sec).lengthvect, [size(MODEL_sections(sec).depthvect, 1) 1]).*MODEL_sections(sec).depthvect;
            end
            MODEL_volume(area).min(t) = MODEL_volume(area).min(t) + vecsecin(area).sign(l) * 1e-6 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, :, :)).*MODEL_sections(sec).areavect)); % Sv
            MODEL_volume(area).sin(t) = MODEL_volume(area).sin(t) + vecsecin(area).sign(l) * 1e-6 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, :, :).*MODEL_sections(sec).vecs(t, :, :)).*MODEL_sections(sec).areavect)); % psu * Sv
            MODEL_volume(area).hin(t) = MODEL_volume(area).hin(t) + vecsecin(area).sign(l) * 4.186e6 * 1e-15 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, :, :).*MODEL_sections(sec).vect(t, :, :)).*MODEL_sections(sec).areavect)); % PW
            MODEL_volume(area).fin(t) = MODEL_volume(area).fin(t) + vecsecin(area).sign(l) * 1e-3 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, :, :).*(S0 - MODEL_sections(sec).vecs(t, :, :))/S0).*MODEL_sections(sec).areavect)); % mSv
            if ~isopycnic
                MODEL_volume(area).s1in(t) = MODEL_volume(area).s1in(t) + vecsecin(area).sign(l) * 1e-6 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, 1:zlev1, :).*MODEL_sections(sec).vecs(t, 1:zlev1, :)).*MODEL_sections(sec).areavect(1:zlev1, :)));
                MODEL_volume(area).s2in(t) = MODEL_volume(area).s2in(t) + vecsecin(area).sign(l) * 1e-6 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, zlev1 + 1:zlev2, :).*MODEL_sections(sec).vecs(t, zlev1 + 1:zlev2, :)).*MODEL_sections(sec).areavect(zlev1 + 1:zlev2, :)));
                MODEL_volume(area).s3in(t) = MODEL_volume(area).s3in(t) + vecsecin(area).sign(l) * 1e-6 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, zlev2 + 1:zlev3, :).*MODEL_sections(sec).vecs(t, zlev2 + 1:zlev3, :)).*MODEL_sections(sec).areavect(zlev2 + 1:zlev3, :)));
                MODEL_volume(area).h1in(t) = MODEL_volume(area).h1in(t) + vecsecin(area).sign(l) * 4.186e6 * 1e-15 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, 1:zlev1, :).*MODEL_sections(sec).vect(t, 1:zlev1, :)).*MODEL_sections(sec).areavect(1:zlev1, :)));
                MODEL_volume(area).h2in(t) = MODEL_volume(area).h2in(t) + vecsecin(area).sign(l) * 4.186e6 * 1e-15 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, zlev1 + 1:zlev2, :).*MODEL_sections(sec).vect(t, zlev1 + 1:zlev2, :)).*MODEL_sections(sec).areavect(zlev1 + 1:zlev2, :)));
                MODEL_volume(area).h3in(t) = MODEL_volume(area).h3in(t) + vecsecin(area).sign(l) * 4.186e6 * 1e-15 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, zlev2 + 1:zlev3, :).*MODEL_sections(sec).vect(t, zlev2 + 1:zlev3, :)).*MODEL_sections(sec).areavect(zlev2 + 1:zlev3, :)));
                MODEL_volume(area).f1in(t) = MODEL_volume(area).f1in(t) + vecsecin(area).sign(l) * 1e-3 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, 1:zlev1, :).*(S0 - MODEL_sections(sec).vecs(t, 1:zlev1, :))/S0).*MODEL_sections(sec).areavect(1:zlev1, :)));
                MODEL_volume(area).f2in(t) = MODEL_volume(area).f2in(t) + vecsecin(area).sign(l) * 1e-3 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, zlev1 + 1:zlev2, :).*(S0 - MODEL_sections(sec).vecs(t, zlev1 + 1:zlev2, :))/S0).*MODEL_sections(sec).areavect(zlev1 + 1:zlev2, :)));
                MODEL_volume(area).f3in(t) = MODEL_volume(area).f3in(t) + vecsecin(area).sign(l) * 1e-3 * nansum(nansum(squeeze(MODEL_sections(sec).vecv(t, zlev2 + 1:zlev3, :).*(S0 - MODEL_sections(sec).vecs(t, zlev2 + 1:zlev3, :))/S0).*MODEL_sections(sec).areavect(zlev2 + 1:zlev3, :)));
            end %if ~isopycnic
        end

        % we keep track of integral of volume for each area in case it changes in time (cf GFDL model)
        MODEL_volume(area).vol(t) = nansum(nansum(volume));
        if ~isopycnic
            MODEL_volume(area).vol1(t) = nansum(nansum(volume(1:zlev1, :)));
            MODEL_volume(area).vol2(t) = nansum(nansum(volume(zlev1 + 1:zlev2, :)));
            MODEL_volume(area).vol3(t) = nansum(nansum(volume(zlev2 + 1:zlev3, :)));
        end
    end
    % end of loop on time

    % we save constant information for each area
    MODEL_volume(area).time = time;
    MODEL_volume(area).name = MODEL_area(area).name;
    MODEL_volume(area).indi = MODEL_area(area).indi;
    MODEL_volume(area).indj = MODEL_area(area).indj;
    MODEL_volume(area).surf = sum(MODEL_area(area).surface); % surface of the area at the top level in m2

end
% end of loop on area
