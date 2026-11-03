#pragma once

#include "pack12.hpp"

#include <array>
#include <cstddef>
#include <cstdint>
#include <stdexcept>

namespace pack12::vertical {

// A plane stores one bit from each input value. Plane b, lane i is bit b of
// input[i]. This is a different wire format from pack12.hpp's horizontal
// sequential stream, despite having exactly the same bit count.
template <std::size_t N, class PlaneWord>
using planes_array = std::array<PlaneWord, 12>;

template <std::size_t N, class PlaneWord>
[[nodiscard]] planes_array<N, PlaneWord>
pack_scalar(const std::array<std::uint32_t, N>& values) {
    static_assert(N == 16 || N == 64, "vertical reference supports 16 or 64 values");
    static_assert(std::is_unsigned_v<PlaneWord>);
    static_assert(sizeof(PlaneWord) * 8 >= N);
    planes_array<N, PlaneWord> out{};
    for (std::size_t i = 0; i < N; ++i) {
        validate_value(values[i]);
        for (unsigned b = 0; b < 12; ++b) {
            if ((values[i] >> b) & 1u) out[b] = static_cast<PlaneWord>(out[b] | static_cast<PlaneWord>(PlaneWord{1} << i));
        }
    }
    return out;
}

template <std::size_t N, class PlaneWord>
[[nodiscard]] std::array<std::uint32_t, N>
unpack_scalar(const planes_array<N, PlaneWord>& planes) {
    static_assert(N == 16 || N == 64, "vertical reference supports 16 or 64 values");
    static_assert(std::is_unsigned_v<PlaneWord>);
    static_assert(sizeof(PlaneWord) * 8 >= N);
    std::array<std::uint32_t, N> out{};
    for (std::size_t i = 0; i < N; ++i) {
        for (unsigned b = 0; b < 12; ++b) {
            if ((planes[b] >> i) & PlaneWord{1}) out[i] |= (std::uint32_t{1} << b);
        }
    }
    return out;
}

#if PACK12_HAS_X86_TARGETS

// AVX-512 implementation for 16 values. Each compare produces one 16-bit
// mask-register result. This really does use AVX-512 k-mask registers.
PACK12_TARGET_AVX512 inline std::array<std::uint16_t, 12>
pack16_avx512(const std::uint32_t* input) {
    pack12::validate_input<16>(input);
    const __m512i values = _mm512_loadu_si512(reinterpret_cast<const void*>(input));
    const __m512i zero = _mm512_setzero_si512();
    std::array<std::uint16_t, 12> planes{};
    for (unsigned b = 0; b < 12; ++b) {
        const __m512i bit = _mm512_set1_epi32(static_cast<int>(std::uint32_t{1} << b));
        const __m512i selected = _mm512_and_si512(values, bit);
        const __mmask16 mask = _mm512_cmpneq_epi32_mask(selected, zero);
        planes[b] = static_cast<std::uint16_t>(mask);
    }
    return planes;
}

PACK12_TARGET_AVX512 inline std::array<std::uint32_t, 16>
unpack16_avx512(const std::array<std::uint16_t, 12>& planes) {
    __m512i values = _mm512_setzero_si512();
    for (unsigned b = 0; b < 12; ++b) {
        const __mmask16 mask = static_cast<__mmask16>(planes[b]);
        const __m512i bits = _mm512_maskz_set1_epi32(mask, static_cast<int>(std::uint32_t{1} << b));
        values = _mm512_or_si512(values, bits);
    }
    std::array<std::uint32_t, 16> out{};
    _mm512_storeu_si512(reinterpret_cast<void*>(out.data()), values);
    return out;
}

// Four 16-lane vectors become four 16-bit pieces of each 64-lane plane.
// 12 x uint64_t = 768 bits = 64 x 12 bits.
PACK12_TARGET_AVX512 inline std::array<std::uint64_t, 12>
pack64_avx512(const std::uint32_t* input) {
    pack12::validate_input<64>(input);
    const __m512i zero = _mm512_setzero_si512();
    const __m512i bit_masks[12] = {
        _mm512_set1_epi32(1 << 0), _mm512_set1_epi32(1 << 1),
        _mm512_set1_epi32(1 << 2), _mm512_set1_epi32(1 << 3),
        _mm512_set1_epi32(1 << 4), _mm512_set1_epi32(1 << 5),
        _mm512_set1_epi32(1 << 6), _mm512_set1_epi32(1 << 7),
        _mm512_set1_epi32(1 << 8), _mm512_set1_epi32(1 << 9),
        _mm512_set1_epi32(1 << 10), _mm512_set1_epi32(1 << 11)
    };
    std::array<std::uint64_t, 12> planes{};
    for (unsigned chunk = 0; chunk < 4; ++chunk) {
        const __m512i values = _mm512_loadu_si512(reinterpret_cast<const void*>(input + chunk * 16));
        for (unsigned b = 0; b < 12; ++b) {
            const __m512i selected = _mm512_and_si512(values, bit_masks[b]);
            const __mmask16 mask = _mm512_cmpneq_epi32_mask(selected, zero);
            planes[b] |= static_cast<std::uint64_t>(mask) << (chunk * 16);
        }
    }
    return planes;
}

PACK12_TARGET_AVX512 inline std::array<std::uint32_t, 64>
unpack64_avx512(const std::array<std::uint64_t, 12>& planes) {
    std::array<std::uint32_t, 64> out{};
    for (unsigned chunk = 0; chunk < 4; ++chunk) {
        __m512i values = _mm512_setzero_si512();
        for (unsigned b = 0; b < 12; ++b) {
            const auto mask_bits = static_cast<std::uint16_t>((planes[b] >> (chunk * 16)) & 0xFFFFu);
            const __mmask16 mask = static_cast<__mmask16>(mask_bits);
            const __m512i bits = _mm512_maskz_set1_epi32(mask, static_cast<int>(std::uint32_t{1} << b));
            values = _mm512_or_si512(values, bits);
        }
        _mm512_storeu_si512(reinterpret_cast<void*>(out.data() + chunk * 16), values);
    }
    return out;
}

#endif // PACK12_HAS_X86_TARGETS

} // namespace pack12::vertical
