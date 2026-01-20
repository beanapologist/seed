#!/usr/bin/env python3
"""
Test NIST STS Integration

This test verifies that the NIST STS workflow functions correctly.
It's designed to be run as part of the test suite.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestNISTSTSIntegration(unittest.TestCase):
    """Test NIST Statistical Test Suite integration."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.repo_root = Path(__file__).parent
        cls.scripts_dir = cls.repo_root / 'scripts'
        cls.temp_dir = Path(tempfile.mkdtemp())
        
    def test_generate_binary_script_exists(self):
        """Test that generate_nist_binary.py script exists."""
        script = self.scripts_dir / 'generate_nist_binary.py'
        self.assertTrue(script.exists(), f"Script not found: {script}")
        self.assertTrue(os.access(script, os.X_OK), f"Script not executable: {script}")
    
    def test_run_nist_tests_script_exists(self):
        """Test that run_nist_tests.py script exists."""
        script = self.scripts_dir / 'run_nist_tests.py'
        self.assertTrue(script.exists(), f"Script not found: {script}")
        self.assertTrue(os.access(script, os.X_OK), f"Script not executable: {script}")
    
    def test_generate_binary_universal(self):
        """Test generating binary data from Universal QKD."""
        output_file = self.temp_dir / 'test_universal.txt'
        
        result = subprocess.run(
            [
                sys.executable,
                str(self.scripts_dir / 'generate_nist_binary.py'),
                '-n', '10000',
                '-t', 'universal',
                '-o', str(output_file)
            ],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")
        self.assertTrue(output_file.exists(), "Output file not created")
        
        # Verify file content
        with open(output_file, 'r') as f:
            data = f.read()
            self.assertEqual(len(data), 10000, "Incorrect number of bits generated")
            self.assertTrue(all(c in '01' for c in data), "Invalid characters in output")
    
    def test_run_nist_tests_basic(self):
        """Test running NIST tests on generated data."""
        # Generate test data
        input_file = self.temp_dir / 'test_data.txt'
        output_file = self.temp_dir / 'test_results.json'
        
        # Generate binary data
        subprocess.run(
            [
                sys.executable,
                str(self.scripts_dir / 'generate_nist_binary.py'),
                '-n', '10000',
                '-t', 'universal',
                '-o', str(input_file)
            ],
            check=True,
            capture_output=True
        )
        
        # Run NIST tests
        result = subprocess.run(
            [
                sys.executable,
                str(self.scripts_dir / 'run_nist_tests.py'),
                '-i', str(input_file),
                '-o', str(output_file)
            ],
            capture_output=True,
            text=True
        )
        
        # Test may fail some statistical tests, but should complete
        # (exit code 0 = all passed, 1 = some failed but completed)
        self.assertIn(result.returncode, [0, 1], f"Script crashed: {result.stderr}")
        self.assertTrue(output_file.exists(), "Results file not created")
        
        # Verify JSON structure
        with open(output_file, 'r') as f:
            results = json.load(f)
            
        self.assertIn('metadata', results, "Missing metadata in results")
        self.assertIn('tests', results, "Missing tests in results")
        self.assertIn('summary', results, "Missing summary in results")
        
        self.assertIn('total_bits', results['metadata'])
        self.assertEqual(results['metadata']['total_bits'], 10000)
        
        self.assertIn('total_tests', results['summary'])
        self.assertIn('passed', results['summary'])
        self.assertIn('failed', results['summary'])
        self.assertIn('pass_rate', results['summary'])
        self.assertIn('overall_passed', results['summary'])
    
    def test_multiple_generators(self):
        """Test that all generators produce valid output."""
        generators = ['universal', 'gqs1', 'kyber', 'dilithium', 'sphincs']
        
        for gen in generators:
            with self.subTest(generator=gen):
                output_file = self.temp_dir / f'test_{gen}.txt'
                
                result = subprocess.run(
                    [
                        sys.executable,
                        str(self.scripts_dir / 'generate_nist_binary.py'),
                        '-n', '5000',
                        '-t', gen,
                        '-o', str(output_file)
                    ],
                    capture_output=True,
                    text=True
                )
                
                self.assertEqual(result.returncode, 0,
                                 f"Generator {gen} failed: {result.stderr}")
                self.assertTrue(output_file.exists(),
                                f"Output file not created for {gen}")
                
                # Verify content
                with open(output_file, 'r') as f:
                    data = f.read()
                    self.assertTrue(all(c in '01' for c in data),
                                    f"Invalid characters in {gen} output")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(cls.temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
