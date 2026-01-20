//! Binary Fusion Tap - Rust Implementation
//! Quantum-inspired key generation using 8-fold Heartbeat and ZPE Overflow

use std::fmt;

#[derive(Debug, Clone)]
pub struct BinaryFusionResult {
    pub k: u64,
    pub seed_value: u128,
    pub binary_seed: String,
    pub tap_state: u128,
    pub zpe_overflow: u128,
}

impl fmt::Display for BinaryFusionResult {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "K: {}\nSeed: {}\nTap State: {:b}\nZPE Overflow: {:b}",
            self.k, self.seed_value, self.tap_state, self.zpe_overflow
        )
    }
}

/// Generate binary fusion tap with 8-fold heartbeat and ZPE overflow
///
/// # Arguments
/// * `k` - Tap parameter (recommended: 11 for optimal entropy)
///
/// # Returns
/// * `BinaryFusionResult` - Key generation data
pub fn binary_fusion_tap(k: u64) -> BinaryFusionResult {
    // 1. Generate seed from concatenated sequence
    let mut seed_str = String::new();
    for i in 1..=k {
        seed_str.push_str(&i.to_string());
    }
    let seed_val: u128 = seed_str.parse().expect("Failed to parse seed");

    // 2. Apply 8-fold Heartbeat (bit-shift left by 3)
    let heartbeat_val = seed_val << 3;

    // 3. Add Phase Offset
    let manifested = heartbeat_val + (k as u128);

    // 4. Extract ZPE Overflow
    let overflow = if k < 10 {
        0
    } else {
        manifested ^ (seed_val * 8)
    };

    BinaryFusionResult {
        k,
        seed_value: seed_val,
        binary_seed: format!("{:b}", seed_val),
        tap_state: manifested,
        zpe_overflow: overflow,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_k11() {
        let result = binary_fusion_tap(11);
        assert_eq!(result.k, 11);
        assert_eq!(result.seed_value, 1234567891011);
        assert_eq!(result.zpe_overflow, 59);
    }
}

fn main() {
    let result = binary_fusion_tap(11);
    println!("{}", result);
}
