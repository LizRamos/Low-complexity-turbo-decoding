

frmLen = 256;
rng default


intrlvrIndices = randperm(frmLen);

hTEnc = comm.TurboEncoder('TrellisStructure',poly2trellis(4, ...
    [13 15 17],13),'InterleaverIndices',intrlvrIndices);

hTDec = comm.TurboDecoder('TrellisStructure',poly2trellis(4, ...
    [13 15 17],13),'InterleaverIndices',intrlvrIndices, ...
    'NumIterations',4);

hMod = comm.BPSKModulator;


TEB=[];
EbNo_range=-12:0.2:2;

for EbNo = EbNo_range
    EbNo
    hChan = comm.AWGNChannel('EbNo',EbNo);
    hError = comm.ErrorRate;
    noiseVar = 10^(-EbNo/10);
  
    hDemod = comm.BPSKDemodulator('DecisionMethod','Log-likelihood ratio', ...
    'Variance',noiseVar);

    for trial = 1:1000
        data = randi([0 1],frmLen,1);
        encodedData = step(hTEnc,data);
        modSignal = step(hMod,encodedData);
        receivedSignal = step(hChan,modSignal);
        demodSignal = step(hDemod,receivedSignal);
        receivedBits = step(hTDec,-demodSignal);
        errorStats = step(hError,data,receivedBits);
    end
    
    errorStats(1)
    TEB=[TEB errorStats(1)];
end

figure();
plot(EbNo_range,TEB);