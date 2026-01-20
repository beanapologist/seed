# Binary Fusion Tap - JavaScript Implementation

Version: 1.0.0
Release Date: 2026-01-03

## Installation

No dependencies. Works in Node.js 10.4+ and modern browsers.

## Usage

```javascript
const { binaryFusionTap } = require('./binary_fusion_tap');

const result = binaryFusionTap(11);
console.log(`K Parameter: ${result.k}`);
console.log(`Tap State: 0b${result.tapState}`);
console.log(`ZPE Overflow: 0b${result.zpeOverflow}`);
```

## Running

```bash
node binary_fusion_tap.js
```

## Browser Usage

```html
<script src="binary_fusion_tap.js"></script>
<script>
  const result = binaryFusionTap(11);
  console.log(result);
</script>
```

## API

```javascript
binaryFusionTap(k: number): Object
```

Returns object with:
- `k`: Tap parameter
- `seedValue`: Generated seed (BigInt string)
- `binarySeed`: Binary representation
- `tapState`: Manifested state (binary string)
- `zpeOverflow`: ZPE overflow (binary string)
- `zpeOverflowDecimal`: ZPE as decimal string

## License

Part of the COINjecture protocol.
