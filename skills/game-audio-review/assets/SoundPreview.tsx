import { useEffect, useRef, useState } from 'react';
import './SoundPreview.css';

export type PreviewSound = {
  id: string;
  label: string;
  description: string;
  duration: number;
  // Resolve after audio is unlocked and playback has actually been scheduled.
  play: () => void | Promise<void>;
  stop?: () => void;
};
export type SoundComparison = {
  id: string;
  title: string;
  description: string;
  sounds: PreviewSound[];
};

export default function SoundPreview({ gameName, sounds, comparisons = [] }: {
  gameName: string;
  sounds: PreviewSound[];
  comparisons?: SoundComparison[];
}) {
  const [playing, setPlaying] = useState<PreviewSound | null>(null);
  const [scheduled, setScheduled] = useState(false);
  const [status, setStatus] = useState('Choose a sound to listen.');
  const request = useRef(0);
  const active = useRef<PreviewSound | null>(null);

  useEffect(() => () => {
    request.current++;
    active.current?.stop?.();
  }, []);

  useEffect(() => {
    if (!playing || !scheduled) return;
    const timer = window.setTimeout(() => {
      playing.stop?.();
      active.current = null;
      setPlaying(null);
      setScheduled(false);
      setStatus(`Last played: ${playing.label}`);
    }, (playing.duration + 0.2) * 1000);
    return () => window.clearTimeout(timer);
  }, [playing, scheduled]);

  const preview = async (sound: PreviewSound) => {
    if (active.current) return;
    const token = ++request.current;
    active.current = sound;
    setPlaying(sound);
    setScheduled(false);
    setStatus(`Starting: ${sound.label}`);
    try {
      await sound.play();
      if (token !== request.current) { sound.stop?.(); return; }
      setScheduled(true);
      setStatus(`Playing: ${sound.label}`);
    } catch {
      sound.stop?.();
      if (token !== request.current) return;
      active.current = null;
      setPlaying(null);
      setStatus('Audio could not start. Try clicking the sound again.');
    }
  };

  const row = (sound: PreviewSound) => (
    <li key={sound.id} className="sound-preview-row">
      <button type="button" aria-label={`Play ${sound.label}`} disabled={playing !== null}
        onClick={() => void preview(sound)}>
        {playing === sound ? (scheduled ? 'Playing…' : 'Starting…') : 'Play'}
      </button>
      <div>
        <div className="sound-preview-label">{sound.label}</div>
        <p className="sound-preview-description">{sound.description}</p>
      </div>
    </li>
  );
  const comparedIds = new Set(comparisons.flatMap(comparison => comparison.sounds.map(sound => sound.id)));

  return (
    <main className="sound-preview-page">
      <div className="sound-preview-column">
        <h1>{gameName} — sound effects</h1>
        <p>All {sounds.length} game sounds. One sound at a time.</p>
        <p role="status" className="sound-preview-status">{status}</p>
        {comparisons.map(comparison => (
          <section key={comparison.id} aria-labelledby={`comparison-${comparison.id}`}>
            <h2 id={`comparison-${comparison.id}`}>{comparison.title}</h2>
            <p className="sound-preview-comparison-description">{comparison.description}</p>
            <ul>{comparison.sounds.map(row)}</ul>
          </section>
        ))}
        <section aria-labelledby="sound-preview-inventory">
          <h2 id="sound-preview-inventory">{comparisons.length ? 'Other game sounds' : 'Game sounds'}</h2>
          <ul>{sounds.filter(sound => !comparedIds.has(sound.id)).map(row)}</ul>
        </section>
        <a href="/">Back to game</a>
      </div>
    </main>
  );
}
