#!/usr/bin/env node

/**
 * Test script for GoldenSeed JavaScript package
 * Demonstrates basic usage of the golden-seed npm package
 */

const fs = require('fs');
const path = require('path');

// Check if dist/index.js exists
const distPath = path.join(__dirname, 'dist', 'index.js');
if (!fs.existsSync(distPath)) {
  console.error('Error: dist/index.js not found!');
  console.error('Please run: node build-js.js');
  process.exit(1);
}

const goldenSeed = require('./dist/index.js');

console.log('='.repeat(60));
console.log('GoldenSeed JavaScript Package Test');
console.log('='.repeat(60));
console.log();

// Test 1: Golden Ratio constant
console.log('1. Golden Ratio (φ):');
console.log('   φ =', goldenSeed.PHI);
console.log();

// Test 2: Golden Ratio Sequence
console.log('2. Golden Ratio Sequence (10 values):');
const sequence = goldenSeed.goldenRatioSequence(0, 10);
console.log('   ', sequence.map(v => v.toFixed(4)).join(', '));
console.log();

// Test 3: Coin Flips
console.log('3. Golden Ratio Coin Flips (20 flips):');
const coinFlips = Array.from({length: 20}, (_, i) => 
  goldenSeed.goldenRatioCoinFlip(i) ? 'H' : 'T'
).join('');
console.log('   ', coinFlips);
console.log();

// Test 4: Test Vectors
console.log('4. Test Vectors (5 vectors):');
const vectors = goldenSeed.generateTestVectors(5);
vectors.forEach((vector, i) => {
  console.log(`   Vector ${i}: ${vector}`);
});
console.log();

// Test 5: Statistics
console.log('5. Sequence Statistics (1000 values):');
const largeSequence = goldenSeed.goldenRatioSequence(0, 1000);
const avg = largeSequence.reduce((a, b) => a + b, 0) / largeSequence.length;
const min = Math.min(...largeSequence);
const max = Math.max(...largeSequence);
console.log(`   Mean: ${avg.toFixed(4)}`);
console.log(`   Min:  ${min.toFixed(4)}`);
console.log(`   Max:  ${max.toFixed(4)}`);
console.log();

// Test 6: Coin Flip Statistics
console.log('6. Coin Flip Statistics (10000 flips):');
let heads = 0;
for (let i = 0; i < 10000; i++) {
  if (goldenSeed.goldenRatioCoinFlip(i)) heads++;
}
const headsPercent = (heads / 10000 * 100).toFixed(2);
const tailsPercent = ((10000 - heads) / 10000 * 100).toFixed(2);
console.log(`   Heads: ${heads} (${headsPercent}%)`);
console.log(`   Tails: ${10000 - heads} (${tailsPercent}%)`);
console.log();

console.log('='.repeat(60));
console.log('✓ All tests completed successfully!');
console.log('='.repeat(60));
