function [] = define_sections()
%DEFINE_SECTIONS produces a .mat sections file
%
% DESCRIPTION
% DEFINE_SECTIONS produces a .mat file that contains a structure that gathers
% all information regarding sections to be analysed, ie
% name, longitude and latitude of each end point/corner,
% the positive direction across each segment (NE, NW, SE or SW)
%
% Currently available sections are in the :
%
% - global
% - Arctic
% - North Atlantic
% - Southern Africa
%
% EXAMPLES
%
% To produce ${HOME}/.pago/sections_[GL|AR|SA|NA].mat:
%
%   define_sections();
%
%   See also <https://sourcesup.renater.fr/pago/sections.html>
%
% Release notes :
%
% PAGO V2.0
%
% - add Arctic and Southern Africa predefined sections
% - no more interactivity
%
% TODO save error handling
% TODO return filenames
%
%MAPAGO Toolbox.
%Copyright 2012-2015, CNRS TODO

% JD PAGO WHOI

basedir = fullfile(getenv('HOME'), '.pago');

% predefined sections for North Atlantic
region_code = 'NA';

% 42n
sections(1).name = '42n';
sections(1).lon = [-53 -49 -29 -9];
sections(1).lat = [47 42 43 52];
sections(1).dir = ['NE';'NW';'NW'];

% a25
sections(2).name = 'a25';
sections(2).lon = [-42.5 -9.0];
sections(2).lat = [61.5 54.0];
sections(2).dir = ['NE'];

% ar7w
sections(3).name = 'ar7';
sections(3).lon = [-56 -47];
sections(3).lat = [53 61.5];
sections(3).dir = ['NW'];

% barents
sections(4).name = 'bar';
sections(4).lon = [18.0 15.0];
sections(4).lat = [69 78];
sections(4).dir = ['NE'];

% nordic_n
sections(5).name = 'non';
sections(5).lon = [-19 -0.5 15];
sections(5).lat = [77.5 77 78];
sections(5).dir = ['NE';'NW'];

% nordic_s
sections(6).name = 'nos';
sections(6).lon = [-23.0 -2.0 13.0];
sections(6).lat = [71 66 65];
sections(6).dir = ['NE';'NE'];

% Hudson Strait
sections(7).name = 'hud';
sections(7).lon = [-65 -66];
sections(7).lat = [59 64];
sections(7).dir = ['NE'];

% Baffin Bay
sections(8).name = 'baf';
sections(8).lon = [-64 -52];
sections(8).lat = [66 67];
sections(8).dir = ['SE'];

% Denmark Strait overflow
sections(9).name = 'dso';
sections(9).lon = [-34 -22];
sections(9).lat = [68 65.5];
sections(9).dir = ['NE'];

% Iceland-Faroe overflow
sections(10).name = 'ifo';
sections(10).lon = [-15 -7.5];
sections(10).lat = [65 62.5];
sections(10).dir = ['NE'];

% Faroe-Shetland overflow
sections(11).name = 'fso';
sections(11).lon = [-7.5 -5];
sections(11).lat = [62.5 58];
sections(11).dir = ['NE'];

% Iceland to Shetland
sections(12).name = 'its';
sections(12).lon = [-6 -4];
sections(12).lat = [55 57];
sections(12).dir = ['NW'];

% Mer du Nord
sections(13).name = 'mdn';
sections(13).lon = [-3 7];
sections(13).lat = [57 60];
sections(13).dir = ['NW'];

% OVIDE section
sections(14).name = 'ovi';
sections(14).lon = [-44.2 -30.7 -12.2 -7.5];
sections(14).lat = [60.1 58.7 40.3 40.28];
sections(14).dir = ['NE';'NE';'NE'];

% 26°N section
sections(15).name = '26n';
sections(15).lon = [-80 -10];
sections(15).lat = [26 26];
sections(15).dir = ['NW'];

filename = fullfile(basedir, ['sections_', region_code, '.mat']);
save(filename, 'sections');

% predefined sections for global diagnostics
region_code = 'GL';

n = 1;
sections = [];
sections(n).name = 'A4N';
sections(n).lon = [-63 -0.7];
sections(n).lat = [45 45];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'A2N';
sections(n).lon = [-81 -12];
sections(n).lat = [26 26];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'A3S';
sections(n).lon = [-54 20];
sections(n).lat = [-30 -30];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'ITF';
sections(n).lon = [-242 -243];
sections(n).lat = [-22 -8.7];
sections(n).dir = ['NW'];

n = n + 1;
sections(n).name = 'P2N';
sections(n).lon = [-244 -108];
sections(n).lat = [27 27];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'P4N';
sections(n).lon = [142.5 -120];
sections(n).lat = [45 45];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'P1N';
sections(n).lon = [106 -84];
sections(n).lat = [10 10];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'P1S';
sections(n).lon = [149 -70];
sections(n).lat = [-10 -10];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'P3S';
sections(n).lon = [-68 -208];
sections(n).lat = [-30 -30];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'P4S';
sections(n).lon = [-213 -70];
sections(n).lat = [-42 -45];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'I9W';
sections(n).lon = [50 77];
sections(n).lat = [9 9];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'I9E';
sections(n).lon = [77 99];
sections(n).lat = [9 9];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'I3S';
sections(n).lon = [30 117];
sections(n).lat = [-30 -30];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'DRA';
sections(n).lon = [-67 -59];
sections(n).lat = [-55 -64];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'AAF';
sections(n).lon = [22 28];
sections(n).lat = [-32 -71];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'AUS';
sections(n).lon = [-213 -210];
sections(n).lat = [-42 -69];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'DSO';
sections(n).lon = [-33 -19];
sections(n).lat = [70 66];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'ISO';
sections(n).lon = [-14 -5];
sections(n).lat = [65 58];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'FRA';
sections(n).lon = [-15 17];
sections(n).lat = [81 79];
sections(n).dir = ['NE'];

n = n + 1;
sections(n).name = 'MOZ';
sections(n).lon = [38 48];
sections(n).lat = [-14 -16];
sections(n).dir = ['SW'];

n = n + 1;
sections(n).name = 'BER';
sections(n).lon = [-171 -167];
sections(n).lat = [66 65.7];
sections(n).dir = ['NE'];

filename = fullfile(basedir, ['sections_', region_code, '.mat']);
save(filename, 'sections');

% predefined sections around Southern Africa
region_code = 'SA';

%sections for Kyle Cooper (UCT);
n = 1;
sections = [];
sections(n).name = 'AC1';
sections(n).lon = [30.2 32.4 38.83];
sections(n).lat = [-30.9 -32.8 -37.76];
sections(n).dir = ['SW';'SW'];

n = n + 1;
sections(n).name = 'LOC';
sections(n).lon = [39.25 44.1];
sections(n).lat = [-16.36 -17.4];
sections(n).dir = ['SW'];

n = n + 1;
sections(n).name = 'GHL';
sections(n).lon = [18.6 15 2];
sections(n).lat = [-33.9 -33.9 -50];
sections(n).dir = ['NW';'NW'];

n = n + 1;
sections(n).name = 'NEM';
sections(n).lon = [49.5 49.5];
sections(n).lat = [-12.5 -8];
sections(n).dir = ['NW'];

n = n + 1;
sections(n).name = 'EMC';
sections(n).lon = [45 45];
sections(n).lat = [-29 -25];
sections(n).dir = ['SW'];

n = n + 1;
sections(n).name = 'GH2';
sections(n).lon = [2 18.6];
sections(n).lat = [-50 -33.9];
sections(n).dir = ['NW'];

n = n + 1;
sections(n).name = 'AAF';
sections(n).lon = [19.9 28.4];
sections(n).lat = [-34.53 -51.38];
sections(n).dir = ['SW'];

n = n + 1;
sections(n).name = 'LUD';
sections(n).lon = [2.75 5.83 8.5 12.75];
sections(n).lat = [-29.59 -23.32 -20.39 -18.82];
sections(n).dir = ['NW';'NW';'NW'];

n = n + 1;
sections(n).name = 'bej';
sections(n).lon = [-1.58 10.42 15.75];
sections(n).lat = [-42.53 -31.17 -27.47];
sections(n).dir = ['NW';'NW'];

filename = fullfile(basedir, ['sections_', region_code, '.mat']);
save(filename, 'sections');

% predefined sections for Arctic
region_code = 'AR';

% Bering Strait
n = 1;
sections = [];
sections(n).name = 'ber';
sections(n).lon = [-167 -172];
sections(n).lat = [66 66];
sections(n).dir = ['NW'];

% through Canada basin
n = n + 1;
sections(n).name = 'can';
sections(n).lon = [-130 -165 158];
sections(n).lat = [70 78 71];
sections(n).dir = ['NE';'NW'];

% through Fram basin
n = n + 1;
sections(n).name = 'fra';
sections(n).lon = [-38 60 130 128];
sections(n).lat = [82 90 85 73];
sections(n).dir = ['NW';'NW';'NW'];

% Barents
n = n + 1;
sections(n).name = 'bar';
sections(n).lon = [18.0 15.0];
sections(n).lat = [69 78];
sections(n).dir = ['NE'];

% nordic_n
n = n + 1;
sections(n).name = 'non';
sections(n).lon = [-19 -0.5 15];
sections(n).lat = [77.5 77 78];
sections(n).dir = ['NE';'NW'];

% Hudson Strait
n = n + 1;
sections(n).name = 'hud';
sections(n).lon = [-65 -66];
sections(n).lat = [59 64];
sections(n).dir = ['NE'];

% Baffin Bay
n = n + 1;
sections(n).name = 'baf';
sections(n).lon = [-64 -52];
sections(n).lat = [66 67];
sections(n).dir = ['SE'];

filename = fullfile(basedir, ['sections_', region_code, '.mat']);
save(filename, 'sections');

end
