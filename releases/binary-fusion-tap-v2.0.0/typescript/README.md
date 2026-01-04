# Binary Fusion Tap - TypeScript Implementation

Version: 2.0.0
Release Date: 2026-01-04

## Installation

```bash
npm install --save-dev typescript
```

## Compilation

```bash
tsc binary_fusion_tap.ts
```

## Usage

```typescript
import { binaryFusionTap, BinaryFusionResult } from './binary_fusion_tap';

const result: BinaryFusionResult = binaryFusionTap(11);
console.log(`K Parameter: ${result.k}`);
console.log(`Tap State: 0b${result.tapState}`);
```

## API

```typescript
interface BinaryFusionResult {
    k: number;
    seedValue: string;
    binarySeed: string;
    tapState: string;
    zpeOverflow: string;
    zpeOverflowDecimal: string;
}

function binaryFusionTap(k: number): BinaryFusionResult
```

## Running Compiled Code

```bash
node binary_fusion_tap.js
```

## License

Part of the COINjecture protocol.
