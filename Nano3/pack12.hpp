#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <type_traits>

#if (defined(__x86_64__) || defined(__i386__)) && (defined(__GNUC__) || defined(__clang__))
  #include <immintrin.h>
  #define PACK12_HAS_X86_TARGETS 1
  #define PACK12_TARGET_AVX2 __attribute__((target("avx2")))
  #define PACK12_TARGET_AVX512 __attribute__((target("avx512f")))
#else
  #define PACK12_HAS_X86_TARGETS 0
  #define PACK12_TARGET_AVX2
  #define PACK12_TARGET_AVX512
#endif

namespace pack12 {

inline constexpr std::uint32_t value_mask = 0x0FFFu;
inline constexpr unsigned value_bits = 12;

inline void validate_value(std::uint32_t value) {
    if (value > value_mask) {
        throw std::invalid_argument("12-bit value out of range (expected 0..4095)");
    }
}

template <class Word, std::size_t N>
using packed_array = std::array<Word, (N * value_bits + sizeof(Word) * 8 - 1) / (sizeof(Word) * 8)>;

// Canonical little-bit-order stream: value 0 occupies the least-significant
// 12 bits, then value 1, and so on. Word type controls chunk boundaries.
// The returned numeric words are host-endian C++ integers; byte serialization
// must specify an endian convention separately.
template <class Word, std::size_t N>
[[nodiscard]] packed_array<Word, N> pack(const std::array<std::uint32_t, N>& values) {
    static_assert(std::is_unsigned_v<Word>, "packed word type must be unsigned");
    constexpr unsigned word_bits = sizeof(Word) * 8;
    static_assert(word_bits == 32 || word_bits == 64, "use 32- or 64-bit words");

    packed_array<Word, N> out{};
    for (std::size_t i = 0; i < N; ++i) {
        validate_value(values[i]);
        const std::size_t bit = i * value_bits;
        const std::size_t word_index = bit / word_bits;
        const unsigned shift = static_cast<unsigned>(bit % word_bits);
        out[word_index] |= static_cast<Word>(values[i]) << shift;
        if (shift > word_bits - value_bits) {
            out[word_index + 1] |= static_cast<Word>(values[i]) >> (word_bits - shift);
        }
    }
    return out;
}

template <class Word, std::size_t N>
[[nodiscard]] std::array<std::uint32_t, N> unpack(const packed_array<Word, N>& words) {
    static_assert(std::is_unsigned_v<Word>, "packed word type must be unsigned");
    constexpr unsigned word_bits = sizeof(Word) * 8;
    static_assert(word_bits == 32 || word_bits == 64, "use 32- or 64-bit words");

    std::array<std::uint32_t, N> out{};
    for (std::size_t i = 0; i < N; ++i) {
        const std::size_t bit = i * value_bits;
        const std::size_t word_index = bit / word_bits;
        const unsigned shift = static_cast<unsigned>(bit % word_bits);
        Word value = words[word_index] >> shift;
        if (shift > word_bits - value_bits) {
            value |= words[word_index + 1] << (word_bits - shift);
        }
        out[i] = static_cast<std::uint32_t>(value & static_cast<Word>(value_mask));
    }
    return out;
}

template <std::size_t N>
inline void validate_input(const std::uint32_t* input) {
    if (input == nullptr) throw std::invalid_argument("input pointer is null");
    for (std::size_t i = 0; i < N; ++i) validate_value(input[i]);
}

// Unchecked formula helpers. Call only after validating all inputs or after a
// SIMD mask stage that is paired with validation. These reproduce the
// horizontal bit layout shown in the supplied 8x/32x/64x source.
[[nodiscard]] inline std::array<std::uint32_t, 3>
pack8_formula_valid(const std::uint32_t* t) {
    const std::uint32_t a=t[0], b=t[1], c=t[2], d=t[3];
    const std::uint32_t e=t[4], f=t[5], g=t[6], h=t[7];
    return {a | (b << 12) | (c << 24),
            (c >> 8) | (d << 4) | (e << 16) | (f << 28),
            (f >> 4) | (g << 8) | (h << 20)};
}

[[nodiscard]] inline std::array<std::uint64_t, 3>
pack16_formula_valid(const std::uint32_t* t) {
    const std::uint64_t a=t[0], b=t[1], c=t[2], d=t[3];
    const std::uint64_t e=t[4], f=t[5], g=t[6], h=t[7];
    const std::uint64_t i=t[8], j=t[9], k=t[10], l=t[11];
    const std::uint64_t m=t[12], n=t[13], o=t[14], p=t[15];
    return {a | (b << 12) | (c << 24) | (d << 36) | (e << 48) | (f << 60),
            (f >> 4) | (g << 8) | (h << 20) | (i << 32) | (j << 44) | (k << 56),
            (k >> 8) | (l << 4) | (m << 16) | (n << 28) | (o << 40) | (p << 52)};
}

// Checked scalar formula entry points. These are useful baselines against the
// generic, easier-to-audit bitstream loop below.
[[nodiscard]] inline std::array<std::uint32_t, 3>
pack12_8x_manual(const std::array<std::uint32_t, 8>& v) {
    for (auto x : v) validate_value(x);
    return pack8_formula_valid(v.data());
}
[[nodiscard]] inline std::array<std::uint64_t, 3>
pack12_16x_manual(const std::array<std::uint32_t, 16>& v) {
    for (auto x : v) validate_value(x);
    return pack16_formula_valid(v.data());
}
[[nodiscard]] inline std::array<std::uint64_t, 6>
pack12_32x_manual(const std::array<std::uint32_t, 32>& v) {
    for (auto x : v) validate_value(x);
    std::array<std::uint64_t, 6> out{};
    for (std::size_t block = 0; block < 2; ++block) {
        const auto part = pack16_formula_valid(v.data() + block * 16);
        for (std::size_t j = 0; j < 3; ++j) out[block * 3 + j] = part[j];
    }
    return out;
}
[[nodiscard]] inline std::array<std::uint64_t, 12>
pack12_64x_manual(const std::array<std::uint32_t, 64>& v) {
    for (auto x : v) validate_value(x);
    std::array<std::uint64_t, 12> out{};
    for (std::size_t block = 0; block < 4; ++block) {
        const auto part = pack16_formula_valid(v.data() + block * 16);
        for (std::size_t j = 0; j < 3; ++j) out[block * 3 + j] = part[j];
    }
    return out;
}

// Scalar fixed-size entry points matching the block sizes in the reviewed text.
[[nodiscard]] inline std::array<std::uint32_t, 3> pack12_8x(const std::array<std::uint32_t, 8>& v) {
    return pack<std::uint32_t>(v);
}
[[nodiscard]] inline std::array<std::uint64_t, 1> pack12_4x(const std::array<std::uint32_t, 4>& v) {
    return pack<std::uint64_t>(v);
}
[[nodiscard]] inline std::array<std::uint64_t, 3> pack12_16x(const std::array<std::uint32_t, 16>& v) {
    return pack<std::uint64_t>(v);
}
[[nodiscard]] inline std::array<std::uint64_t, 6> pack12_32x(const std::array<std::uint32_t, 32>& v) {
    return pack<std::uint64_t>(v);
}
[[nodiscard]] inline std::array<std::uint64_t, 12> pack12_64x(const std::array<std::uint32_t, 64>& v) {
    return pack<std::uint64_t>(v);
}

[[nodiscard]] inline std::array<std::uint32_t, 8> unpack12_8x(const std::array<std::uint32_t, 3>& v) {
    return unpack<std::uint32_t, 8>(v);
}
[[nodiscard]] inline std::array<std::uint32_t, 4> unpack12_4x(const std::array<std::uint64_t, 1>& v) {
    return unpack<std::uint64_t, 4>(v);
}
[[nodiscard]] inline std::array<std::uint32_t, 16> unpack12_16x(const std::array<std::uint64_t, 3>& v) {
    return unpack<std::uint64_t, 16>(v);
}
[[nodiscard]] inline std::array<std::uint32_t, 32> unpack12_32x(const std::array<std::uint64_t, 6>& v) {
    return unpack<std::uint64_t, 32>(v);
}
[[nodiscard]] inline std::array<std::uint32_t, 64> unpack12_64x(const std::array<std::uint64_t, 12>& v) {
    return unpack<std::uint64_t, 64>(v);
}

#if PACK12_HAS_X86_TARGETS
inline bool cpu_has_avx2() {
    __builtin_cpu_init();
    return __builtin_cpu_supports("avx2");
}
inline bool cpu_has_avx512f() {
    __builtin_cpu_init();
    return __builtin_cpu_supports("avx512f");
}

// These deliberately mirror the strategy in the supplied code: SIMD load +
// 12-bit mask, followed by the same canonical scalar bit placement. They are
// not claimed to be fully vectorized horizontal packers.
PACK12_TARGET_AVX2 inline std::array<std::uint32_t, 3>
pack12_8x_avx2(const std::uint32_t* input) {
    validate_input<8>(input);
    const __m256i mask = _mm256_set1_epi32(static_cast<int>(value_mask));
    __m256i v = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input));
    v = _mm256_and_si256(v, mask);
    alignas(32) std::uint32_t temp[8];
    _mm256_store_si256(reinterpret_cast<__m256i*>(temp), v);
    return pack8_formula_valid(temp);
}

PACK12_TARGET_AVX2 inline std::array<std::uint64_t, 3>
pack12_16x_avx2(const std::uint32_t* input) {
    validate_input<16>(input);
    const __m256i mask = _mm256_set1_epi32(static_cast<int>(value_mask));
    alignas(32) std::uint32_t temp[16];
    for (std::size_t i = 0; i < 16; i += 8) {
        __m256i v = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input + i));
        v = _mm256_and_si256(v, mask);
        _mm256_store_si256(reinterpret_cast<__m256i*>(temp + i), v);
    }
    return pack16_formula_valid(temp);
}

PACK12_TARGET_AVX2 inline std::array<std::uint64_t, 6>
pack12_32x_avx2(const std::uint32_t* input) {
    validate_input<32>(input);
    const __m256i mask = _mm256_set1_epi32(static_cast<int>(value_mask));
    alignas(32) std::uint32_t temp[32];
    for (std::size_t i = 0; i < 32; i += 8) {
        __m256i v = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input + i));
        v = _mm256_and_si256(v, mask);
        _mm256_store_si256(reinterpret_cast<__m256i*>(temp + i), v);
    }
    std::array<std::uint64_t, 6> out{};
    for (std::size_t block = 0; block < 2; ++block) {
        const auto part = pack16_formula_valid(temp + block * 16);
        for (std::size_t j = 0; j < 3; ++j) out[block * 3 + j] = part[j];
    }
    return out;
}

PACK12_TARGET_AVX2 inline std::array<std::uint64_t, 12>
pack12_64x_avx2(const std::uint32_t* input) {
    validate_input<64>(input);
    const __m256i mask = _mm256_set1_epi32(static_cast<int>(value_mask));
    alignas(32) std::uint32_t temp[64];
    for (std::size_t i = 0; i < 64; i += 8) {
        __m256i v = _mm256_loadu_si256(reinterpret_cast<const __m256i*>(input + i));
        v = _mm256_and_si256(v, mask);
        _mm256_store_si256(reinterpret_cast<__m256i*>(temp + i), v);
    }
    std::array<std::uint64_t, 12> out{};
    for (std::size_t block = 0; block < 4; ++block) {
        const auto part = pack16_formula_valid(temp + block * 16);
        for (std::size_t j = 0; j < 3; ++j) out[block * 3 + j] = part[j];
    }
    return out;
}

PACK12_TARGET_AVX512 inline std::array<std::uint64_t, 3>
pack12_16x_avx512(const std::uint32_t* input) {
    validate_input<16>(input);
    __m512i v = _mm512_loadu_si512(reinterpret_cast<const void*>(input));
    v = _mm512_and_si512(v, _mm512_set1_epi32(static_cast<int>(value_mask)));
    alignas(64) std::uint32_t temp[16];
    _mm512_store_si512(reinterpret_cast<void*>(temp), v);
    return pack16_formula_valid(temp);
}

PACK12_TARGET_AVX512 inline std::array<std::uint64_t, 6>
pack12_32x_avx512(const std::uint32_t* input) {
    validate_input<32>(input);
    const __m512i mask = _mm512_set1_epi32(static_cast<int>(value_mask));
    alignas(64) std::uint32_t temp[32];
    for (std::size_t i = 0; i < 32; i += 16) {
        __m512i v = _mm512_loadu_si512(reinterpret_cast<const void*>(input + i));
        v = _mm512_and_si512(v, mask);
        _mm512_store_si512(reinterpret_cast<void*>(temp + i), v);
    }
    std::array<std::uint64_t, 6> out{};
    for (std::size_t block = 0; block < 2; ++block) {
        const auto part = pack16_formula_valid(temp + block * 16);
        for (std::size_t j = 0; j < 3; ++j) out[block * 3 + j] = part[j];
    }
    return out;
}

PACK12_TARGET_AVX512 inline std::array<std::uint64_t, 12>
pack12_64x_avx512(const std::uint32_t* input) {
    validate_input<64>(input);
    const __m512i mask = _mm512_set1_epi32(static_cast<int>(value_mask));
    alignas(64) std::uint32_t temp[64];
    for (std::size_t i = 0; i < 64; i += 16) {
        __m512i v = _mm512_loadu_si512(reinterpret_cast<const void*>(input + i));
        v = _mm512_and_si512(v, mask);
        _mm512_store_si512(reinterpret_cast<void*>(temp + i), v);
    }
    std::array<std::uint64_t, 12> out{};
    for (std::size_t block = 0; block < 4; ++block) {
        const auto part = pack16_formula_valid(temp + block * 16);
        for (std::size_t j = 0; j < 3; ++j) out[block * 3 + j] = part[j];
    }
    return out;
}
#endif

} // namespace pack12
