# Binary Fusion Tap - C Implementation

Version: 1.0.0
Release Date: 2026-01-03

## Compilation

```bash
gcc binary_fusion_tap.c -o binary_fusion_tap
```

With optimization:
```bash
gcc -O3 binary_fusion_tap.c -o binary_fusion_tap
```

## Usage

```c
#include "binary_fusion_tap.h"

int main() {
    BinaryFusionResult result = binary_fusion_tap(11);
    printf("K: %d\n", result.k);
    printf("ZPE Overflow: %llu\n", result.zpe_overflow);
    return 0;
}
```

## Running

```bash
./binary_fusion_tap
```

## API

```c
typedef struct {
    int k;
    uint64_t seed_value;
    uint64_t tap_state;
    uint64_t zpe_overflow;
} BinaryFusionResult;

BinaryFusionResult binary_fusion_tap(int k);
```

## Note

Uses `uint64_t` - supports k up to 15.
For larger k values, use GMP library.

## License

Part of the COINjecture protocol.
