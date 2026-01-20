# Binary Fusion Tap - Java Implementation

Version: 1.0.0
Release Date: 2026-01-03

## Compilation

```bash
javac BinaryFusionTap.java
```

## Usage

```java
public class Main {
    public static void main(String[] args) {
        BinaryFusionTap.Result result = BinaryFusionTap.generate(11);
        System.out.println("K: " + result.k);
        System.out.println("Tap State: 0b" + result.tapState.toString(2));
    }
}
```

## Running

```bash
java BinaryFusionTap
```

## API

```java
public class BinaryFusionTap {
    public static class Result {
        public int k;
        public BigInteger seedValue;
        public String binarySeed;
        public BigInteger tapState;
        public BigInteger zpeOverflow;
        public String zpeOverflowBinary;
    }

    public static Result generate(int k);
}
```

## License

Part of the COINjecture protocol.
