#!/usr/bin/env node

/**
 * Build script for Golden Seed npm package
 * Creates JavaScript distribution from Python source
 */

const fs = require('fs');
const path = require('path');

// Create dist directory
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// Copy binary fusion tap implementation
const sourceFile = path.join(__dirname, 'releases', 'binary-fusion-tap-v2.0.0', 'javascript', 'binary_fusion_tap.js');
const targetFile = path.join(distDir, 'binary_fusion_tap.js');

if (fs.existsSync(sourceFile)) {
  fs.copyFileSync(sourceFile, targetFile);
  console.log('✓ Copied binary_fusion_tap.js');
} else {
  console.log('ℹ binary_fusion_tap.js not found (optional component)');
}

// Create index.js that exports the main functionality
const indexContent = `/**
 * GoldenSeed - Deterministic High-Entropy Byte Streams
 * 
 * ⚠️ NOT FOR CRYPTOGRAPHY: This library generates deterministic pseudo-random
 * streams and must NOT be used for cryptographic purposes.
 * 
 * For procedural content generation, reproducible testing, and deterministic simulations.
 * 
 * @module golden-seed
 * @version 3.0.0
 * @license GPL-3.0-or-later
 */

// Import binary fusion tap if available
let BinaryFusionTap;
try {
  BinaryFusionTap = require('./binary_fusion_tap');
} catch (e) {
  console.warn('Binary fusion tap not available:', e.message);
}

/**
 * Golden Ratio constant (φ)
 */
const PHI = (1 + Math.sqrt(5)) / 2;

/**
 * Generate deterministic pseudo-random numbers using golden ratio
 * 
 * @param {number} seed - Initial seed value
 * @param {number} count - Number of values to generate
 * @returns {number[]} Array of pseudo-random values in [0, 1)
 */
function goldenRatioSequence(seed = 0, count = 10) {
  const sequence = [];
  let current = seed;
  
  for (let i = 0; i < count; i++) {
    current = (current + PHI) % 1.0;
    sequence.push(current);
  }
  
  return sequence;
}

/**
 * Deterministic coin flip based on golden ratio
 * 
 * @param {number} index - Position in sequence
 * @returns {boolean} true for heads, false for tails
 */
function goldenRatioCoinFlip(index) {
  const value = ((index + 1) * PHI) % 1.0;
  return value < 0.5;
}

/**
 * Generate deterministic test vectors
 * 
 * @param {number} count - Number of vectors to generate
 * @param {number} seed - Initial seed value
 * @returns {string[]} Array of hex-encoded test vectors
 */
function generateTestVectors(count = 10, seed = 0x3c732e0d) {
  const vectors = [];
  let current = seed;
  
  for (let i = 0; i < count; i++) {
    // Simple deterministic hash
    current = (current * 0x41c64e6d + 0x3039) >>> 0;
    const hex = current.toString(16).padStart(8, '0');
    vectors.push(hex);
  }
  
  return vectors;
}

module.exports = {
  PHI,
  goldenRatioSequence,
  goldenRatioCoinFlip,
  generateTestVectors,
  BinaryFusionTap,
};

// Default export
module.exports.default = module.exports;
`;

fs.writeFileSync(path.join(distDir, 'index.js'), indexContent);
console.log('✓ Created index.js');

// Create TypeScript definitions
const typesContent = `/**
 * GoldenSeed - Deterministic High-Entropy Byte Streams
 * 
 * @module golden-seed
 * @version 3.0.0
 */

/**
 * Golden Ratio constant (φ)
 */
export const PHI: number;

/**
 * Generate deterministic pseudo-random numbers using golden ratio
 * 
 * @param seed - Initial seed value
 * @param count - Number of values to generate
 * @returns Array of pseudo-random values in [0, 1)
 */
export function goldenRatioSequence(seed?: number, count?: number): number[];

/**
 * Deterministic coin flip based on golden ratio
 * 
 * @param index - Position in sequence
 * @returns true for heads, false for tails
 */
export function goldenRatioCoinFlip(index: number): boolean;

/**
 * Generate deterministic test vectors
 * 
 * @param count - Number of vectors to generate
 * @param seed - Initial seed value
 * @returns Array of hex-encoded test vectors
 */
export function generateTestVectors(count?: number, seed?: number): string[];

/**
 * Binary Fusion Tap implementation (if available)
 */
export const BinaryFusionTap: any;

export default {
  PHI,
  goldenRatioSequence,
  goldenRatioCoinFlip,
  generateTestVectors,
  BinaryFusionTap,
};
`;

fs.writeFileSync(path.join(distDir, 'index.d.ts'), typesContent);
console.log('✓ Created index.d.ts');

console.log('\n✓ Build complete! Distribution created in dist/');
