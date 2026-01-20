# Binary Fusion Tap - Go Implementation

Version: 1.0.0
Release Date: 2026-01-03

## Installation

No external dependencies required.

## Building

```bash
go build binary_fusion_tap.go
```

## Usage

```go
package main

import "fmt"

func main() {
    result := BinaryFusionTap(11)
    fmt.Printf("K: %d\n", result.K)
    fmt.Printf("Tap State: 0b%s\n", result.TapState.Text(2))
}
```

## Running

```bash
go run binary_fusion_tap.go
```

## API

```go
type BinaryFusionResult struct {
    K                 int
    SeedValue         *big.Int
    BinarySeed        string
    TapState          *big.Int
    ZPEOverflow       *big.Int
    ZPEOverflowBinary string
}

func BinaryFusionTap(k int) *BinaryFusionResult
```

## License

Part of the COINjecture protocol.
