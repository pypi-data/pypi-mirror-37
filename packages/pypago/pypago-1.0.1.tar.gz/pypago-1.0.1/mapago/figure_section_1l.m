function [] = figure_section_1l(structfile, secplot)
%FIGURE_SECTION_1L
%
% DESCRIPTION
% FIGURE_SECTION_1L plots the mean characteristics stored in structfile along a chosen section and prints figure
%
% EXAMPLES
%
%    figure_section_1l(structfile, secplot);
%
%   See also <https://sourcesup.renater.fr/pago/sections.html>
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO


% JD PAGO WHOI

load(structfile);

if nargin == 1
    disp('available sections:')
    for sec=1:length(MODEL_sections)
        disp( MODEL_sections(sec).name)
    end
    secplotname = input('enter section to draw: ', 's');
    secplot = findsecnum(MODEL_sections, secplotname);
end

if isfield(MODEL_sections, 'vecv')
    vecv = 1;
else
    if isfield(MODEL_sections, 'transv')
        s = secplot;
        MODEL_sections(s).vecv = 1e6 * MODEL_sections(s).transv./repmat(reshape(MODEL_sections(s).areavect, [1 size(MODEL_sections(s).areavect, 1) size(MODEL_sections(s).areavect, 2)]), [size(MODEL_sections(s).transv, 1) 1 1]);
        vecv = 1;
    else
        vecv = 0;
    end
end

vect = isfield(MODEL_sections, 'vect');
vecs = isfield(MODEL_sections, 'vecs');

if vect
    if length(size(MODEL_sections(secplot).vect)) == 3
        tempt = squeeze(nanmean(MODEL_sections(secplot).vect(:, :, :), 1));
    else
        tempt = MODEL_sections(secplot).vect;
    end
end

if vecs
    if length(size(MODEL_sections(secplot).vecs)) == 3
        temps = squeeze(nanmean(MODEL_sections(secplot).vecs(:, :, :), 1));
    else
        temps = MODEL_sections(secplot).vecs;
    end
end

if vecv
    if length(size(MODEL_sections(secplot).vecv)) == 3
        tempv = squeeze(nanmean(MODEL_sections(secplot).vecv(:, :, :), 1));
    else
        tempv = MODEL_sections(secplot).vecv;
    end
end

figure
initfig_landscape
colormap(jet)
%%
width = .28;
clf

if vect
    if vecv
        tempt(find(tempv == 0)) = NaN;
    else
        tempt(find(tempt == 0)) = NaN;
    end
    s1 = axes('position', [.05 .4 width .25]);
    [atracer, zvect, lvect, atracer_pcol, zvect_pcol, lvect_pcol] = preplot(MODEL_sections(secplot), tempt);
    h = pcolor(lvect_pcol, (zvect_pcol * 1e-3), atracer_pcol);
    set(h, 'linestyle', 'none')
    hold on
    title(MODEL_sections(secplot).name, 'Fontweight', 'bold', 'Fontsize', 14)
    ylabel('depth (km)')
    xlabel('distance (km)')
    s1ax = inputaxis(s1);
    hc1 = colorbar('peer', s1, 'location', 'Southoutside');
    set(hc1, 'position', [(.05 + .02) .3 (width - .04) .03], 'XAxisLocation', 'bottom')
    xlabel(hc1, 'temperature (C)')
    inputcaxis(s1, hc1)
    tt = caxis(s1);
    step = 0.1;
    while length(tt(1):step:tt(2)) > 15
        step = step * 2;
    end
    valt = tt(1):step:tt(2);
    [cc, hh] = contour(lvect, (zvect * 1e-3), atracer, valt, 'k');
    colorbar_l1(hc1, 'hor', valt)
end

if vecs
    if vecv
        temps(find(tempv == 0)) = NaN;
    else
        temps(find(temps == 0)) = NaN;
    end
    s2 = axes('position', [(.05 + width + .01) .4 width .25]);
    [atracer, zvect, lvect, atracer_pcol, zvect_pcol, lvect_pcol] = preplot(MODEL_sections(secplot), temps);
    h = pcolor(lvect_pcol, (zvect_pcol * 1e-3), atracer_pcol);
    set(h, 'linestyle', 'none')
    hold on
    title(MODEL_sections(secplot).name, 'Fontweight', 'bold', 'Fontsize', 14)
    set(s2, 'YTickLabel', '')
    xlabel('distance (km)')
    if exist('s1ax', 'var')
        axis(s2, s1ax);
    else
        s1ax = inputaxis(s2);
    end
    hc2 = colorbar('peer', s2, 'location', 'Southoutside');
    set(hc2, 'position', [(.05 + width + .01 + .02) .3 (width - .04) .03], 'XAxisLocation', 'bottom')
    xlabel(hc2, 'salinity (psu)')
    inputcaxis(s2, hc2)
    tt = caxis(s2);
    steps = .2;
    while length(ceil(tt(1) * 100)/100:steps:floor(tt(2) * 100)/100) < 10
        steps = steps/2;
    end
    vals = ceil(tt(1) * 100)/100:steps:floor(tt(2) * 100)/100;
    [cc, hh] = contour(lvect, (zvect * 1e-3), atracer, vals, 'k');
    colorbar_l1(hc2, 'hor', vals)
end

if vecv
    tempv(find(tempv == 0)) = NaN;
    s3 = axes('position', [(.05 + width + .01 + width + .01) .4 width .25]);
    [atracer, zvect, lvect, atracer_pcol, zvect_pcol, lvect_pcol] = preplotv(MODEL_sections(secplot), tempv);
    h = pcolor(lvect_pcol, (zvect_pcol * 1e-3), (atracer_pcol * 100));
    set(h, 'linestyle', 'none')
    hold on
    title(MODEL_sections(secplot).name, 'Fontweight', 'bold', 'Fontsize', 14)
    set(s3, 'YTickLabel', '')
    xlabel('distance (km)')
    if exist('s1ax', 'var')
        axis(s3, s1ax);
    else
        s1ax = inputaxis(s3);
    end
    hc3 = colorbar('peer', s3, 'location', 'Southoutside');
    set(hc3, 'position', [(.05 + width + .01 + width + .01 + .02) .3 (width - .04) .03], 'XAxisLocation', 'bottom')
    xlabel(hc3, 'normal velocity (cm/s)')
    inputcaxis(s3, hc3)
    tt = caxis(s3);
    stepv = 1;
    if sign(tt(1)) == sign(tt(2))
        while length(tt(1):stepv:tt(2)) > 8
            stepv = stepv * 2;
        end
        valv = tt(1):stepv:tt(2);
    else
        while length(0:stepv:max(abs(tt(1)), abs(tt(2)))) > 5
            stepv = stepv * 2;
        end
        valv = cat(2, fliplr([0:-stepv:tt(1)]), [stepv:stepv:tt(2)]);
    end
    [cc, hh] = contour(lvect, (zvect * 1e-3), (atracer * 100), valv, 'k', 'linewidth', 1);
    colorbar_l1(hc3, 'hor', valv)
    if sign(tt(1)) ~= sign(tt(2))
        [cc, hh] = contour(lvect, (zvect * 1e-3), (atracer * 100), [0 0], 'k', 'linewidth', 2);
        colorbar_l2(hc3, 'hor', [0 0])
    end
end

%
ans = input('print figure ? ');
if ans
    filename = [structfile(1:(end - 4)) '_SEC' MODEL_sections(secplot).name '_tsv.pdf'];
    print('-dpdf', filename);
    disp(['figure saved in ' filename]);
end
