function [] = M_H6BA_15_1_1()

global FAMLIST THERING GLOBVAL

GLOBVAL.E0 = 3.5e9;
GLOBVAL.LatticeFile = 'M_H6BA_15_1_1';
FAMLIST = cell(0);

bendpass = 'BendLinearPass';
quadpass = 'StrMPoleSymplectic4Pass';
sextpass = 'StrMPoleSymplectic4Pass';

disp('Loading Diamond-II Lattice');
h = 934;   % Harmonic number

%% Drifts 
dr_01 = drift('dr_01', 2.495491, 'DriftPass');
dr_02 = drift('dr_02', 0.100000, 'DriftPass');
dr_03 = drift('dr_03', 0.075000, 'DriftPass');
dr_04 = drift('dr_04', 0.150000, 'DriftPass');
dr_05 = drift('dr_05', 0.075000, 'DriftPass');
dr_06 = drift('dr_06', 0.075000, 'DriftPass');
dr_07 = drift('dr_07', 0.075000, 'DriftPass');
dr_08 = drift('dr_08', 0.075000, 'DriftPass');
dr_09 = drift('dr_09', 0.330500, 'DriftPass');
dr_10 = drift('dr_10', 0.075000, 'DriftPass');
dr_11 = drift('dr_11', 0.075000, 'DriftPass');
dr_12 = drift('dr_12', 0.075000, 'DriftPass');
dr_13 = drift('dr_13', 0.165500, 'DriftPass');
dr_14 = drift('dr_14', 0.075000, 'DriftPass');
dr_15 = drift('dr_15', 0.075000, 'DriftPass');
dr_16 = drift('dr_16', 0.075000, 'DriftPass');
dr_17 = drift('dr_17', 0.100000, 'DriftPass');
dr_18 = drift('dr_18', 0.080000, 'DriftPass');
dr_19 = drift('dr_19', 0.197000, 'DriftPass');
dr_20 = drift('dr_20', 0.090000, 'DriftPass');
dr_21 = drift('dr_21', 0.090000, 'DriftPass');
dr_22 = drift('dr_22', 0.075000, 'DriftPass');
dr_23 = drift('dr_23', 0.100000, 'DriftPass');
dr_24 = drift('dr_24', 1.360131, 'DriftPass');
dl_27 = drift('dl_27', 3.670491, 'DriftPass');
dl_26 = drift('dl_26', 0.100000, 'DriftPass');
dl_25 = drift('dl_25', 0.035000, 'DriftPass');
dl_24 = drift('dl_24', 0.035000, 'DriftPass');
dl_23 = drift('dl_23', 0.075000, 'DriftPass');
dl_22 = drift('dl_22', 0.075000, 'DriftPass');
dl_21 = drift('dl_21', 0.075000, 'DriftPass');
dl_20 = drift('dl_20', 0.075000, 'DriftPass');
dl_19 = drift('dl_19', 0.075000, 'DriftPass');
dl_18 = drift('dl_18', 0.075000, 'DriftPass');
dl_17 = drift('dl_17', 0.075000, 'DriftPass');
dl_16 = drift('dl_16', 0.330500, 'DriftPass');
dl_15 = drift('dl_15', 0.075000, 'DriftPass');
dl_14 = drift('dl_14', 0.075000, 'DriftPass');
dl_13 = drift('dl_13', 0.075000, 'DriftPass');
dl_12 = drift('dl_12', 0.165500, 'DriftPass');
dl_11 = drift('dl_11', 0.075000, 'DriftPass');
dl_10 = drift('dl_10', 0.075000, 'DriftPass');
dl_09 = drift('dl_09', 0.075000, 'DriftPass');
dl_08 = drift('dl_08', 0.100000, 'DriftPass');
dl_07 = drift('dl_07', 0.080000, 'DriftPass');
dl_06 = drift('dl_06', 0.197000, 'DriftPass');
dl_05 = drift('dl_05', 0.090000, 'DriftPass');
dl_04 = drift('dl_04', 0.090000, 'DriftPass');
dl_03 = drift('dl_03', 0.075000, 'DriftPass');
dl_02 = drift('dl_02', 0.100000, 'DriftPass');
dl_01 = drift('dl_01', 1.360131, 'DriftPass');

%% Quads 
qf1 = quadrupole('qf1', 0.150000, 7.125230, quadpass);
qd2 = quadrupole('qd2', 0.150000, -5.914638, quadpass);
qd3 = quadrupole('qd3', 0.150000, -3.457434, quadpass);
qf4 = quadrupole('qf4', 0.150000, 5.099144, quadpass);
qf4l = quadrupole('qf4l', 0.150000, 5.364405, quadpass);
qd5 = quadrupole('qd5', 0.105000, -6.516092, quadpass);
qf6 = quadrupole('qf6', 0.360000, 6.262225, quadpass);
qf8 = quadrupole('qf8', 0.250000, 7.259360, quadpass);
qf4_c1 = quadrupole('qf4_c1', 0.150000, 4.761672, quadpass);
qd3_c1 = quadrupole('qd3_c1', 0.150000, -3.102686, quadpass);
qd2_c1 = quadrupole('qd2_c1', 0.105000, -1.227677, quadpass);
qf1_c1 = quadrupole('qf1_c1', 0.185000, -4.785793, quadpass);
quad_add = quadrupole('quad_add', 0.185000, 6.156117, quadpass);

%% Dipoles 
dl1a_5 = sbend('dl1a_5', 0.200000, 0.013064, 0.019775, -0.006711, 0.000000, bendpass);
dl1a_4 = sbend('dl1a_4', 0.200000, 0.008544, 0.006711, 0.001833, 0.000000, bendpass);
dl1a_3 = sbend('dl1a_3', 0.200000, 0.006911, -0.001833, 0.008744, 0.000000, bendpass);
dl1a_2 = sbend('dl1a_2', 0.200000, 0.005903, -0.008744, 0.014647, 0.000000, bendpass);
dl1a_1 = sbend('dl1a_1', 0.200000, 0.005128, -0.014647, 0.019775, 0.000000, bendpass);
dq1 = sbend('dq1', 0.870000, 0.051799, 0.025900, 0.025900, -2.790450, bendpass);

%% Sextupoles 
sd1 = sextupole('sd1', 0.140000, -263.876618, sextpass);
sd2 = sextupole('sd2', 0.140000, -246.404964, sextpass);
sf1 = sextupole('sf1', 0.140000, 329.639903, sextpass);
sh1 = sextupole('sh1', 0.100000, 36.000000, sextpass);
sh2 = sextupole('sh2', 0.100000, -20.000000, sextpass);
s = sextupole('s', 0.100000, 63.044000, sextpass);

%% Octupoles 
of1s = octupole('of1s', 0.090000, -9444.444444, sextpass);

%% BPMs 
bpm_01 = marker('BPM', 'IdentityPass');
bpm_02 = marker('BPM', 'IdentityPass');
bpm_03 = marker('BPM', 'IdentityPass');
bpm_04 = marker('BPM', 'IdentityPass');
bpm_05 = marker('BPM', 'IdentityPass');
bpm_06 = marker('BPM', 'IdentityPass');
bpm_07 = marker('BPM', 'IdentityPass');
bpm_08 = marker('BPM', 'IdentityPass');
bpm_09 = marker('BPM', 'IdentityPass');
bpm_10 = marker('BPM', 'IdentityPass');
bpm_11 = marker('BPM', 'IdentityPass');

%% Correctors 
hcor01 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor02 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor03 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor04 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor05 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor06 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor07 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor08 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor09 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor10 = corrector('CM', 0.000000, [0 0], 'CorrectorPass');
hcor11 = corrector('CM', 0.080000, [0 0], 'CorrectorPass');

%% Cavity 
CAV = rfcavity('RF', 0, 1660000.000000, 499499134.279998, h, 'CavityPass');

%% Defining ring segments
dl1a = [dl1a_5, dl1a_4, dl1a_3, dl1a_2, dl1a_1] ;
arca_c2r = [dr_24, bpm_05, dr_23, hcor05, sh2, dr_22, qf8, dr_21, dq1, dr_20, qf6, dr_19, bpm_04, dr_18, s, hcor04,  dr_17, dl1a, dr_16, qd5, dr_15, sd2, hcor03, dr_14, bpm_03, dr_13, of1s, dr_12, qf4, dr_11, sf1, dr_10, qf4, dr_09, bpm_02, dr_08, hcor02, sd1, dr_07, qd3, dr_06, fliplr(dl1a), dr_05, qd2, dr_04, hcor01, sh1, dr_03, qf1, dr_02, bpm_01, dr_01] ;
arca_c1r = [dl_01, bpm_06, dl_02, hcor06, sh2, dl_03, qf8, dl_04, dq1, dl_05, qf6, dl_06, bpm_07, dl_07, s, hcor07,  dl_08, dl1a, dl_09, qd5, dl_10, sd2, hcor08, dl_11, bpm_08, dl_12, of1s, dl_13, qf4l, dl_14, sf1, dl_15, qf4_c1, dl_16, bpm_09, dl_17, hcor09, sd1, dl_18, qd3_c1, dl_19, fliplr(dl1a), dl_20, qd2_c1, dl_21, bpm_10, dl_22, hcor10, sh1, dl_23, qf1_c1, dl_24, hcor11, dl_25, quad_add, dl_26, bpm_11, dl_27] ;
arca_c2 = [fliplr(arca_c2r), arca_c2r] ;
arca_c1 = [fliplr(arca_c2r), arca_c1r] ;
sp = [fliplr(arca_c1), arca_c2, arca_c2, arca_c1] ;
% ring = [6*sp] ;
ringRF = [sp sp sp sp CAV sp sp] ;

buildlat(ringRF)

for i=1:length(THERING)
	THERING{i}.Energy = GLOBVAL.E0;
end
