function [MODEL_indices] = indices_MODEL(structfile, varargin)
%INDICES_MODEL calculates diagnostics of circulation across sections
%
% DESCRIPTION
%
% calculates diagnostics of circulation across sections, see website
% for a description of those diagnostics.
%
% output: MODEL_indices, is a structure that contains all indices, which can be time series (1d) or 2d matrices, calculated on each time step included in structfile given as argument
%
% no additional argument: indices are calculated for a set of sections to be decided by user
% with additional argument 1: default sections for the North Atlantic
% with additional argument 2: default sections for the global ocean.
% units are as follows: volume transports (Sv), heat transports (PW), and freshwater transports (mSv)
%
% EXAMPLES
%
%   See also NANMAX, NANMEAN, NANSUM, INDICES_MODEL
%
% TODO
% if 0 % not available yet... isopycnic
% see website : replace with the precise page
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO
%
% JD PAGO --- modified on May, 8th 2012

load(structfile)

% choice of sections where full diagnostics will be calculated
if not(isempty(varargin))
    switch cell2mat(varargin(1))
        case 1 % diagnostics for North Atlantic
             vecfull_allnames = ['42n a25 ar7 nos ovi 26n'];
        case 2 % diagnostics for GL
             %vecfull_allnames = ['A4N A2N A3S'];
             vecfull_allnames = ['A4N A2N A3S ITF P2N P4N P1N P1S P3S P4S DRA AUS DSO ISO FRA MOZ BER AAF I9W I9E I3S'];
    end
    disp(['full diagnostics on sections: ' vecfull_allnames])
else
    if input('standard choice of sections in North Atlantic for full diagnostics? (0 or 1) ')
        vecfull_allnames = ['42n a25 ar7 nos ovi 26n'];
        disp(['full diagnostics on sections: ' vecfull_allnames])
    else
        for sec=1:length(MODEL_sections)
            disp(MODEL_sections(sec).name)
        end
        vecfull_allnames = input('enter list of sections to run full diagnostics (list of names separated by space, or "all" otherwise): ','s');
    end
end
vecfull = [];
if not(isempty(vecfull_allnames))
    if length(vecfull_allnames) == 3 & strcmp(vecfull_allnames, 'all')
        vecfull = [1:length(MODEL_sections)]';
    else
        temp = find(strcmp(vecfull_allnames, ' '));
        temp = cat(2, 0, temp);
        for ind=1:length(temp)
            vecfull = cat(1, vecfull, findsecnum(MODEL_sections, vecfull_allnames(temp(ind) + 1:temp(ind) + 3)));
        end
    end
end

% choice of sections where simple diagnostics will be calculated
if not(isempty(varargin))
    switch cell2mat(varargin(1))
        case 1 % diagnostics for North Atlantic
            vecnet_allnames = ['bar non hud baf dso ifo fso its mdn'];
        case 2 % diagnostics for GL
             %vecnet_allnames = ['ITF P2N P4N P1N P1S P3S P4S DRA AUS DSO ISO FRA MOZ BER AAF I9W I9E I3S'];
             vecnet = [];
    end
    disp(['simple diagnostics on sections: ' vecnet_allnames])
else
    if input('standard choice of sections in North Atlantic for simple diagnostics (net heat, salt and freshwater flux)? (0 or 1) ')
        vecnet_allnames = ['bar non hud baf dso ifo fso its mdn'];
        disp(['simple diagnostics on sections: ' vecnet_allnames])
    else
        for sec=1:length(MODEL_sections)
            disp(MODEL_sections(sec).name)
        end
        vecnet_allnames = input('enter list of sections to run simple diagnostics (list of names separated by space, or "all" otherwise): ','s');
    end
end
vecnet = [];
if not(isempty(vecnet_allnames))
    if length(vecnet_allnames) == 3 & strcmp(vecnet_allnames, 'all')
        vecnet = [1:length(MODEL_sections)]';
    else
        temp = find(strcmp(vecnet_allnames, ' '));
        temp = cat(2, 0, temp);
        for ind=1:length(temp)
            vecnet = cat(1, vecnet, findsecnum(MODEL_sections, vecnet_allnames(temp(ind) + 1:temp(ind) + 3)));
        end
    end
end

% combines the list of sections to calculate diagnostics
[vecall, ind] = sort(cat(1, vecfull, vecnet));
temp = cat(1, ones(length(vecfull), 1), zeros(length(vecnet), 1));
diagfull = temp(ind);
diagfull = cat(1, diagfull(1), diagfull(1 + find(diff(vecall) > 0)));
vecall = cat(1, vecall(1), vecall(1 + find(diff(vecall) > 0)));

% default parameters for isopycnic projection
S0 = 34.8; % reference salinity for freshwater calculations
disp(['Freshwater calculations based on reference salinity of ' num2str(S0) '.'])
sigma0_vec1 = [24;24.4;24.9;25.4;25.9;26.4;26.75;27.05;27.30;27.45;27.58;27.68;27.75;27.80;27.83;27.86;27.89;27.92;27.95;27.98;28.01;28.04;28.07;28.1;28.6;29.1];
sigma0_vec2 = [24;24.2;24.4;24.65;24.9;25.15;25.4;25.65;25.9;16.15;26.4;16.57;26.75;26.90;27.05;27.17;27.30;27.37;27.45;27.52;27.58;27.63;27.68;27.72;27.75;27.78;...
    27.80;27.815;27.83;27.845;27.86;27.875;27.89;27.905;27.92;27.935;27.95;27.965;27.98;27.99;28.01;28.025;28.04;28.055;28.07;28.085;28.1;28.35;28.6;28.8;29.1];
sigma2_vec = [34.4;34.6;34.8;35;35.2;35.4;36;36.4;36.6;36.7;36.8;36.9;36.95;37;37.05;37.1;37.15;37.2;37.4;37.6;38];
sigma1_vec = [29.68:.01:32.99:35]';


% diagnostics for depth intervals also, defined as follows
% for other depth intervals, it is possible to change the three variables below directly, but pay attention that the same variables defined in function volumes_MODEL.m are modified accordingly
lev1 = 500; % first depth interval from surface down to 500 m
lev2 = 1000; % second depth interval from 500 m down to 1000 m
lev3 = 2000; % third depth interval from 1000 m down to 2000 m
% fourth depth interval from 2000 m down to bottom
% also modify load_definition.m accordingly so that the netcdf output file has correct attribute

% identifies the vertical levels that correspond to the depth intervals
[nt, nz, nl] = size(MODEL_sections(1).vect);

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
zlev1_cst = max(zlev1);
zlev2_cst = max(zlev2);
zlev3_cst = max(zlev3);

if not(isempty(vecfull))
    disp('Full diagnostics give transports for the following depth intervals:')
    disp(['surface - ' num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev1_cst, :), 1)))) 'm, which is represented by up to ' num2str(zlev1_cst) ' levels,'])
    disp([num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev1_cst, :), 1)))) 'm - ' num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev2_cst, :), 1)))) 'm, which is represented by up to ' num2str(zlev2_cst - zlev1_cst) ' levels, '])
    disp([num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev2_cst, :), 1)))) 'm - ' num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev3_cst, :), 1)))) 'm, which is represented by up to ' num2str(zlev3_cst - zlev2_cst) ' levels, '])
    disp([num2str(floor(max(sum(MODEL_sections(1).depthvect(1:zlev3_cst, :), 1)))) 'm - bottom, which is represented by up to ' num2str(nz - zlev3_cst) ' levels.'])
end

% identifies density limits to calculate transport integrated in density bin
if nargin == 0
    if not(isempty(vecfull))
        if input('do you want to calculated transport integrated over density bin? (0 or 1)')
            disp('please select the type of potential density to define the limits of the density bin')
            stype = input('(type 0 for sigma-0, 1 for sigma-1, 2 for sigma-2): ');
            disp('now enter the limits for the density bin (densities are in the range 24-40 kg/m3)')
            smin = input('enter the lower limit for the density bin ');
            smax = input('enter the upper limit for the density bin ');
            if smin > smax
                temp = smin;
                smin = smax;
                smax = temp;
            end
        else
            stype = NaN;
            smin = NaN;
            smax = NaN;
        end
    end
end

% in case transv is extracted from the model output then vecv must be calculated
if ~isfield(MODEL_sections, 'vecv')
    for s=1:length(vecall)
        if ndims(MODEL_sections(vecall(s)).transv) > 2
            MODEL_sections(vecall(s)).vecv = 1e6 * MODEL_sections(vecall(s)).transv./repmat(reshape(MODEL_sections(vecall(s)).areavect, [1 size(MODEL_sections(ivecall(s)).areavect, 1) size(MODEL_sections(vecall(s)).areavect, 2)]), [size(MODEL_sections(vecall(s)).transv, 1) 1 1]);
        else
            MODEL_sections(vecall(s)).vecv = 1e6 * MODEL_sections(vecall(s)).transv./MODEL_sections(vecall(s)).areavect;
        end
    end
end

% in case the thickness of layers changes over time
if isfield(MODEL_sections, 'vech')
    vech = 1;
    if JDinputbin('is model outputs on isopycnic levels ? (0 or 1) ')
%        refdens = input('please indicate which potential density is used: enter s0 (referenced to the surface), s1 or s2 ... ', 's');
        isopycnic = 1;
    else
        isopycnic = 0;
    end
%    disp(['for few diagnostics that require a z-level discretization, isopycnic velocities are interpolated on fixed z-levels located in the middle of temporal-mean layers'] % development still ongoing...
%    for s=1:length(vecall)
        %depthvect_lmean = squeeze(nanmean(MODEL_sections(vecall(s)).depthvect, 2));
        %PROJ_sections(vecall(s)).zlev(1) = 0.5 * depthvect_lmean(1);
        %for z=2:nz
        %    PROJ_sections(vecall(s)).zlev(z) = PROJ_sections(vecall(s)).zlev(z - 1) + 0.5 * depthvect_lmean(z - 1) + 0.5 * depthvect_lmean(z);
        %end
        %PROJ_sections(vecall(s)).vecv = iso_proj_zlev(MODEL_sections(vecall(s)).vecv, MODEL_sections(vecall(s)).vech, PROJ_sections(vecall(s)).zlev);
%    end
else
    vech = 0;
    isopycnic = 0;
end

% beginning of calculation, for each section
for s=1:length(vecall)
    disp(['analysing section ' MODEL_sections(vecall(s)).name ])
    MODEL_indices(s).name = MODEL_sections(vecall(s)).name;
    if exist('MODEL_time', 'var')
        MODEL_indices(s).time = MODEL_time;
        [nt, nz, nl] = size(MODEL_sections(vecall(s)).vecv);
    else
        nt = 1;
        [nz, nl] = size(MODEL_sections(vecall(s)).vecv);
        MODEL_sections(vecall(s)).vecv = reshape(MODEL_sections(vecall(s)).vecv, [1 nz nl]);
        MODEL_sections(vecall(s)).vect = reshape(MODEL_sections(vecall(s)).vect, [1 nz nl]);
        MODEL_sections(vecall(s)).vecs = reshape(MODEL_sections(vecall(s)).vecs, [1 nz nl]);
    end
    vecv_nonet = zeros(nz, nl);
    vect_nonet = zeros(nz, nl);
    clear bpmt_vec mt1_vec mt2_vec mt3_vec thwnd1_vec thwnd2_vec

    % beginning of the loop for each time step
    for t=1:nt
        vecT_iso_s0_1 = zeros(length(sigma0_vec1), nl);
        vecT_iso_s0_2 = zeros(length(sigma0_vec2), nl);
        vecT_iso_s2 = zeros(length(sigma2_vec), nl);
        vecT_iso_s1 = zeros(length(sigma1_vec), nl);
        vect_iso_s0_1 = zeros(length(sigma0_vec1), nl);
        vect_iso_s0_2 = zeros(length(sigma0_vec2), nl);
        vect_iso_s2 = zeros(length(sigma2_vec), nl);
        vect_iso_s1 = zeros(length(sigma1_vec), nl);
        vecf_iso_s0_1 = zeros(length(sigma0_vec1), nl);
        vecf_iso_s0_2 = zeros(length(sigma0_vec2), nl);
        vecf_iso_s2 = zeros(length(sigma2_vec), nl);
        vecf_iso_s1 = zeros(length(sigma1_vec), nl);
        vecT_iso_bin = 0;
        vect_iso_bin = 0;
        vecf_iso_bin = 0;
        denom_iso_s0_1 = zeros(length(sigma0_vec1), nl);
        denom_iso_s0_2 = zeros(length(sigma0_vec2), nl);
        denom_iso_s2 = zeros(length(sigma2_vec), nl);
        denom_iso_s1 = zeros(length(sigma1_vec), nl);
        if vech
            MODEL_sections(vecall(s)).depthvect = squeeze(MODEL_sections(vecall(s)).vech(t, :, :));
            MODEL_sections(vecall(s)).depthvect(find(isnan(MODEL_sections(vecall(s)).depthvect))) = 0;
            MODEL_sections(vecall(s)).areavect = repmat(MODEL_sections(vecall(s)).lengthvect, [size(MODEL_sections(vecall(s)).depthvect, 1) 1]).*MODEL_sections(vecall(s)).depthvect;
        end
        areavect = MODEL_sections(vecall(s)).areavect;
        areavect(find(isnan(squeeze(MODEL_sections(vecall(s)).vecv(t, :, :))))) = NaN;
        areavect(find(isnan(squeeze(MODEL_sections(vecall(s)).vect(t, :, :))))) = NaN;

        % net transport of mass (Sv), heat (PW), salinity (psu*Sv), freshwater (mSv)
        MODEL_indices(s).netmt(t) = 1e-6 * nansum(nansum(squeeze(MODEL_sections(vecall(s)).vecv(t, :, :)).*areavect));
        MODEL_indices(s).netht(t) = 4.186e6 * 1e-15 * nansum(nansum(squeeze(MODEL_sections(vecall(s)).vecv(t, :, :).*MODEL_sections(vecall(s)).vect(t, :, :)).*areavect));
        MODEL_indices(s).netst(t) = 1e-6 * nansum(nansum(squeeze(MODEL_sections(vecall(s)).vecv(t, :, :).*MODEL_sections(vecall(s)).vecs(t, :, :)).*areavect));
        MODEL_indices(s).netft(t) = 1e-3 * nansum(nansum(squeeze(MODEL_sections(vecall(s)).vecv(t, :, :).*(S0 - MODEL_sections(vecall(s)).vecs(t, :, :))/S0).*areavect));

        % total heat (PW), salinity (psu*Sv) and freshwater (mSv) transport without the net mass transport
        vecv_nonet = squeeze(MODEL_sections(vecall(s)).vecv(t, :, :)) - 1e6 * MODEL_indices(s).netmt(t)/nansum(nansum(areavect));
        MODEL_indices(s).totht(t) = 4.186e6 * 1e-15 * nansum(nansum(vecv_nonet.*squeeze(MODEL_sections(vecall(s)).vect(t, :, :)).*areavect));
        MODEL_indices(s).totst(t) = 1e-6 * nansum(nansum(vecv_nonet.*squeeze(MODEL_sections(vecall(s)).vecs(t, :, :)).*areavect));
        MODEL_indices(s).totft(t) = 1e-3 * nansum(nansum(vecv_nonet.*squeeze(S0 - MODEL_sections(vecall(s)).vecs(t, :, :))/S0.*areavect));
        vect_nonet = squeeze(MODEL_sections(vecall(s)).vect(t, :, :)) - nansum(nansum(squeeze(MODEL_sections(vecall(s)).vect(t, :, :)).*areavect))/nansum(nansum(areavect));
        vecf_nonet = -(squeeze(MODEL_sections(vecall(s)).vecs(t, :, :)) - nansum(nansum(squeeze(MODEL_sections(vecall(s)).vecs(t, :, :)).*areavect))/nansum(nansum(areavect)))/S0;

        % overturning components in z coordinates
        if ~vech
            vecv_ov = nansum(vecv_nonet.*areavect, 2)./nansum(areavect, 2);
            vect_ov = nansum(vect_nonet.*areavect, 2)./nansum(areavect, 2);
            vecf_ov = nansum(vecf_nonet.*areavect, 2)./nansum(areavect, 2);
            vecv_ov(find(vecv_ov == 0)) = NaN;
            [val, ind] = nanmax(cumsum(vecv_ov.*nansum(areavect, 2)));
            MODEL_indices(s).ovmt(t) = 1e-6 * val; % overturning mass transport (Sv)
            MODEL_indices(s).dpmt(t) = nanmean(nansum(MODEL_sections(vecall(s)).depthvect(1:ind, :), 1));
            MODEL_indices(s).ovht(t) = 4.186e6 * 1e-15 * nansum(vecv_ov.*vect_ov.*nansum(areavect, 2)); % overturning heat transport (PW)
            MODEL_indices(s).ovft(t) = 1e-3 * nansum(vecv_ov.*vecf_ov.*nansum(areavect, 2)); % overturning transport of freshwater (mSv)
        else
            if 0 % not available yet... isopycnic
                 % in NorESM outputs there is a mixed layer which transport has to be distributed in the layers below
                vecv_ov = nansum(vecv_nonet.*areavect, 2)./nansum(areavect, 2); % overturning in density space here
                vect_ov = nansum(vect_nonet.*areavect, 2)./nansum(areavect, 2);
                vecf_ov = nansum(vecf_nonet.*areavect, 2)./nansum(areavect, 2);
                vecv_ov(find(isnan(vecv_ov))) = 0;
                [val, ind] = nanmax(cumsum(vecv_ov.*nansum(areavect, 2), 1));
                switch refdens
                    case 's0'
                        MODEL_indices(s).ovrmt_s0_1(t) = 1e-6 * val; % overturning mass transport (Sv)
                        MODEL_indices(s).ovrht_s0_1(t) = 4.186e8 * 1e-15 * nansum(vecv_ov.*vect_ov.*nansum(areavect, 2)); % overturning heat transport (PW)
                        MODEL_indices(s).ovrft_s0_1(t) = 1e-3 * nansum(vecv_ov.*vecf_ov.*nansum(areavect, 2)); % overturning transport of freshwater (mSv)
                    case 's1'
                        MODEL_indices(s).ovrmt_s1(t) = 1e-6 * val; % overturning mass transport (Sv)
                        MODEL_indices(s).ovrht_s1(t) = 4.186e8 * 1e-15 * nansum(vecv_ov.*vect_ov.*nansum(areavect, 2)); % overturning heat transport (PW)
                        MODEL_indices(s).ovrft_s1(t) = 1e-3 * nansum(vecv_ov.*vecf_ov.*nansum(areavect, 2)); % overturning transport of freshwater (mSv)
                    case 's2'
                        MODEL_indices(s).ovrmt_s2(t) = 1e-6 * val; % overturning mass transport (Sv)
                        MODEL_indices(s).ovrht_s2(t) = 4.186e8 * 1e-15 * nansum(vecv_ov.*vect_ov.*nansum(areavect, 2)); % overturning heat transport (PW)
                        MODEL_indices(s).ovrft_s2(t) = 1e-3 * nansum(vecv_ov.*vecf_ov.*nansum(areavect, 2)); % overturning transport of freshwater (mSv)
                end % switch refdens
            end % if isopycnic
        end % if ~vech

        if ~vech %|| isopycnic % activate option isopycnic once vecv_ov available
            % horizontal components
            vecv_ho = vecv_nonet - repmat(vecv_ov, [1 nl]);
            vect_ho = vect_nonet - repmat(vect_ov, [1 nl]);
            vecf_ho = vecf_nonet - repmat(vecf_ov, [1 nl]);
            % barotropic components from top to bottom
            vecv_bp = nansum(vecv_ho.*areavect, 1)./nansum(areavect, 1);
            vect_bp = nansum(vect_ho.*areavect, 1)./nansum(areavect, 1);
            vecf_bp = nansum(vecf_ho.*areavect, 1)./nansum(areavect, 1);
            res = vecv_bp.*nansum(areavect, 1);
            res(find(isnan(res))) = 0;
            MODEL_indices(s).bpmt_vec(t, :) = res;
            MODEL_indices(s).bpht(t) = 4.186e6 * 1e-15 * nansum(vecv_bp.*vect_bp.*nansum(areavect, 1)); % barotropic heat transport (PW)
            MODEL_indices(s).bpft(t) = 1e-3 * nansum(vecv_bp.*vecf_bp.*nansum(areavect, 1)); % barotropic transport of freshwater (mSv)
            % baroclinic components (total)
            vecv_bc = vecv_ho - repmat(vecv_bp, [nz 1]);
            vect_bc = vect_ho - repmat(vect_bp, [nz 1]);
            vecf_bc = vecf_ho - repmat(vecf_bp, [nz 1]);
            MODEL_indices(s).bcht(t) = 4.186e6 * 1e-15 * nansum(nansum(vecv_bc.*vect_bc.*areavect)); % baroclinic heat transport (PW)
            MODEL_indices(s).bcft(t) = 1e-3 * nansum(nansum(vecv_bc.*vecf_bc.*areavect)); % baroclinic transport of freshwater (mSv)
            % ok : bcht+bpht+ovht = totht
        end % if ~vech || isopycnic

        if diagfull(s)
            % overturning in density coordinates, associated heat and freshwater transport
            % only available for zlev data
            if ~vech
                for l=1:nl
                    for z=1:nz
                        res = vecv_nonet(z, l).*areavect(z, l);
                        rest = vect_nonet(z, l).*areavect(z, l);
                        resf = vecf_nonet(z, l).*areavect(z, l);
                        if isnan(res)
                            res = 0;
                        end
                        % in sigma0 coordinates, ie referenced to the surface - low resolution density bins
                        % dens = sw_dens(MODEL_sections(vecall(s)).vecs(t, z, l), MODEL_sections(vecall(s)).vect(t, z, l), 0)-1000; % using UNESCO 1983 (EOS 80) density of sea water
                        dens = eos_pot(MODEL_sections(vecall(s)).vect(t, z, l), MODEL_sections(vecall(s)).vecs(t, z, l), 0); % using Jackett and McDougall 1994 equation of state
                        class = whichclass(dens, sigma0_vec1);
                        if ~isnan(class)
                            vecT_iso_s0_1(class, l) = vecT_iso_s0_1(class, l) + res;
                            vect_iso_s0_1(class, l) = vect_iso_s0_1(class, l) + rest;
                            vecf_iso_s0_1(class, l) = vecf_iso_s0_1(class, l) + resf;
                            denom_iso_s0_1(class, l) = denom_iso_s0_1(class, l) + areavect(z, l);
                        end
                        % in sigma0 coordinates, ie referenced to the surface - high resolution density bins
                        class = whichclass(dens, sigma0_vec2);
                        if ~isnan(class)
                            vecT_iso_s0_2(class, l) = vecT_iso_s0_2(class, l) + res;
                            vect_iso_s0_2(class, l) = vect_iso_s0_2(class, l) + rest;
                            vecf_iso_s0_2(class, l) = vecf_iso_s0_2(class, l) + resf;
                            denom_iso_s0_2(class, l) = denom_iso_s0_2(class, l) + areavect(z, l);
                        end
                        if exist('stype', 'var')
                            if stype == 0
                                if smin < dens && dens <smax
                                    vecT_iso_bin = vecT_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*areavect(z, l);
                                    vect_iso_bin = vect_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*MODEL_sections(vecall(s)).vect(t, z, l).*areavect(z, l);
                                    vecf_iso_bin = vecf_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*(S0 - MODEL_sections(vecall(s)).vecs(t, z, l))/S0.*areavect(z, l);
                                end
                            end
                        end
                        % in sigma2 coordinates, ie referenced to 2000m depth
                        % dens = sw_dens(MODEL_sections(vecall(s)).vecs(t, z, l), MODEL_sections(vecall(s)).vect(t, z, l), 2000)-1000;% using UNESCO 1983 (EOS 80) density of sea water
                        dens = eos_pot(MODEL_sections(vecall(s)).vect(t, z, l), MODEL_sections(vecall(s)).vecs(t, z, l), 2000); % using Jackett and McDougall 1994 equation of state
                        class = whichclass(dens, sigma2_vec);
                        if ~isnan(class)
                            vecT_iso_s2(class, l) = vecT_iso_s2(class, l) + res;
                            vect_iso_s2(class, l) = vect_iso_s2(class, l) + rest;
                            vecf_iso_s2(class, l) = vecf_iso_s2(class, l) + resf;
                            denom_iso_s2(class, l) = denom_iso_s2(class, l) + areavect(z, l);
                        end
                        if exist('stype', 'var')
                            if stype == 2
                                if smin < dens && dens < smax
                                    vecT_iso_bin = vecT_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*areavect(z, l);
                                    vect_iso_bin = vect_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*MODEL_sections(vecall(s)).vect(t, z, l).*areavect(z, l);
                                    vecf_iso_bin = vecf_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*(S0 - MODEL_sections(vecall(s)).vecs(t, z, l))/S0.*areavect(z, l);
                                end
                            end
                        end
                        % in sigma1 coordinates, ie referenced to 1000m depth
                        % dens = sw_dens(MODEL_sections(vecall(s)).vecs(t, z, l), MODEL_sections(vecall(s)).vect(t, z, l), 1000)-1000;% using UNESCO 1983 (EOS 80) density of sea water
                        dens = eos_pot(MODEL_sections(vecall(s)).vect(t, z, l), MODEL_sections(vecall(s)).vecs(t, z, l), 1000); % using Jackett and McDougall 1994 equation of state
                        class = whichclass(dens, sigma1_vec);
                        if ~isnan(class)
                            vecT_iso_s1(class, l) = vecT_iso_s1(class, l) + res;
                            vect_iso_s1(class, l) = vect_iso_s1(class, l) + rest;
                            vecf_iso_s1(class, l) = vecf_iso_s1(class, l) + resf;
                            denom_iso_s1(class, l) = denom_iso_s1(class, l) + areavect(z, l);
                        end
                        if exist('stype', 'var')
                            if stype == 1
                                if smin < dens && dens < smax
                                    vecT_iso_bin = vecT_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*areavect(z, l);
                                    vect_iso_bin = vect_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*MODEL_sections(vecall(s)).vect(t, z, l).*areavect(z, l);
                                    vecf_iso_bin = vecf_iso_bin + MODEL_sections(vecall(s)).vecv(t, z, l).*(S0 - MODEL_sections(vecall(s)).vecs(t, z, l))/S0.*areavect(z, l);
                                end
                            end
                        end
                    end  % for l=1:nl
                end  % for z=1:nz
                vecT_iso_s0_1(find(vecT_iso_s0_1 == 0)) = NaN;
                [val, ind] = nanmax(cumsum(nansum(vecT_iso_s0_1, 2)));
                MODEL_indices(s).ovrmt_s0_1(t) = 1e-6 * val;
                MODEL_indices(s).dsmt_s0_1(t) = sigma0_vec1(ind);
                MODEL_indices(s).ovrht_s0_1(t) = 4.186e6 * 1e-15 * nansum(nansum(vecT_iso_s0_1.*vect_iso_s0_1./denom_iso_s0_1)); % PW
                MODEL_indices(s).ovrft_s0_1(t) = 1e-3 * nansum(nansum(vecT_iso_s0_1.*vecf_iso_s0_1./denom_iso_s0_1)); % mSv

                vecT_iso_s0_2(find(vecT_iso_s0_2 == 0)) = NaN;
                [val, ind] = nanmax(cumsum(nansum(vecT_iso_s0_2, 2)));
                MODEL_indices(s).ovrmt_s0_2(t) = 1e-6 * val;
                MODEL_indices(s).dsmt_s0_2(t) = sigma0_vec2(ind);
                MODEL_indices(s).ovrht_s0_2(t) = 4.186e6 * 1e-15 * nansum(nansum(vecT_iso_s0_2.*vect_iso_s0_2./denom_iso_s0_2));
                MODEL_indices(s).ovrft_s0_2(t) = 1e-3 * nansum(nansum(vecT_iso_s0_2.*vecf_iso_s0_2./denom_iso_s0_2));

                vecT_iso_s2(find(vecT_iso_s2 == 0)) = NaN;
                [val, ind] = nanmax(cumsum(nansum(vecT_iso_s2, 2)));
                MODEL_indices(s).ovrmt_s2(t) = 1e-6 * val;
                MODEL_indices(s).dsmt_s2(t) = sigma2_vec(ind);
                MODEL_indices(s).ovrht_s2(t) = 4.186e6 * 1e-15 * nansum(nansum(vecT_iso_s2.*vect_iso_s2./denom_iso_s2));
                MODEL_indices(s).ovrft_s2(t) = 1e-3 * nansum(nansum(vecT_iso_s2.*vecf_iso_s2./denom_iso_s2));

                vecT_iso_s1(find(vecT_iso_s1 == 0)) = NaN;
                [val, ind] = nanmax(cumsum(nansum(vecT_iso_s1, 2)));
                MODEL_indices(s).ovrmt_s1(t) = 1e-6 * val;
                MODEL_indices(s).dsmt_s1(t) = sigma1_vec(ind);
                MODEL_indices(s).ovrht_s1(t) = 4.186e6 * 1e-15 * nansum(nansum(vecT_iso_s1.*vect_iso_s1./denom_iso_s1));
                MODEL_indices(s).ovrft_s1(t) = 1e-3 * nansum(nansum(vecT_iso_s1.*vecf_iso_s1./denom_iso_s1));

                MODEL_indices(s).mt_bin(t) = 1e-6 * vecT_iso_bin;
                MODEL_indices(s).ht_bin(t) = 4.186e6 * 1e-15 * vect_iso_bin;
                MODEL_indices(s).ft_bin(t) = 1e-3 * vecf_iso_bin;

                % mass and heat transports for depth intervals
                % + mass transport from thermal wind, ie with reference 0 velocity at lower level of depth interval

                clear mt1_res ht1_res mt2_res ht2_res mt3_res ht3_res drhodl coriolis

                vecv = squeeze(MODEL_sections(vecall(s)).vecv(t, :, :));
                vect = squeeze(MODEL_sections(vecall(s)).vect(t, :, :));
                vecs = squeeze(MODEL_sections(vecall(s)).vecs(t, :, :));
                zlev1 = zlev1_cst * ones(1, nl);
                zlev2 = zlev2_cst * ones(1, nl);
                zlev3 = zlev3_cst * ones(1, nl);
                for l=1:nl
                    MODEL_indices(s).mt1_vec(t, l) = nansum(vecv(1:zlev1(l), l).*areavect(1:zlev1(l), l), 1);
                    ht1_res(l) = 4.186e6 * 1e-15 * nansum(vecv(1:zlev1(l), l).*vect(1:zlev1(l), l).*areavect(1:zlev1(l), l), 1);
                    ft1_res(l) = 1e-3 * nansum(vecv(1:zlev1(l), l).*(S0 - vecs(1:zlev1(l), l))/S0.*areavect(1:zlev1(l), l), 1);
                    MODEL_indices(s).thwnd1_vec(t, l) = nansum((vecv(1:zlev1(l), l) - vecv(zlev1(l), l)).*areavect(1:zlev1(l), l), 1);

                    MODEL_indices(s).mt2_vec(t, l) = nansum(vecv(zlev1(l) + 1:zlev2(l), l).*areavect(zlev1(l) + 1:zlev2(l), l), 1);
                    ht2_res(l) = 4.186e6 * 1e-15 *nansum(vecv(zlev1(l) + 1:zlev2(l), l).*vect(zlev1(l) + 1:zlev2(l), l).*areavect(zlev1(l) + 1:zlev2(l), l), 1);
                    ft2_res(l) = 1e-3 * nansum(vecv(zlev1(l) + 1:zlev2(l), l).*(S0 - vecs(zlev1(l) + 1:zlev2(l), l))/S0.*areavect(zlev1(l) + 1:zlev2(l), l), 1);
                    MODEL_indices(s).thwnd2_vec(t, l) = nansum((vecv(zlev1(l) + 1:zlev2(l), l) - vecv(zlev2(l), l)).*areavect(zlev1(l) + 1:zlev2(l), l), 1);

                    MODEL_indices(s).mt3_vec(t, l) = nansum(vecv(zlev2(l) + 1:zlev3(l), l).*areavect(zlev2(l) + 1:zlev3(l), l), 1);
                    ht3_res(l) = 4.186e6 * 1e-15 * nansum(vecv(zlev2(l) + 1:zlev3(l), l).*vect(zlev2(l) + 1:zlev3(l), l).*areavect(zlev2(l) + 1:zlev3(l), l), 1);
                    ft3_res(l) = 1e-3 * nansum(vecv(zlev2(l) + 1:zlev3(l), l).*(S0 - vecs(zlev2(l) + 1:zlev3(l), l))/S0.*areavect(zlev2(l) + 1:zlev3(l), l), 1);
                    MODEL_indices(s).thwnd3_vec(t, l) = nansum((vecv(zlev2(l) + 1:zlev3(l), l) - vecv(zlev3(l), l)).*areavect(zlev2(l) + 1:zlev3(l), l), 1);

                    if zlev3(l) < nz
                        MODEL_indices(s).mt4_vec(t, l) = nansum(vecv(zlev3(l) + 1:nz, l).*areavect(zlev3(l) + 1:nz, l), 1);
                        ht4_res(l) = 4.186e6 * 1e-15 * nansum(vecv(zlev3(l) + 1:nz, l).*vect(zlev3(l) + 1:nz, l).*areavect(zlev3(l) + 1:nz, l), 1);
                        ft4_res(l) = 1e-3 * nansum(vecv(zlev3(l) + 1:nz, l).*(S0 - vecs(zlev3(l) + 1:nz, l))/S0.*areavect(zlev3(l) + 1:nz, l), 1);
                    else
                        MODEL_indices(s).mt4_vec(t, l) = 0;
                        ht4_res(l) = 0;
                        ft4_res(l) = 0;
                    end
                end % for l=1:nl
                MODEL_indices(s).ht1(t) = nansum(ht1_res);
                MODEL_indices(s).ht2(t) = nansum(ht2_res);
                MODEL_indices(s).ht3(t) = nansum(ht3_res);
                MODEL_indices(s).ht4(t) = nansum(ht4_res);
                MODEL_indices(s).ft1(t) = nansum(ft1_res);
                MODEL_indices(s).ft2(t) = nansum(ft2_res);
                MODEL_indices(s).ft3(t) = nansum(ft3_res);
                MODEL_indices(s).ft4(t) = nansum(ft4_res);

                %ok : ht1+ht2+ht3 = totht
            end %if vech
        end %if diagfull(s)
    end % for t=1:nt
end % for s
