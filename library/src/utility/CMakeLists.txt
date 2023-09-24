## utility
set(UTILITY_SOURCE
    device_memory.cpp
    host_tensor.cpp
    convolution_parameter.cpp
)

add_library(utility SHARED ${UTILITY_SOURCE})
add_library(composable_kernel::utility ALIAS utility)

target_include_directories(utility PUBLIC
    "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/ck>"
    "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/ck/library/utility>"
)

set_target_properties(utility PROPERTIES VERSION "5.7.0" SOVERSION "5.7.0")

rocm_install(
    TARGETS utility
    EXPORT utilityTargets
)

rocm_install(
    EXPORT utilityTargets
    FILE composable_kernelutilityTargets.cmake
    NAMESPACE composable_kernel::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/composable_kernel
)

clang_tidy_check(utility)
