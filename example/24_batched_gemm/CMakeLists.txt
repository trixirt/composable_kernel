add_custom_target(example_batched_gemm_xdl)
add_example_executable(example_batched_gemm_xdl_fp32 batched_gemm_xdl_fp32.cpp)
if(result EQUAL 0)
  add_dependencies(example_batched_gemm_xdl example_batched_gemm_xdl_fp32)
endif()
add_example_executable(example_batched_gemm_xdl_fp16 batched_gemm_xdl_fp16.cpp)
if(result EQUAL 0)
  add_dependencies(example_batched_gemm_xdl example_batched_gemm_xdl_fp16)
endif()
add_example_executable(example_batched_gemm_xdl_bf16 batched_gemm_xdl_bf16.cpp)
if(result EQUAL 0)
  add_dependencies(example_batched_gemm_xdl example_batched_gemm_xdl_bf16)
endif()
add_example_executable(example_batched_gemm_xdl_int8 batched_gemm_xdl_int8.cpp)
if(result EQUAL 0)
  add_dependencies(example_batched_gemm_xdl example_batched_gemm_xdl_int8)
endif()
if(USE_BITINT_EXTENSION_INT4)
  add_example_executable(example_batched_gemm_xdl_int4 batched_gemm_xdl_int4.cpp)
  if(result EQUAL 0)
    add_dependencies(example_batched_gemm_xdl example_batched_gemm_xdl_int4)
  endif()
endif()
