// Load in a browser evaluation. Analyze decoded or fully rendered game audio.
// The weighted metric is a comparison aid, not standardized LUFS/true peak.
globalThis.analyzeGameAudioBuffer = async function (buffer, { weighted = true } = {}) {
  const scan = data => {
    const frames = data[0].length;
    const channels = data.length;
    const windowSize = Math.max(1, Math.round(buffer.sampleRate * 0.1));
    const energy = new Float64Array(frames);
    let peak = 0, total = 0, nonFinite = 0, fullScale = 0;
    for (let channel = 0; channel < channels; channel++) {
      for (let i = 0; i < frames; i++) {
        const value = data[channel][i];
        if (!Number.isFinite(value)) { nonFinite++; continue; }
        peak = Math.max(peak, Math.abs(value));
        if (Math.abs(value) >= 1) fullScale++;
        energy[i] += value * value / channels;
      }
    }
    let rolling = 0, maxEnergy = 0;
    for (let i = 0; i < frames; i++) {
      total += energy[i];
      rolling += energy[i];
      if (i >= windowSize) rolling -= energy[i - windowSize];
      maxEnergy = Math.max(maxEnergy, rolling);
    }
    const threshold = (peak * 0.001) ** 2;
    let first = 0, last = frames - 1;
    while (first < frames && energy[first] <= threshold) first++;
    while (last >= first && energy[last] <= threshold) last--;
    let activeEnergy = 0;
    for (let i = first; i <= last; i++) activeEnergy += energy[i];
    return {
      peak, rms: frames ? Math.sqrt(total / frames) : 0,
      activeRms: last >= first ? Math.sqrt(activeEnergy / (last - first + 1)) : 0,
      windowRms: Math.sqrt(maxEnergy / windowSize), nonFinite, fullScale,
    };
  };
  const channels = Array.from({ length: buffer.numberOfChannels }, (_, i) => buffer.getChannelData(i));
  const raw = scan(channels);
  const db = amplitude => amplitude > 0 ? 20 * Math.log10(amplitude) : null;
  let weightedDb = null;
  if (weighted && raw.nonFinite === 0 && buffer.length > 0) {
    const ctx = new OfflineAudioContext(buffer.numberOfChannels, buffer.length, buffer.sampleRate);
    const source = ctx.createBufferSource();
    source.buffer = buffer;
    const highpass = ctx.createBiquadFilter();
    highpass.type = 'highpass'; highpass.frequency.value = 60; highpass.Q.value = 0.707;
    const shelf = ctx.createBiquadFilter();
    shelf.type = 'highshelf'; shelf.frequency.value = 1500; shelf.gain.value = 4;
    source.connect(highpass); highpass.connect(shelf); shelf.connect(ctx.destination);
    source.start();
    const output = await ctx.startRendering();
    weightedDb = db(scan(Array.from({ length: output.numberOfChannels }, (_, i) => output.getChannelData(i))).windowRms);
  }
  return {
    duration: buffer.length / buffer.sampleRate,
    channels: buffer.numberOfChannels,
    sampleRate: buffer.sampleRate,
    peak: raw.peak,
    peakDbFS: db(raw.peak),
    rmsDbFS: db(raw.rms),
    activeRmsDbFS: db(raw.activeRms),
    peakWindowRmsDbFS: db(raw.windowRms),
    weightedPeakWindowDbFS: weightedDb,
    silent: raw.peak === 0 && raw.nonFinite === 0,
    nonFiniteSamples: raw.nonFinite,
    fullScaleSamples: raw.fullScale,
  };
};
