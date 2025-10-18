from proto_elamite_decoder import ProtoElamiteAngularAnalyzer

def validate_proto_elamite_analysis():
    """
    Validation tests for Proto-Elamite analysis
    """
    analyzer = ProtoElamiteAngularAnalyzer()
    
    test_frequency = analyzer.calculate_frequency(90)
    assert abs(test_frequency - 440) < 0.1, f"Expected 440 Hz, got {test_frequency}"
    print("✓ Test 1 passed: 90° → 440 Hz")
    
    test_frequency = analyzer.calculate_frequency(180)
    assert abs(test_frequency - 880) < 0.1, f"Expected 880 Hz, got {test_frequency}"
    print("✓ Test 2 passed: 180° → 880 Hz")
    
    test_frequency = analyzer.calculate_frequency(45)
    assert abs(test_frequency - 220) < 0.1, f"Expected 220 Hz, got {test_frequency}"
    print("✓ Test 3 passed: 45° → 220 Hz")
    
    test_frequency = analyzer.calculate_frequency(90, 1.33)
    expected = 440 * 1.33
    assert abs(test_frequency - expected) < 0.1, f"Expected {expected} Hz, got {test_frequency}"
    print(f"✓ Test 4 passed: 90° with royal modifier → {expected:.2f} Hz")
    
    assert analyzer.classify_administrative_level(900) == "Ultimate Authority"
    assert analyzer.classify_administrative_level(650) == "High Administrative"
    assert analyzer.classify_administrative_level(450) == "Standard Administrative"
    assert analyzer.classify_administrative_level(250) == "Temporal/Structural"
    assert analyzer.classify_administrative_level(150) == "Fractional/Detailed"
    print("✓ Test 5 passed: Administrative level classification")
    
    assert "Perfect Line" in analyzer.interpret_mathematical_concept(180)
    assert "Right Angle" in analyzer.interpret_mathematical_concept(90)
    assert "Half Right Angle" in analyzer.interpret_mathematical_concept(45)
    print("✓ Test 6 passed: Mathematical concept interpretation")
    
    mock_sign = {"m_number": "M001"}
    analysis = analyzer.analyze_sign(mock_sign)
    assert "frequency" in analysis
    assert "administrative_level" in analysis
    assert "mathematical_concept" in analysis
    print("✓ Test 7 passed: Glyph lookup and analysis")
    
    print("\n" + "="*50)
    print("All validation tests passed!")
    print("="*50)

if __name__ == "__main__":
    validate_proto_elamite_analysis()
