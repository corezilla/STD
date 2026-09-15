#pragma once

#include <cstddef>
#include <cstdint>
#include <span>
#include <variant>

// EX-ISD/v1 teaching API, not a product ABI or a serialized native layout.
namespace ex_isd {
enum class InvalidReason { Version, Kind, Length };
struct FrameView {
    std::uint8_t kind;
    std::span<const std::uint8_t> payload; // Borrows input storage, including after return.
};
struct Ok { FrameView view; std::size_t consumed; };
struct NeedMore { std::size_t consumed = 0; };
struct Invalid { InvalidReason reason; std::size_t consumed = 0; };
using DecodeResult = std::variant<Ok, NeedMore, Invalid>;

// Input must remain valid and immutable during the call and all returned view use.
// Error alternatives contain no view. No heap allocation, no mutation, no retained state.
[[nodiscard]] DecodeResult decode_one(std::span<const std::uint8_t> input) noexcept;
} // namespace ex_isd
