import numpy as np
import json
from typing import Dict

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False
    print("Warning: soundfile not available. Audio export will be limited.")

class ProtoElamiteAudioSynthesis:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def generate_tone(self, frequency, duration=0.5):
        """
        Generate a pure tone for a given frequency
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        tone = np.sin(2 * np.pi * frequency * t)
        
        envelope = np.ones_like(tone)
        fade_samples = int(0.01 * self.sample_rate)  # 10ms fade
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return tone * envelope
    
    def synthesize_inscription(self, analysis_file: str, output_file="proto_elamite_audio.wav"):
        """
        Create audio from analysis JSON
        """
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        audio_sequence = np.array([])
        
        for sign in analysis["signs"]:
            frequency = sign["frequency"]
            tone = self.generate_tone(frequency, duration=0.8)
            silence = np.zeros(int(0.2 * self.sample_rate))
            audio_sequence = np.concatenate([audio_sequence, tone, silence])
        
        if len(audio_sequence) > 0:
            audio_sequence = audio_sequence / np.max(np.abs(audio_sequence))
        
        if SOUNDFILE_AVAILABLE:
            sf.write(output_file, audio_sequence, self.sample_rate)
            print(f"Audio generated: {output_file}")
        else:
            np.save(output_file.replace('.wav', '.npy'), audio_sequence)
            print(f"Audio data saved as numpy array: {output_file.replace('.wav', '.npy')}")
            print("Install soundfile to export as WAV: pip install soundfile")
        
        return output_file
    
    def generate_frequency_report(self, analysis_file: str):
        """
        Generate a report of frequencies in the inscription
        """
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        print("\n" + "="*60)
        print("PROTO-ELAMITE ACOUSTIC FREQUENCY REPORT")
        print("="*60)
        print(f"Inscription ID: {analysis['inscription_id']}")
        print(f"Context: {analysis['context']}")
        print(f"Total Signs: {len(analysis['signs'])}")
        print(f"Total Frequency: {analysis['total_frequency']:.2f} Hz")
        print("\nSign-by-Sign Breakdown:")
        print("-"*60)
        
        for sign in analysis["signs"]:
            print(f"Position {sign['position']:2d}: {sign['primary_angle']:6.1f}° → {sign['frequency']:7.2f} Hz")
            print(f"              Level: {sign['administrative_level']}")
            print(f"              Concept: {sign['mathematical_concept']}")
            print()
        
        print("="*60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate audio from Proto-Elamite analysis")
    parser.add_argument("--analysis", default="results.json", help="Analysis JSON file")
    parser.add_argument("--output", default="proto_audio.wav", help="Output audio file")
    parser.add_argument("--report", action="store_true", help="Generate frequency report")
    args = parser.parse_args()
    
    synth = ProtoElamiteAudioSynthesis()
    
    if args.report:
        synth.generate_frequency_report(args.analysis)
    
    file = synth.synthesize_inscription(args.analysis, args.output)
