#include "pack12.hpp"
#include "pack12_vertical.hpp"

#include <algorithm>
#include <array>
#include <cstdint>
#include <exception>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

namespace {

// Independent oracle: set/read each of the 12 bits individually. This is
// intentionally unlike the word-shift implementation in pack12.hpp.
template <std::size_t N, std::size_t W>
std::array<std::uint64_t, W> oracle_pack64(const std::array<std::uint32_t, N>& values) {
    std::array<std::uint64_t, W> out{};
    for (std::size_t i = 0; i < N; ++i) {
        if (values[i] > 4095) throw std::runtime_error("oracle input invalid");
        for (unsigned b = 0; b < 12; ++b) {
            if ((values[i] >> b) & 1u) {
                const std::size_t absolute_bit = i * 12 + b;
                out[absolute_bit / 64] |= (std::uint64_t{1} << (absolute_bit % 64));
            }
        }
    }
    return out;
}

template <std::size_t N, std::size_t W>
std::array<std::uint32_t, N> oracle_unpack64(const std::array<std::uint64_t, W>& words) {
    std::array<std::uint32_t, N> out{};
    for (std::size_t i = 0; i < N; ++i) {
        for (unsigned b = 0; b < 12; ++b) {
            const std::size_t absolute_bit = i * 12 + b;
            if ((words[absolute_bit / 64] >> (absolute_bit % 64)) & 1u) {
                out[i] |= (std::uint32_t{1} << b);
            }
        }
    }
    return out;
}

template <std::size_t N, class PackFn, class UnpackFn>
void check64_case(const std::string& name, const std::array<std::uint32_t, N>& values,
                  PackFn pack_fn, UnpackFn unpack_fn, std::uint64_t& checks) {
    const auto packed = pack_fn(values);
    const auto oracle = oracle_pack64<N, packed.size()>(values);
    if (packed != oracle) throw std::runtime_error(name + ": packed words differ from independent bit oracle");
    if (unpack_fn(packed) != values) throw std::runtime_error(name + ": round-trip mismatch");
    if (oracle_unpack64<N>(oracle) != values) throw std::runtime_error(name + ": oracle round-trip mismatch");
    ++checks;
}

template <std::size_t N>
void run64_suite(const std::string& name, std::uint64_t& checks) {
    constexpr std::size_t W = (N * 12 + 63) / 64;
    auto p = [](const auto& x) { return pack12::pack<std::uint64_t>(x); };
    auto u = [](const auto& x) { return pack12::unpack<std::uint64_t, N>(x); };

    std::array<std::uint32_t, N> values{};
    check64_case<N>(name + "/zero", values, p, u, checks);
    values.fill(4095);
    check64_case<N>(name + "/all-ones", values, p, u, checks);
    for (std::size_t i = 0; i < N; ++i) {
        values.fill(0);
        values[i] = 4095;
        check64_case<N>(name + "/single-max-" + std::to_string(i), values, p, u, checks);
        values[i] = 1;
        check64_case<N>(name + "/single-lowbit-" + std::to_string(i), values, p, u, checks);
    }
    std::mt19937 rng(static_cast<std::uint32_t>(0xC0FFEEu + N));
    std::uniform_int_distribution<std::uint32_t> dist(0, 4095);
    for (unsigned iter = 0; iter < 20000; ++iter) {
        for (auto& x : values) x = dist(rng);
        check64_case<N>(name + "/random", values, p, u, checks);
    }
    (void)W;
}

template <std::size_t N>
void check32_case(const std::string& name, const std::array<std::uint32_t, N>& values,
                  std::uint64_t& checks) {
    const auto packed = pack12::pack<std::uint32_t>(values);
    // Independent reference for 32-bit word boundaries.
    std::array<std::uint32_t, (N * 12 + 31) / 32> oracle{};
    for (std::size_t i = 0; i < N; ++i) {
        for (unsigned b = 0; b < 12; ++b) {
            if ((values[i] >> b) & 1u) {
                const std::size_t pos = i * 12 + b;
                oracle[pos / 32] |= (std::uint32_t{1} << (pos % 32));
            }
        }
    }
    if (packed != oracle) throw std::runtime_error(name + ": 32-bit packed words differ from independent oracle");
    if (pack12::unpack<std::uint32_t, N>(packed) != values) throw std::runtime_error(name + ": 32-bit round-trip mismatch");
    ++checks;
}


void check_vertical_suites(std::uint64_t& checks) {
    std::mt19937 rng(0xB17B1A9u);
    std::uniform_int_distribution<std::uint32_t> dist(0, 4095);
    for (unsigned k = 0; k < 20000; ++k) {
        std::array<std::uint32_t, 16> a16{};
        std::array<std::uint32_t, 64> a64{};
        for (auto& x : a16) x = dist(rng);
        for (auto& x : a64) x = dist(rng);
        const auto p16 = pack12::vertical::pack_scalar<16, std::uint16_t>(a16);
        const auto p64 = pack12::vertical::pack_scalar<64, std::uint64_t>(a64);
        if (pack12::vertical::unpack_scalar<16>(p16) != a16) throw std::runtime_error("vertical scalar 16x round-trip mismatch");
        if (pack12::vertical::unpack_scalar<64>(p64) != a64) throw std::runtime_error("vertical scalar 64x round-trip mismatch");
        checks += 2;
#if PACK12_HAS_X86_TARGETS
        if (pack12::cpu_has_avx512f()) {
            const auto v16 = pack12::vertical::pack16_avx512(a16.data());
            const auto v64 = pack12::vertical::pack64_avx512(a64.data());
            if (v16 != p16) throw std::runtime_error("AVX-512 vertical 16x differs from scalar plane oracle");
            if (v64 != p64) throw std::runtime_error("AVX-512 vertical 64x differs from scalar plane oracle");
            if (pack12::vertical::unpack16_avx512(v16) != a16) throw std::runtime_error("AVX-512 vertical 16x decode mismatch");
            if (pack12::vertical::unpack64_avx512(v64) != a64) throw std::runtime_error("AVX-512 vertical 64x decode mismatch");
            checks += 4;
        }
#endif
    }
}

void check_rejects_invalid(std::uint64_t& checks) {
    std::array<std::uint32_t, 16> values{};
    values[7] = 4096;
    bool threw = false;
    try { (void)pack12::pack12_16x(values); }
    catch (const std::invalid_argument&) { threw = true; }
    if (!threw) throw std::runtime_error("scalar pack must reject 4096 rather than truncate it");
    ++checks;

#if PACK12_HAS_X86_TARGETS
    if (pack12::cpu_has_avx2()) {
        threw = false;
        try { (void)pack12::pack12_16x_avx2(values.data()); }
        catch (const std::invalid_argument&) { threw = true; }
        if (!threw) throw std::runtime_error("AVX2 pack must reject 4096 rather than truncate it");
        ++checks;
    }
    if (pack12::cpu_has_avx512f()) {
        threw = false;
        try { (void)pack12::vertical::pack16_avx512(values.data()); }
        catch (const std::invalid_argument&) { threw = true; }
        if (!threw) throw std::runtime_error("AVX-512 vertical pack must reject 4096 rather than truncate it");
        ++checks;
    }
    threw = false;
    try { (void)pack12::pack12_16x_avx2(nullptr); }
    catch (const std::invalid_argument&) { threw = true; }
    if (!threw) throw std::runtime_error("AVX2 pack must reject null input");
    ++checks;
#endif
}

#if PACK12_HAS_X86_TARGETS
void run_simd_checks(std::uint64_t& checks) {
    std::mt19937 rng(0x51D512u);
    std::uniform_int_distribution<std::uint32_t> dist(0, 4095);

    if (pack12::cpu_has_avx2()) {
        // Deliberately offset pointers exercise the loadu path rather than
        // relying on incidental stack alignment.
        std::array<std::uint32_t, 65> misaligned{};
        for (auto& x : misaligned) x = dist(rng);
        std::array<std::uint32_t, 16> a16{};
        std::copy_n(misaligned.data() + 1, 16, a16.begin());
        if (pack12::pack12_16x_avx2(misaligned.data() + 1) != pack12::pack12_16x(a16))
            throw std::runtime_error("AVX2 unaligned input mismatch");
        checks++;
    }
    if (pack12::cpu_has_avx512f()) {
        std::array<std::uint32_t, 65> misaligned{};
        for (auto& x : misaligned) x = dist(rng);
        std::array<std::uint32_t, 16> a16{};
        std::copy_n(misaligned.data() + 1, 16, a16.begin());
        if (pack12::pack12_16x_avx512(misaligned.data() + 1) != pack12::pack12_16x(a16))
            throw std::runtime_error("AVX-512 unaligned input mismatch");
        checks++;
    }

    if (pack12::cpu_has_avx2()) {
        for (unsigned k = 0; k < 10000; ++k) {
            std::array<std::uint32_t, 8> a8{};
            std::array<std::uint32_t, 16> a16{};
            std::array<std::uint32_t, 32> a32{};
            std::array<std::uint32_t, 64> a64{};
            for (auto& x : a8) x = dist(rng);
            for (auto& x : a16) x = dist(rng);
            for (auto& x : a32) x = dist(rng);
            for (auto& x : a64) x = dist(rng);
            if (pack12::pack12_8x_avx2(a8.data()) != pack12::pack12_8x(a8)) throw std::runtime_error("AVX2 8x mismatch");
            if (pack12::pack12_16x_avx2(a16.data()) != pack12::pack12_16x(a16)) throw std::runtime_error("AVX2 16x mismatch");
            if (pack12::pack12_32x_avx2(a32.data()) != pack12::pack12_32x(a32)) throw std::runtime_error("AVX2 32x mismatch");
            if (pack12::pack12_64x_avx2(a64.data()) != pack12::pack12_64x(a64)) throw std::runtime_error("AVX2 64x mismatch");
            checks += 4;
        }
    }
    if (pack12::cpu_has_avx512f()) {
        for (unsigned k = 0; k < 10000; ++k) {
            std::array<std::uint32_t, 16> a16{};
            std::array<std::uint32_t, 32> a32{};
            std::array<std::uint32_t, 64> a64{};
            for (auto& x : a16) x = dist(rng);
            for (auto& x : a32) x = dist(rng);
            for (auto& x : a64) x = dist(rng);
            if (pack12::pack12_16x_avx512(a16.data()) != pack12::pack12_16x(a16)) throw std::runtime_error("AVX-512 16x mismatch");
            if (pack12::pack12_32x_avx512(a32.data()) != pack12::pack12_32x(a32)) throw std::runtime_error("AVX-512 32x mismatch");
            if (pack12::pack12_64x_avx512(a64.data()) != pack12::pack12_64x(a64)) throw std::runtime_error("AVX-512 64x mismatch");
            checks += 3;
        }
    }
}
#endif


// Literal transcription of the supplied Grok 8x uint32_t formulas.
std::array<std::uint32_t, 3> grok_pack8_formula(const std::array<std::uint32_t, 8>& x) {
    for (auto v : x) if (v > 4095) throw std::invalid_argument("bad test input");
    const std::uint32_t a=x[0], b=x[1], c=x[2], d=x[3];
    const std::uint32_t e=x[4], f=x[5], g=x[6], h=x[7];
    std::array<std::uint32_t, 3> out{};
    out[0] = a | (b << 12) | (c << 24);
    out[1] = (c >> 8) | (d << 4) | (e << 16) | (f << 28);
    out[2] = (f >> 4) | (g << 8) | (h << 20);
    return out;
}
std::array<std::uint32_t, 8> grok_unpack8_formula(const std::array<std::uint32_t, 3>& in) {
    const auto w0=in[0], w1=in[1], w2=in[2];
    return {w0 & 0x0FFFu, (w0 >> 12) & 0x0FFFu,
            ((w0 >> 24) | (w1 << 8)) & 0x0FFFu,
            (w1 >> 4) & 0x0FFFu, (w1 >> 16) & 0x0FFFu,
            ((w1 >> 28) | (w2 << 4)) & 0x0FFFu,
            (w2 >> 8) & 0x0FFFu, (w2 >> 20) & 0x0FFFu};
}

// Literal 16-value 64-bit layout implied by the repeated formulas in the
// supplied 32x/64x examples. The source refers to unpack12_16x but omits it.
std::array<std::uint64_t, 3> grok_pack16_formula(const std::array<std::uint32_t, 16>& x) {
    for (auto v : x) if (v > 4095) throw std::invalid_argument("bad test input");
    auto v = [&](std::size_t i) -> std::uint64_t { return x[i]; };
    return {
        v(0) | (v(1)<<12) | (v(2)<<24) | (v(3)<<36) | (v(4)<<48) | (v(5)<<60),
        (v(5)>>4) | (v(6)<<8) | (v(7)<<20) | (v(8)<<32) | (v(9)<<44) | (v(10)<<56),
        (v(10)>>8) | (v(11)<<4) | (v(12)<<16) | (v(13)<<28) | (v(14)<<40) | (v(15)<<52)
    };
}
std::array<std::uint32_t, 16> grok_unpack16_formula(const std::array<std::uint64_t, 3>& w) {
    return {
        static_cast<std::uint32_t>(w[0] & 0x0FFFu),
        static_cast<std::uint32_t>((w[0] >> 12) & 0x0FFFu),
        static_cast<std::uint32_t>((w[0] >> 24) & 0x0FFFu),
        static_cast<std::uint32_t>((w[0] >> 36) & 0x0FFFu),
        static_cast<std::uint32_t>((w[0] >> 48) & 0x0FFFu),
        static_cast<std::uint32_t>(((w[0] >> 60) | (w[1] << 4)) & 0x0FFFu),
        static_cast<std::uint32_t>((w[1] >> 8) & 0x0FFFu),
        static_cast<std::uint32_t>((w[1] >> 20) & 0x0FFFu),
        static_cast<std::uint32_t>((w[1] >> 32) & 0x0FFFu),
        static_cast<std::uint32_t>((w[1] >> 44) & 0x0FFFu),
        static_cast<std::uint32_t>(((w[1] >> 56) | (w[2] << 8)) & 0x0FFFu),
        static_cast<std::uint32_t>((w[2] >> 4) & 0x0FFFu),
        static_cast<std::uint32_t>((w[2] >> 16) & 0x0FFFu),
        static_cast<std::uint32_t>((w[2] >> 28) & 0x0FFFu),
        static_cast<std::uint32_t>((w[2] >> 40) & 0x0FFFu),
        static_cast<std::uint32_t>((w[2] >> 52) & 0x0FFFu)
    };
}

void check_grok_formula_transcriptions(std::uint64_t& checks) {
    std::mt19937 rng(0xA771u);
    std::uniform_int_distribution<std::uint32_t> dist(0, 4095);
    for (unsigned k = 0; k < 50000; ++k) {
        std::array<std::uint32_t, 8> a8{};
        for (auto& x : a8) x=dist(rng);
        const auto p8 = grok_pack8_formula(a8);
        if (p8 != pack12::pack12_8x(a8) || p8 != pack12::pack12_8x_manual(a8) || grok_unpack8_formula(p8) != a8)
            throw std::runtime_error("literal Grok 8x formula mismatch");
        checks += 2;

        std::array<std::uint32_t, 16> a16{};
        for (auto& x : a16) x=dist(rng);
        const auto p16 = grok_pack16_formula(a16);
        if (p16 != pack12::pack12_16x(a16) || p16 != pack12::pack12_16x_manual(a16) || grok_unpack16_formula(p16) != a16)
            throw std::runtime_error("literal 16x formula mismatch");
        checks += 2;

        std::array<std::uint32_t, 32> a32{};
        for (auto& x : a32) x=dist(rng);
        const auto p32 = pack12::pack12_32x(a32);
        const std::array<std::uint32_t, 16> lo = [&] { std::array<std::uint32_t,16> a{}; std::copy_n(a32.begin(),16,a.begin()); return a; }();
        const std::array<std::uint32_t, 16> hi = [&] { std::array<std::uint32_t,16> a{}; std::copy_n(a32.begin()+16,16,a.begin()); return a; }();
        const auto g32lo = grok_pack16_formula(lo);
        const auto g32hi = grok_pack16_formula(hi);
        std::array<std::uint64_t, 6> g32{};
        std::copy(g32lo.begin(),g32lo.end(),g32.begin());
        std::copy(g32hi.begin(),g32hi.end(),g32.begin()+3);
        if (p32 != g32 || p32 != pack12::pack12_32x_manual(a32)) throw std::runtime_error("literal Grok 32x block composition mismatch");
        checks++;

        std::array<std::uint32_t, 64> a64{};
        for (auto& x : a64) x=dist(rng);
        const auto p64 = pack12::pack12_64x(a64);
        std::array<std::uint64_t, 12> g64{};
        for (std::size_t block=0; block<4; ++block) {
            std::array<std::uint32_t,16> a{};
            std::copy_n(a64.begin()+static_cast<std::ptrdiff_t>(block*16),16,a.begin());
            const auto g = grok_pack16_formula(a);
            std::copy(g.begin(),g.end(),g64.begin()+static_cast<std::ptrdiff_t>(block*3));
        }
        if (p64 != g64 || p64 != pack12::pack12_64x_manual(a64)) throw std::runtime_error("literal Grok 64x block composition mismatch");
        checks++;
    }
}

} // namespace

int main() {
    try {
        std::uint64_t checks = 0;
        run64_suite<4>("4x-u64", checks);
        run64_suite<16>("16x-u64", checks);
        run64_suite<32>("32x-u64", checks);
        run64_suite<64>("64x-u64", checks);
        std::array<std::uint32_t, 8> a8{};
        check32_case("8x-u32", a8, checks);
        a8.fill(4095);
        check32_case("8x-u32-all-max", a8, checks);
        for (std::size_t i = 0; i < 8; ++i) {
            a8.fill(0); a8[i] = 4095;
            check32_case("8x-u32-single-max", a8, checks);
        }
        std::mt19937 rng(0x832u);
        std::uniform_int_distribution<std::uint32_t> dist(0, 4095);
        for (unsigned k = 0; k < 20000; ++k) {
            for (auto& x : a8) x = dist(rng);
            check32_case("8x-u32-random", a8, checks);
        }
        check_rejects_invalid(checks);
        check_grok_formula_transcriptions(checks);
        check_vertical_suites(checks);
#if PACK12_HAS_X86_TARGETS
        run_simd_checks(checks);
        std::cout << "CPU AVX2=" << (pack12::cpu_has_avx2() ? "yes" : "no")
                  << "; AVX-512F=" << (pack12::cpu_has_avx512f() ? "yes" : "no") << '\n';
#else
        std::cout << "SIMD tests not built for this compiler/architecture\n";
#endif
        std::cout << "PASS: " << checks << " independent/reference/round-trip/rejection checks\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "FAIL: " << e.what() << '\n';
        return 1;
    }
}
