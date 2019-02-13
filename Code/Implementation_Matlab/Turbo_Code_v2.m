%% Turbo encoder and decoder
% Encoder: RSC (Recursive Systematic Convolution)
% Decoder: BCJR iterative decoder
% Author: Liz Ramos

% Clean up
clear variables;
clc;
close all;

%% Encoder
L = 12144; % Block length

%% Encoder 1 (Outer decoder)
g1 = 7; 
g2 = 5;

K = 3; % Lenght constraint

m = K-1; 
n_states = 2^m; % Number of states

n_iter = 1:1:16; % Number of iterations

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

% AWGN channel 
EbNo_range  = -12:0.1:4.5;       % E_B/N0 in dB

%% Decoder 

hAPPDec = comm.APPDecoder(...
    'TrellisStructure',trellis, ...
    'Algorithm','Max*','CodedBitLLROutputPort',true, ...
    'NumScalingBits', 8);

deinterleaver = comm.BlockDeinterleaver(permVec');

BER = zeros(length(n_iter), length(EbNo_range));

% AWGN Channel
Pn = 10.^((-EbNo_range - 3)/10);
nt = sqrt(Pn)' * randn(1, length(x)); 


% counters
c_ebno = 1;
c_iter = 1;

for n_it = n_iter

    for Eb = EbNo_range
        
        % Initialization of the probabilities
        L_u1 = zeros(L,1);
        L_c = zeros(length(c1),1);
        
        
        rt = nt(c_ebno,:)' + x; % received signal
        y_Lch = (2/Pn(c_ebno))*rt; % L-value for BPSK

        for i=1:n_it
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

        z_bit = (z+1)/2; % convert to bits

        %% BER Calculation

        b_error = sum(xor(data,z_bit));

        BER (c_iter,c_ebno) = b_error/L;
        
        c_ebno = c_ebno + 1; 

    end
    c_ebno = 1; 

    c_iter = c_iter + 1;

end 
figure
semilogy(EbNo_range,BER(3,:))
xlabel('Eb/No in dB')
ylabel('BER')
grid on
hold on
semilogy(EbNo_range,BER(4,:))
semilogy(EbNo_range,BER(5,:))
semilogy(EbNo_range,BER(6,:))
semilogy(EbNo_range,BER(7,:))
semilogy(EbNo_range,BER(9,:))
semilogy(EbNo_range,BER(16,:))
legend('3 iterations', '4 iterations', '5 iterations', '6 iterations','7 iterations', '9 iterations', '16 iterations' )

dlmwrite('Eb_No.dat', EbNo_range)
dlmwrite('BER.dat', BER)


