# Audio measurement and preview verification

Measure final sounds, not oscillator gain settings. Prefer buffers rendered by the actual scheduling code with production gain and processing, all layers, and enough tail to avoid truncation. For random noise, use several renders or a deterministic test seed and report variation.

Execute `scripts/analyze-audio-buffer.js` in an isolated browser evaluation. It defines `globalThis.analyzeGameAudioBuffer(buffer, { weighted: true })`. Pass a real `AudioBuffer` from `decodeAudioData` or `OfflineAudioContext.startRendering`. It reports peak, RMS, active-range RMS, maximum 100 ms RMS, simple frequency-weighted 100 ms RMS, silence, and non-finite/full-scale sample counts.

The weighting uses a 60 Hz high-pass and a +4 dB high shelf at 1500 Hz. It is an engineering comparison aid, **not LUFS, true peak, a hearing model, or standardized loudness measurement**. Keep sample rate, padding, render path, and weighting consistent. Do not impose one game's numeric levels on another. For long music/voice material, use an available established loudness analyzer when appropriate.

After loading the helper in a browser:

```javascript
const buffer = await offlineContext.startRendering();
const metrics = await analyzeGameAudioBuffer(buffer);
```

If scheduling is coupled to a live singleton, an isolated adapter may provide an offline context. Keep it in scratch work, restore temporary globals with `finally`, and do not resume an offline context as if it were live. Avoid reusing the application's cached live module for experiments. Do not redesign production playback just for convenient measurement.

Check complete-cue weighted RMS versus peers; full-scale/non-finite samples, silence, abrupt boundaries, and truncated tails; repeated and concurrent bursts with music headroom; and unintended makeup gain or changes to isolated cues from output processors.

Use a **real browser click** on a Play button before automated playback loops. Programmatic `.click()` after navigation can leave audio suspended while the page's timer still completes. Verify running context and non-silent output rather than the timer alone. Unlock separate candidate contexts as needed. Check errors and scrolling to the bottom, then open that same URL for the user.

Measurements substantiate volume balance and clipping. They cannot prove that a cue is pleasant or fits the mood. Label those assessments as listening judgments or code-based inferences and use the comparison page for the user's preference.
