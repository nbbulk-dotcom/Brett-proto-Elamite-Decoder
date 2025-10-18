# Brett Sound Simulator - Proto-Elamite

## Overview

The Brett Sound Simulator generates audio files that emulate the estimated tone, intonation, and voice inflections for Proto-Elamite (3200-2700 BCE) using the Brett Method. This tool brings the voices of ancient Susa to life through geometric frequency analysis.

## Features

- **Monotone Intonation**: Flat precision for economic records
- **Geometric Frequencies**: Calculated from glyph angles (Brett Method)
- **Voice Profiles**: Male (hierarchical), Female (administrative), Child (communal)
- **Frequency Analysis**: 147-440 Hz range based on glyph geometry
- **WAV Output**: High-quality 44.1 kHz, 16-bit PCM audio files

## Installation

```bash
pip install numpy scipy pandas pydub
```

## Usage

### Basic Commands

```bash
# Process specific inscription
python brett_sound_simulator.py --inscription M1

# Custom text
python brett_sound_simulator.py --text "shu il su ki"

# Different voice
python brett_sound_simulator.py --text "an en me" --voice female

# Process all inscriptions
python brett_sound_simulator.py
```

### Examples

#### M1 - Grain Chief Record
```bash
python brett_sound_simulator.py --inscription M1
```
- **Output**: `audio_output/M1_proto_elamite.wav`
- **Reading**: "shu-il su-ki" (grain chief)
- **Voice**: Male (100 Hz, authoritative)

#### M43 - Administrative Tablet
```bash
python brett_sound_simulator.py --inscription M43
```
- **Output**: `audio_output/M43_proto_elamite.wav`
- **Reading**: "an-en-me" (administrative record)
- **Voice**: Female (200 Hz, administrative)

## Phoneme Mapping

| Glyph | IPA | Frequency (Hz) | Angle (°) | Duration (s) | Context |
|-------|-----|----------------|-----------|--------------|---------|
| shu | ʃu | 440.00 | 90.0 | 0.5 | Grain |
| il | il | 293.33 | 60.0 | 0.5 | Chief |
| su | su | 220.00 | 45.0 | 0.5 | Total |
| ki | ki | 146.67 | 30.0 | 0.5 | Place |
| an | an | 329.63 | 67.5 | 0.5 | Heaven |
| en | en | 261.63 | 53.5 | 0.5 | Lord |
| me | me | 195.56 | 40.0 | 0.5 | Divine |
| ba | ba | 391.11 | 80.0 | 0.5 | Distribute |
| da | da | 366.67 | 75.0 | 0.5 | Give |
| ga | ga | 342.22 | 70.0 | 0.5 | Milk |

### Geometric Frequency Calculation

Proto-Elamite uses the Brett Method formula:
```
Frequency (Hz) = 440 × (Angle / 90)
```

Where angle is the geometric angle of the glyph (0-90°).

## Voice Profiles

### Male (Hierarchical/Economic)
- **Pitch**: 100 Hz (deep, authoritative)
- **Rate**: 130 wpm
- **Context**: Economic records, hierarchical texts
- **Example**: M1 grain record

### Female (Administrative)
- **Pitch**: 200 Hz (mid-range, clear)
- **Rate**: 140 wpm
- **Context**: Administrative tablets
- **Example**: M43 administrative record

### Child (Communal)
- **Pitch**: 280 Hz (high, youthful)
- **Rate**: 180 wpm
- **Context**: Communal texts
- **Example**: Informal records

## Intonation

### Monotone Pattern (Default)

1. **Primary Stress**: Flat (0.95 amplitude)
   - Reflects economic precision
2. **Secondary Stress**: Slightly reduced (0.90 amplitude)
3. **Unstressed**: Minimal (0.85 amplitude)

## Technical Specifications

- **Format**: WAV, 16-bit PCM
- **Sample Rate**: 44,100 Hz
- **Base Frequency**: 440 Hz (for 90° angle)
- **Range**: 147-440 Hz (30-90° angles)
- **File Size**: 1-5 MB per phrase

## Integration

```python
from brett_sound_simulator import ProtoElamiteSoundSimulator

simulator = ProtoElamiteSoundSimulator()
audio = simulator.synthesize_phrase("shu il su ki", voice_type='male')
simulator.save_wav(audio, 'output.wav')
```

## Geometric Analysis

The Brett Method calculates frequencies from glyph geometry:

- **90° glyphs**: 440 Hz (highest, most complex)
- **60° glyphs**: 293 Hz (mid-range)
- **45° glyphs**: 220 Hz (common)
- **30° glyphs**: 147 Hz (lowest, simplest)

This reflects the visual complexity and semantic importance of glyphs.

## References

- Damerow & Englund (1989) - Proto-Elamite texts
- Englund (2004) - Administrative practices
- Friberg (1978-79) - Numerical systems
- Brett, N. (2025) - Proto-Elamite Decoder

## License

MIT License

## Contact

- **GitHub**: [@nbbulk-dotcom](https://github.com/nbbulk-dotcom)
- **Email**: nbbulk@gmail.com

---

**Version**: 1.0  
**Last Updated**: October 18, 2025
