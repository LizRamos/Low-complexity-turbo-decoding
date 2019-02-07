%% Turbo encoder and decoder
% Encoder: RSC (Recursive Systematic Convolution)
% Decoder: BCJR iterative decoder
% Author: Liz Ramos

% Clean up
clear variables;
clc;
close all;

%% Encoder
L = 1024; % Block length

%% Encoder 1 (Outer decoder)
g1 = 7; 
g2 = 5;

K = 3; % Lenght constraint

m = K-1; 
n_states = 2^m; % Number of states

n_iter = 10; % Number of iterations

data = randi([0 1],L,1);

trellis = poly2trellis(K,[g1 g2],g1);
%trellis2 = poly2trellis([3 3],[7 0 5;0 7 6],[7 7]);

hConEnc = comm.ConvolutionalEncoder('TrellisStructure',trellis,'TerminationMethod','Truncated');

c1 = step(hConEnc,data);

%% Interleaver 
permVec=randperm(length(c1)); 

interleaver = comm.BlockInterleaver(permVec');

b1 = interleaver(c1);

%% Encoder 2 (Inner encoder)
c2 = step(hConEnc,b1);

%% Modulation
% Convert to symbols
x = 2*c2 - 1;

scatterplot(x);

% AWGN channel 
E_b_N0  = -20;       % E_B/N0 in dB

Pn = 10^((-E_b_N0 - 3)/10);
nt = sqrt(Pn) * randn(1, length(x));

rt = nt' + x; %received signal

scatterplot(rt) % Received constellation

y_Lch = (2/Pn)*rt; % L-value for BPSK

%% Decoder 

hAPPDec = comm.APPDecoder(...
    'TrellisStructure',trellis, ...
    'Algorithm','Max*','CodedBitLLROutputPort',true);

L_u1 = zeros(L,1);
L_c = zeros(length(c1),1);

% New permutation vector

interleaver = comm.BlockInterleaver(permVec');
deinterleaver = comm.BlockDeinterleaver(permVec');

for i=1:n_iter
    % inner decoder 
    [L_u] = step(hAPPDec,L_c,y_Lch);
    
    %DeInterleaving of L_u from inner decoder
    L_u = deinterleaver(L_u);
   
   
    % outer decoder
    [L_u2, L_c] = step(hAPPDec,L_u1,L_u);
    

    %  Interleaving of L_c from outer decoder
    L_c = interleaver(L_c);
     
end

% Make hard decision 
z = sign(L_u2);

scatterplot(z) % Decoded symbols 

z_bit = (z+1)/2; % convert to bits

%% BER Calculation

b_error = sum(xor(data,z_bit));

BER = b_error/L;


