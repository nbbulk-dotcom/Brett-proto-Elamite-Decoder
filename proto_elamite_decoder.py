import json
import numpy as np
import cv2
from math import degrees, atan2
from datetime import datetime
from typing import Dict, List, Any

class ProtoElamiteAngularAnalyzer:
    def __init__(self):
        self.base_frequency = 440  # Hz
        self.reference_angle = 90  # degrees
        
    def measure_primary_angle(self, sign_image):
        """
        Measure the primary geometric angle in a Proto-Elamite sign
        """
        gray = cv2.cvtColor(sign_image, cv2.COLOR_BGR2GRAY)
        
        edges = cv2.Canny(gray, 50, 150)
        
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is not None and len(lines) >= 2:
            rho1, theta1 = lines[0][0]
            rho2, theta2 = lines[1][0]
            
            angle_diff = abs(theta1 - theta2)
            angle_degrees = degrees(angle_diff)
            
            if angle_degrees > 180:
                angle_degrees = 360 - angle_degrees
                
            return angle_degrees
        
        return 90  # Default to right angle if detection fails
    
    def calculate_frequency(self, angle_degrees, context_modifier=1.0):
        """
        Calculate frequency from geometric angle
        """
        frequency = self.base_frequency * (angle_degrees / self.reference_angle)
        return frequency * context_modifier
    
    def classify_administrative_level(self, frequency):
        """
        Classify administrative level based on frequency
        """
        if frequency >= 800:
            return "Ultimate Authority"
        elif frequency >= 600:
            return "High Administrative"
        elif frequency >= 400:
            return "Standard Administrative"
        elif frequency >= 200:
            return "Temporal/Structural"
        else:
            return "Fractional/Detailed"
    
    def interpret_mathematical_concept(self, angle):
        """
        Interpret mathematical concept encoded in the angle
        """
        if abs(angle - 180) < 5:
            return "Perfect Line/Unity"
        elif abs(angle - 135) < 5:
            return "Three-Quarter Circle"
        elif abs(angle - 90) < 5:
            return "Right Angle/Square"
        elif abs(angle - 45) < 5:
            return "Half Right Angle"
        elif abs(angle - 30) < 5:
            return "One-Third Right Angle"
        else:
            return f"Complex Angle ({angle:.1f}°)"
    
    def analyze_sign(self, sign_data, context="trade"):
        """
        Analyze a Proto-Elamite sign (from image or pre-loaded data)
        sign_data: dict with 'image' (np.array) or 'm_number' (str) for lookup
        """
        if 'image' in sign_data:
            angle = self.measure_primary_angle(sign_data['image'])
        else:
            with open('glyphs.json', 'r') as f:
                glyphs = json.load(f)['proto_elamite_glyphs']
            glyph = next((g for g in glyphs if g['m_number'] == sign_data['m_number']), None)
            if glyph:
                angle = glyph['primary_angle']
            else:
                angle = 90  # Default
        
        context_modifiers = {
            "royal": 1.33,
            "trade": 1.0,
            "religious": 1.26
        }
        modifier = context_modifiers.get(context, 1.0)
        
        frequency = self.calculate_frequency(angle, modifier)
        
        admin_level = self.classify_administrative_level(frequency)
        concept = self.interpret_mathematical_concept(angle)
        
        return {
            "primary_angle": angle,
            "frequency": frequency,
            "administrative_level": admin_level,
            "context_modifier": modifier,
            "mathematical_concept": concept
        }

class ProtoElamiteDeciphermentSystem:
    def __init__(self):
        self.analyzer = ProtoElamiteAngularAnalyzer()
        self.inscription_database = {}
        
    def analyze_inscription(self, inscription_id, signs, context="trade"):
        """
        Analyze a complete Proto-Elamite inscription
        signs: list of dicts {'m_number': str} or {'image': np.array}
        """
        results = {
            "inscription_id": inscription_id,
            "analysis_date": datetime.now().isoformat(),
            "context": context,
            "signs": [],
            "total_frequency": 0,
            "administrative_summary": {},
            "mathematical_concepts": []
        }
        
        for i, sign in enumerate(signs):
            sign_analysis = self.analyzer.analyze_sign(sign, context)
            sign_analysis["position"] = i + 1
            results["signs"].append(sign_analysis)
            results["total_frequency"] += sign_analysis["frequency"]
            
            concept = sign_analysis["mathematical_concept"]
            if concept not in results["mathematical_concepts"]:
                results["mathematical_concepts"].append(concept)
            
            level = sign_analysis["administrative_level"]
            results["administrative_summary"][level] = results["administrative_summary"].get(level, 0) + 1
        
        self.inscription_database[inscription_id] = results
        return results
    
    def generate_translation(self, inscription_id, target_language="english"):
        """
        Generate human-readable translation
        """
        if inscription_id not in self.inscription_database:
            return "Inscription not found."
        
        analysis = self.inscription_database[inscription_id]
        total_freq = analysis["total_frequency"]
        admin_summary = analysis["administrative_summary"]
        
        narrative_parts = []
        
        if "Ultimate Authority" in admin_summary:
            narrative_parts.append("Royal decree or high-level administrative document")
        elif "High Administrative" in admin_summary:
            narrative_parts.append("Administrative record of significant importance")
        else:
            narrative_parts.append("Standard administrative or trade document")
        
        if analysis["mathematical_concepts"]:
            concepts_str = ", ".join(analysis["mathematical_concepts"])
            narrative_parts.append(f"Mathematical concepts encoded: {concepts_str}")
        
        if total_freq > 2000:
            narrative_parts.append("High-value or complex transaction")
        elif total_freq > 1000:
            narrative_parts.append("Standard administrative procedure")
        else:
            narrative_parts.append("Simple record or notation")
        
        return ". ".join(narrative_parts) + "."
    
    def export_analysis(self, inscription_id, format="json"):
        """
        Export in JSON or CSV
        """
        if inscription_id not in self.inscription_database:
            return None
        
        analysis = self.inscription_database[inscription_id]
        
        if format == "json":
            return json.dumps(analysis, indent=2)
        elif format == "csv":
            csv_lines = ["Position,Angle,Frequency,Administrative_Level,Mathematical_Concept"]
            for sign in analysis["signs"]:
                line = f"{sign['position']},{sign['primary_angle']:.1f},{sign['frequency']:.2f},{sign['administrative_level']},{sign['mathematical_concept']}"
                csv_lines.append(line)
            return "\n".join(csv_lines)
        
        return str(analysis)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Decode Proto-Elamite Inscriptions")
    parser.add_argument("--inscription", required=False, help="Path to inscription JSON file")
    parser.add_argument("--inscription_id", help="Inscription ID")
    parser.add_argument("--signs", nargs="+", help="M-numbers e.g. M001 M032")
    parser.add_argument("--context", default="trade")
    parser.add_argument("--output", default="results.json")
    
    args = parser.parse_args()
    system = ProtoElamiteDeciphermentSystem()
    
    if args.inscription:
        with open(args.inscription, 'r') as f:
            inscription_data = json.load(f)
        inscription_id = inscription_data.get('inscription_id', 'UNKNOWN')
        signs_data = inscription_data.get('signs', [])
        context = inscription_data.get('context', 'trade')
    elif args.signs:
        inscription_id = args.inscription_id or "CLI_INPUT"
        signs_data = [{"m_number": s} for s in args.signs]
        context = args.context
    else:
        print("Error: Provide either --inscription file or --signs list")
        exit(1)
    
    analysis = system.analyze_inscription(inscription_id, signs_data, context)
    with open(args.output, "w") as f:
        json.dump(analysis, f, indent=2)
    print(system.generate_translation(inscription_id))
    print(f"\nAnalysis saved to {args.output}")
