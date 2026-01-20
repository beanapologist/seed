# Binary Fusion Tap - Rust Implementation

Version: 1.0.0
Release Date: 2026-01-03

## Compilation

```bash
rustc binary_fusion_tap.rs
```

Or with Cargo:
```bash
cargo build --release
```

## Usage

```rust
use binary_fusion_tap::binary_fusion_tap;

fn main() {
    let result = binary_fusion_tap(11);
    println!("K: {}", result.k);
    println!("Tap State: {:b}", result.tap_state);
}
```

## Running

```bash
./binary_fusion_tap
```

## API

```rust
pub struct BinaryFusionResult {
    pub k: u64,
    pub seed_value: u128,
    pub binary_seed: String,
    pub tap_state: u128,
    pub zpe_overflow: u128,
}

pub fn binary_fusion_tap(k: u64) -> BinaryFusionResult
```

## Testing

```bash
cargo test
```

## License

Part of the COINjecture protocol.
