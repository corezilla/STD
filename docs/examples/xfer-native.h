/* EX-XFER/v1, revision 1. Fictional logical wire layout, not a device driver. */
#ifndef STD_EX_XFER_NATIVE_H
#define STD_EX_XFER_NATIVE_H
#include <stddef.h>
#include <stdint.h>
#define XFER_VERSION "EX-XFER/v1"
#define XFER_REVISION 1
#define XFER_MAX_BYTES 4096u
/* Wire is little-endian. Do not memcpy a native big-endian host struct. */
struct xfer_desc_v1 {
    uint64_t input_addr;
    uint64_t output_addr;
    uint64_t request_id;
    uint32_t length;
    uint32_t epoch;
};
struct xfer_complete_v1 {
    uint64_t request_id;
    uint32_t epoch;
    uint32_t status; /* 0 OK, 1 DEVICE_ERROR */
    uint32_t bytes_done;
    uint32_t reserved; /* must be zero */
};
_Static_assert(sizeof(struct xfer_desc_v1) == 32, "descriptor size");
_Static_assert(offsetof(struct xfer_desc_v1, input_addr) == 0, "input offset");
_Static_assert(offsetof(struct xfer_desc_v1, output_addr) == 8, "output offset");
_Static_assert(offsetof(struct xfer_desc_v1, request_id) == 16, "request offset");
_Static_assert(offsetof(struct xfer_desc_v1, length) == 24, "length offset");
_Static_assert(offsetof(struct xfer_desc_v1, epoch) == 28, "epoch offset");
_Static_assert(sizeof(struct xfer_complete_v1) == 24, "completion size");
_Static_assert(offsetof(struct xfer_complete_v1, request_id) == 0, "request offset");
_Static_assert(offsetof(struct xfer_complete_v1, epoch) == 8, "epoch offset");
_Static_assert(offsetof(struct xfer_complete_v1, status) == 12, "status offset");
_Static_assert(offsetof(struct xfer_complete_v1, bytes_done) == 16, "bytes offset");
_Static_assert(offsetof(struct xfer_complete_v1, reserved) == 20, "reserved offset");
#endif
