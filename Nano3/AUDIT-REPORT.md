# Audit report — 12-bit packing source

## Scope

Reviewed the full 288-line supplied text: 8-value AVX2 pack/unpack, the 32- and 64-value AVX2 horizontal formulas, the 16- and 32-value AVX-512 horizontal formulas, the stated size table, and the proposed vertical bit-plane follow-up.

This report is about the code and claims present in that source. It does not establish that Grok executed or benchmarked the code in the source conversation.

## Findings

### Horizontal layout

The horizontal bit layout is internally consistent:

| Values | Bits | Packed words |
|---:|---:|---|
| 4 | 48 | 1 × `uint64_t` |
| 8 | 96 | 3 × `uint32_t` |
| 16 | 192 | 3 × `uint64_t` |
| 32 | 384 | 6 × `uint64_t` |
| 64 | 768 | 12 × `uint64_t` |

The supplied 8-value packing expressions and matching unpack expressions agree with an independent bit-by-bit reference. The repeated 16-value layout used by the supplied 32- and 64-value functions also agrees with the same reference.

### Defects and missing contract

1. The supplied 32- and 64-value unpack functions call `unpack12_16x`, but its implementation is absent from the supplied excerpt. Without it, those functions are not self-contained. A matching implementation is supplied and tested here.
2. `value & 0x0FFF` / SIMD mask operations discard all bits above bit 11. The source does not reject invalid input. This can turn an invalid value into a different valid value without reporting an error. The checked functions in this package reject values outside `0..4095` before SIMD work.
3. The code uses fixed-size raw pointers without a length parameter. The caller must provide enough readable elements. This is documented; an API accepting a sized span would be safer for general use.
4. The source gives integer-word layouts but does not specify a byte serialization endianness. Integer equality does not alone define a portable byte-for-byte interchange format.
5. The shown AVX2/AVX-512 methods accelerate loads and masking, then spill to a temporary array and perform scalar shifts/ORs. They are not fully vectorized horizontal packers. The source itself acknowledges that the horizontal layout remains irregular.
6. The 16-value AVX-512 code is one 512-bit load and mask, followed by scalar horizontal placement. The source's 32-value AVX-512 code repeats that operation twice. AVX-512 mask registers are not used for horizontal placement in the shown code.
7. The 4-value and 16-value entries in the source's comparison table are size claims only in this excerpt; their corresponding full implementations are not supplied here. This package implements those sizes independently.

## Verification performed

The final test executable reports:

`PASS: 590256 independent/reference/round-trip/rejection checks`

The checks include:

- independent bit-by-bit packing and unpacking oracles for 4-, 16-, 32-, and 64-value 64-bit-word layouts;
- an independent 32-bit-word oracle for the 8-value layout;
- zero, all-maximum, one-hot and 20,000 seeded random input cases per block family;
- 50,000 random trials comparing literal 8-value and implied 16-value formulas with the independent implementation, plus 32-/64-value block composition;
- 20,000 random vertical 16- and 64-value bit-plane cases, scalar reference comparisons and AVX-512 decode round trips;
- 10,000 random SIMD differential trials per AVX2/AVX-512 block family;
- out-of-range rejection, null-pointer rejection, and intentionally unaligned input pointers.

Builds passed with GCC 14.2.0 and Clang 17.0.0. GCC AddressSanitizer and UndefinedBehaviorSanitizer run passed. The test CPU reports AVX2 and AVX-512F support, so those paths were actually exercised in this environment. On a machine without those features, the scalar code remains available and runtime-gated SIMD tests are skipped.

## Local performance experiment

Environment: AMD EPYC 9V74, GCC 14.2.0, `-O3 -DNDEBUG`; each run processed 4,096 blocks over 40 passes. The table below gives the median of five runs, in nanoseconds per block. Results vary by workload, compiler, CPU frequency, cache state and other system activity; they are not portable performance guarantees.

| Encoding / kernel | 8 values | 16 values | 32 values | 64 values |
|---|---:|---:|---:|---:|
| Horizontal scalar formula, raw prevalidated input | 1.94 | 6.09 | 21.65 | 38.89 |
| Horizontal AVX2 load/mask + scalar placement, raw | 8.87 | 8.32 | 20.53 | 39.42 |
| Horizontal AVX-512 load/mask + scalar placement, raw | — | 9.43 | 24.28 | 41.38 |
| Horizontal checked AVX2 API | 9.67 | 11.20 | 29.29 | 43.83 |
| Horizontal checked AVX-512 API | — | 11.23 | 28.14 | 55.29 |

For this implementation and machine, the horizontal AVX versions did not show a reliable general speedup over the scalar formula. The 32-value AVX2 raw result was slightly lower than the scalar median, but the difference is small and ranges overlap; it is not sufficient to claim a robust win. The 8- and 16-value horizontal AVX paths were slower in this experiment.

The vertical AVX-512 implementation uses AVX-512 compare-to-mask instructions and mask-to-vector reconstruction. It is compared against the scalar implementation of the **same vertical format**, not against the horizontal format:

| Vertical bit-plane format | Scalar median | AVX-512 median |
|---|---:|---:|
| 16 values | 544.55 ns/block | 14.84 ns/block |
| 64 values | 2,235.39 ns/block | 50.32 ns/block |

This demonstrates a substantial local improvement for this straightforward scalar bit-plane reference. It does not prove vertical packing is faster for every application: the representation differs, and end-to-end use must account for conversion, access pattern, compression consumer, decode cost, and cache behavior.

## Conclusions

- The supplied horizontal bit formulas are mathematically consistent for valid 12-bit inputs.
- The supplied excerpt is incomplete as a stand-alone implementation because `unpack12_16x` is missing.
- The omission of input validation is a correctness/API hazard, not just a style concern.
- The shown AVX2/AVX-512 horizontal code is SIMD-assisted, not fully vectorized horizontal packing. Local measurements do not establish a general speedup.
- Vertical AVX-512 bit-plane packing is implemented and tested as a distinct format. Its local speedup is promising for bit-plane workloads, but format conversion and application-level benchmarks remain necessary.

No external publication, repository change, independent third-party audit, or formal performance certification is claimed.
