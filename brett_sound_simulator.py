#!/usr/bin/env python3
"""
Brett Sound Simulator - Proto-Elamite
======================================
Generates audio files that emulate the estimated tone, intonation, and voice 
inflections for Proto-Elamite using the Brett Method.

Created by: Nicolas of the Family Brett
Date: October 18, 2025
License: MIT
"""

import numpy as np
from scipy.io import wavfile
import pandas as pd
import os
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import argparse

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Install with: pip install pydub")

@dataclass
class VoiceProfile:
    """Voice profile configuration"""
    type: str  # 'male', 'female', 'child'
    pitch: float  # Hz
    rate: int  # Words per minute
    description: str

@dataclass
class PhonemeData:
    """Phoneme data structure"""
    glyph: str
    ipa: str
    pitch: float
    duration: float
    stress: str
    angle: Optional[float] = None

class ProtoElamiteSoundSimulator:
    """Sound simulator for Proto-Elamite"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.voice_profiles = {
            'male': VoiceProfile('male', 100, 130, 'Authoritative hierarchical tone'),
            'female': VoiceProfile('female', 200, 140, 'Administrative clarity'),
            'child': VoiceProfile('child', 280, 180, 'Communal tone')
        }
        self.base_freq = 440  # Base for geometric calculation
        
    def load_phoneme_map(self, file_path: str) -> Dict[str, PhonemeData]:
        """Load phoneme-to-IPA mapping"""
        if not os.path.exists(file_path):
            return self._create_default_phoneme_map()
        
        df = pd.read_csv(file_path)
        phoneme_map = {}
        for _, row in df.iterrows():
            phoneme_map[row['glyph']] = PhonemeData(
                glyph=row['glyph'],
                ipa=row['ipa'],
                pitch=row['pitch'],
                duration=row['duration'],
                stress=row['stress'],
                angle=row.get('angle', None)
            )
        return phoneme_map
    
    def _create_default_phoneme_map(self) -> Dict[str, PhonemeData]:
        """Create default phoneme mappings for Proto-Elamite"""
        default_phonemes = {
            'shu': PhonemeData('shu', 'ʃu', 440.00, 0.5, 'primary', 90.0),
            'il': PhonemeData('il', 'il', 293.33, 0.5, 'primary', 60.0),
            'su': PhonemeData('su', 'su', 220.00, 0.5, 'primary', 45.0),
            'ki': PhonemeData('ki', 'ki', 146.67, 0.5, 'primary', 30.0),
            'an': PhonemeData('an', 'an', 329.63, 0.5, 'primary', 67.5),
            'en': PhonemeData('en', 'en', 261.63, 0.5, 'primary', 53.5),
            'me': PhonemeData('me', 'me', 195.56, 0.5, 'primary', 40.0),
            'ba': PhonemeData('ba', 'ba', 391.11, 0.5, 'primary', 80.0),
            'da': PhonemeData('da', 'da', 366.67, 0.5, 'primary', 75.0),
            'ga': PhonemeData('ga', 'ga', 342.22, 0.5, 'primary', 70.0)
        }
        return default_phonemes
    
    def calculate_geometric_frequency(self, angle: float) -> float:
        """Calculate frequency from glyph angle using Brett Method"""
        return self.base_freq * (angle / 90.0)
    
    def generate_tone(self, freq: float, duration: float) -> np.ndarray:
        """Generate sine wave for phoneme"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = np.sin(2 * np.pi * freq * t)
        
        # Apply envelope
        envelope = np.ones_like(tone)
        fade_samples = int(0.01 * self.sample_rate)
        if len(tone) > 2 * fade_samples:
            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        
        return tone * envelope
    
    def apply_monotone_intonation(self, audio: np.ndarray, stress: str) -> np.ndarray:
        """Apply monotone intonation for economic precision"""
        samples = len(audio)
        
        if stress == 'primary':
            # Flat with slight emphasis
            curve = np.ones(samples) * 0.95
        elif stress == 'secondary':
            # Slightly reduced
            curve = np.ones(samples) * 0.90
        else:
            # Minimal
            curve = np.ones(samples) * 0.85
        
        return audio * curve
    
    def synthesize_phrase(self, text: str, voice_type: str = 'male', 
                         phoneme_map: Optional[Dict] = None) -> np.ndarray:
        """Synthesize a phrase into audio"""
        if phoneme_map is None:
            phoneme_map = self._create_default_phoneme_map()
        
        audio_segments = []
        words = text.replace('-', ' ').split()
        
        for word in words:
            if word in phoneme_map:
                phoneme = phoneme_map[word]
                
                # Calculate frequency from angle if available
                freq = phoneme.pitch
                if phoneme.angle is not None:
                    freq = self.calculate_geometric_frequency(phoneme.angle)
                
                # Generate tone
                tone = self.generate_tone(freq, phoneme.duration)
                
                # Apply monotone intonation
                tone = self.apply_monotone_intonation(tone, phoneme.stress)
                
                # Adjust for voice profile
                voice = self.voice_profiles[voice_type]
                pitch_factor = voice.pitch / 100  # Normalize to male baseline
                tone = self._adjust_pitch(tone, pitch_factor)
                
                audio_segments.append(tone)
                
                # Add brief silence
                silence = np.zeros(int(0.15 * self.sample_rate))
                audio_segments.append(silence)
        
        if audio_segments:
            combined = np.concatenate(audio_segments)
            max_val = np.max(np.abs(combined))
            if max_val > 0:
                combined = combined / max_val * 0.8
            return combined
        return np.array([])
    
    def _adjust_pitch(self, audio: np.ndarray, factor: float) -> np.ndarray:
        """Adjust pitch by resampling"""
        if factor == 1.0:
            return audio
        
        indices = np.arange(0, len(audio), factor)
        indices = indices[indices < len(audio)].astype(int)
        return audio[indices]
    
    def save_wav(self, audio: np.ndarray, output_path: str):
        """Save audio as WAV file"""
        audio_int = (audio * 32767).astype(np.int16)
        wavfile.write(output_path, self.sample_rate, audio_int)
        print(f"Saved audio to: {output_path}")
    
    def process_inscription(self, inscription_id: str, output_dir: str = 'audio_output'):
        """Process a decoded inscription into audio"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Example inscriptions
        inscriptions = {
            'M1': {
                'text': 'shu il su ki',
                'voice': 'male',
                'context': 'Grain chief record (Susa)'
            },
            'M43': {
                'text': 'an en me',
                'voice': 'female',
                'context': 'Administrative tablet (Susa)'
            }
        }
        
        if inscription_id not in inscriptions:
            print(f"Inscription {inscription_id} not found")
            return
        
        insc = inscriptions[inscription_id]
        print(f"Processing {inscription_id}: {insc['text']}")
        print(f"Context: {insc['context']}")
        print(f"Voice: {insc['voice']}")
        
        audio = self.synthesize_phrase(insc['text'], insc['voice'])
        output_path = os.path.join(output_dir, f"{inscription_id}_proto_elamite.wav")
        self.save_wav(audio, output_path)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Brett Sound Simulator for Proto-Elamite'
    )
    parser.add_argument('--inscription', '-i', help='Inscription ID (M1, M43)')
    parser.add_argument('--text', '-t', help='Custom text to synthesize')
    parser.add_argument('--voice', '-v', choices=['male', 'female', 'child'], 
                       default='male', help='Voice profile')
    parser.add_argument('--output', '-o', default='audio_output', 
                       help='Output directory')
    parser.add_argument('--phoneme-map', '-p', help='Path to phoneme CSV file')
    
    args = parser.parse_args()
    
    simulator = ProtoElamiteSoundSimulator()
    
    if args.inscription:
        simulator.process_inscription(args.inscription, args.output)
    elif args.text:
        os.makedirs(args.output, exist_ok=True)
        
        phoneme_map = None
        if args.phoneme_map:
            phoneme_map = simulator.load_phoneme_map(args.phoneme_map)
        
        print(f"Synthesizing: {args.text}")
        print(f"Voice: {args.voice}")
        
        audio = simulator.synthesize_phrase(args.text, args.voice, phoneme_map)
        output_path = os.path.join(args.output, f"custom_proto_elamite.wav")
        simulator.save_wav(audio, output_path)
    else:
        print("Processing all available inscriptions...")
        for insc_id in ['M1', 'M43']:
            simulator.process_inscription(insc_id, args.output)

if __name__ == "__main__":
    main()
