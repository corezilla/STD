#include "frame_decoder.h"

namespace ex_isd {
namespace {
constexpr std::size_t header_size = 6;
constexpr std::uint32_t max_payload = 64;
struct Header { std::uint8_t version; std::uint8_t kind; std::uint32_t length; };

// Private helper: input.size() >= 6 is checked by decode_one, not assumed at API boundary.
// Byte reads permit unaligned input. Cast BEFORE shifting to avoid signed int overflow.
Header read_header(std::span<const std::uint8_t> input) noexcept {
    const auto length = (std::uint32_t{input[2]} << 24U)
                      | (std::uint32_t{input[3]} << 16U)
                      | (std::uint32_t{input[4]} << 8U)
                      | std::uint32_t{input[5]};
    return {input[0], input[1], length};
}
} // namespace

DecodeResult decode_one(std::span<const std::uint8_t> input) noexcept {
    if (input.size() < header_size) return NeedMore{};
    const Header header = read_header(input);
    if (header.version != 1) return Invalid{InvalidReason::Version};
    if (header.kind != 1) return Invalid{InvalidReason::Kind};
    if (header.length > max_payload) return Invalid{InvalidReason::Length};
    const auto length = static_cast<std::size_t>(header.length); // now bounded to 0..64
    if (input.size() - header_size < length) return NeedMore{};
    return Ok{{header.kind, input.subspan(header_size, length)}, header_size + length};
}
} // namespace ex_isd
