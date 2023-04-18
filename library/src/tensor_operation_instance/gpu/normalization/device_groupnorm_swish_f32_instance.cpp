// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2022, Advanced Micro Devices, Inc. All rights reserved.

#include "normalization_instance_common.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

using Swish = ck::tensor_operation::element_wise::Swish;

void add_device_normalization_rank_5_3_swish_f32_instances(
    std::vector<std::unique_ptr<DeviceNormalization<F32, F32, F32, F32, F32, Swish, 5, 3>>>&
        instances)
{
    add_device_operation_instances(instances, device_normalization_f32_instances<Swish, 5, 3>{});
}

} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck