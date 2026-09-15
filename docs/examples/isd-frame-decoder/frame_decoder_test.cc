#include "frame_decoder.h"
#include <array>
#include <cstdlib>
#include <iostream>
#include <thread>
#include <vector>

using namespace ex_isd;
namespace {
void check(bool condition, const char* name) {
    if (!condition) { std::cerr << "FAIL: " << name << '\n'; std::exit(1); }
}
void invalid(std::span<const std::uint8_t> input, InvalidReason reason, const char* name) {
    const auto result = decode_one(input);
    const auto* error = std::get_if<Invalid>(&result);
    check(error && error->reason == reason && error->consumed == 0, name);
}
void need_more(std::span<const std::uint8_t> input, const char* name) {
    const auto result = decode_one(input);
    const auto* more = std::get_if<NeedMore>(&result);
    check(more && more->consumed == 0, name);
}
}

int main() {
    const std::array<std::uint8_t, 8> normal{1, 1, 0, 0, 0, 2, 0x41, 0x42};
    const auto before = normal;
    const auto result = decode_one(normal);
    const auto* ok = std::get_if<Ok>(&result);
    check(ok && ok->consumed == 8 && ok->view.kind == 1 && ok->view.payload.size() == 2,
          "C1/v1 normal shape");
    check(ok->view.payload[0] == 0x41 && ok->view.payload[1] == 0x42 &&
          ok->view.payload.data() == normal.data() + 6, "C1/v1 borrowed bytes");
    const std::array<std::uint8_t, 6> empty{1, 1, 0, 0, 0, 0};
    const auto zero = decode_one(empty);
    check(std::holds_alternative<Ok>(zero) && std::get<Ok>(zero).consumed == 6 &&
          std::get<Ok>(zero).view.payload.empty(), "C1/v2 zero payload");
    need_more({}, "C2/v1 empty input");
    for (std::size_t n = 1; n < 6; ++n) need_more(std::span{normal}.first(n), "C2 short header");
    need_more(std::span{normal}.first(7), "C2/v2 short payload");
    const std::array<std::uint8_t, 6> large{1, 1, 0, 0, 0, 65};
    invalid(large, InvalidReason::Length, "C3/v1 length limit");
    const std::array<std::uint8_t, 6> bad_version{2, 2, 255, 255, 255, 255};
    invalid(bad_version, InvalidReason::Version, "C3/v2 precedence");
    const std::array<std::uint8_t, 6> bad_kind{1, 2, 255, 255, 255, 255};
    invalid(bad_kind, InvalidReason::Kind, "C3/v3 kind precedence");
    const std::array<std::uint8_t, 6> huge{1, 1, 255, 255, 255, 255};
    invalid(huge, InvalidReason::Length, "C3/v4 unsigned shifts");
    const std::array<std::uint8_t, 6> big_endian{1, 1, 0, 0, 1, 0};
    invalid(big_endian, InvalidReason::Length, "C3/v5 big endian 256");
    std::vector<std::uint8_t> tail(normal.begin(), normal.end());
    tail.push_back(0xff);
    check(std::get<Ok>(decode_one(tail)).consumed == 8, "C1/v3 trailing bytes");
    std::array<std::uint8_t, 70> maximum{};
    maximum[0] = 1; maximum[1] = 1; maximum[5] = 64;
    for (std::size_t i = 6; i < maximum.size(); ++i) maximum[i] = static_cast<std::uint8_t>(i - 6);
    const auto max_result = decode_one(maximum);
    const auto& max_ok = std::get<Ok>(max_result);
    check(max_ok.consumed == 70 && max_ok.view.payload.size() == 64 &&
          max_ok.view.payload[63] == 63, "C1/v4 max payload");
    alignas(8) const std::array<std::uint8_t, 9> unaligned{0xff, 1, 1, 0, 0, 0, 2, 0x41, 0x42};
    const auto unaligned_result = decode_one(std::span{unaligned}.subspan(1));
    check(std::get<Ok>(unaligned_result).view.payload[1] == 0x42, "C4/v1 unaligned input");
    std::array<bool, 2> passed{};
    auto run = [&](std::size_t index) {
        bool success = true;
        for (int i = 0; i < 1000; ++i) {
            const auto r = decode_one(normal);
            const auto* value = std::get_if<Ok>(&r);
            success = success && value && value->consumed == 8 && value->view.payload[1] == 0x42;
        }
        passed[index] = success; // distinct objects; read only after both joins
    };
    std::thread a(run, 0), b(run, 1);
    a.join(); b.join();
    check(passed[0] && passed[1] && normal == before, "C4/v2 concurrent immutable input");
    // Do not dereference dangling views to simulate lifecycle testing: that is UB.
    std::cout << "PASS FrameDecoder fixed vectors, unaligned input, concurrent reads\n";
}
