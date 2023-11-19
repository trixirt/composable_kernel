%global upstreamname composable_kernel
%global rocm_release 5.7
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

# runs out of memory linking
%global _smp_mflags -j4

%global toolchain rocm

# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

# $gpu will be evaluated in the loops below             
%global _vpath_builddir %{_vendor}-%{_target_os}-build-${gpu}

# No debug info
%global debug_package %{nil}

# Some holes in support, see ck.h CK_BUFFER_RESOURCE_3RD_DWORD
# Missing most of the gfx10XX and some of the gfx9xx
# Not bothering with gfx8 is neither 9 or 10 are used
%global ck_gpu_list gfx11

# For testing
# hardcoded use of gtest and dirs is not suitable for mock building
%bcond_with test


Name:           composable_kernel
Version:        %{rocm_version}
Release:        1%{?dist}
Summary:        Performance Portable Programming Model for Machine Learning Tensor Operators
Url:            https://github.com/ROCmSoftwarePlatform
License:        MIT

Source0:        %{url}/%{upstreamname}/archive/refs/tags/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
Patch0:         0001-Prepare-composable_kernel-cmake-for-fedora.patch
%if %{with test}
Patch1:         0001-Reenable-testing-for-ck.patch
%endif

BuildRequires:  cmake
BuildRequires:  clang-devel
BuildRequires:  compiler-rt
BuildRequires:  lld
BuildRequires:  llvm-devel
BuildRequires:  ninja-build
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules

Requires:       rocm-rpm-macros-modules

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
Composable Kernel (CK) library aims to provide a programming
model for writing performance critical kernels for machine
learning workloads across multiple architectures including
GPUs, CPUs, etc, through general purpose kernel languages,
like HIP C++.

CK utilizes two concepts to achieve performance portability
and code maintainability:

- A tile-based programming model
- Algorithm complexity reduction for complex ML operators,
  using innovative technique we call "Tensor Coordinate
  Transformation".

%package devel
Summary: Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif


%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build
for gpu in %{ck_gpu_list}
do
    module load rocm/$gpu
    %cmake %rocm_cmake_options \
           -DCMAKE_CXX_FLAGS="-mcmodel=medium" \

    %cmake_build
%if %{with test}
    %cmake_build --target tests
%endif
    module purge
done

%install
for gpu in %{ck_gpu_list}
do
    %cmake_install
done

%if %{with test}
cp %{_vpath_builddir}/lib/libgtest* %{buildroot}%{_libdir}/rocm/gfx11/lib/
%endif

# libs need to be stripped
strip %{buildroot}%{_libdir}/rocm/gfx11/lib/libdevice_operations.so.*
strip %{buildroot}%{_libdir}/rocm/gfx11/lib/libutility.so.*

%files 
%license LICENSE
%{_libdir}/rocm/gfx11/lib/libdevice_operations.so.*
%{_libdir}/rocm/gfx11/lib/libutility.so.*

%exclude %{_docdir}/composablekernel/LICENSE

%files devel

%dir %{_includedir}/ck
%dir %{_includedir}/ck/host_utility
%dir %{_includedir}/ck/problem_transform
%dir %{_includedir}/ck/tensor
%dir %{_includedir}/ck/tensor_description
%dir %{_includedir}/ck/tensor_operation
%dir %{_includedir}/ck/tensor_operation/gpu
%dir %{_includedir}/ck/tensor_operation/gpu/block
%dir %{_includedir}/ck/tensor_operation/gpu/device
%dir %{_includedir}/ck/tensor_operation/gpu/device/impl
%dir %{_includedir}/ck/tensor_operation/gpu/element
%dir %{_includedir}/ck/tensor_operation/gpu/grid
%dir %{_includedir}/ck/tensor_operation/gpu/grid/batchnorm_multiblock
%dir %{_includedir}/ck/tensor_operation/gpu/grid/gemm_layernorm
%dir %{_includedir}/ck/tensor_operation/gpu/thread
%dir %{_includedir}/ck/tensor_operation/gpu/warp
%dir %{_includedir}/ck/tensor_operation/operator_transform
%dir %{_includedir}/ck/utility
%dir %{_includedir}/ck/library
%dir %{_includedir}/ck/library/reference_tensor_operation
%dir %{_includedir}/ck/library/reference_tensor_operation/cpu
%dir %{_includedir}/ck/library/reference_tensor_operation/gpu
%dir %{_includedir}/ck/library/tensor_operation_instance
%dir %{_includedir}/ck/library/tensor_operation_instance/gpu
%dir %{_includedir}/ck/library/tensor_operation_instance/gpu/quantization
%dir %{_includedir}/ck/library/tensor_operation_instance/gpu/reduce
%dir %{_includedir}/ck/library/tensor_operation_instance/gpu/softmax
%dir %{_includedir}/ck/library/utility

%dir %{_libdir}/rocm/gfx11/lib/cmake/%{name}

%doc README.md

%{_includedir}/ck/*.hpp
%{_includedir}/ck/host_utility/*.hpp
%{_includedir}/ck/problem_transform/*.hpp
%{_includedir}/ck/library/reference_tensor_operation/cpu/*.hpp
%{_includedir}/ck/library/reference_tensor_operation/gpu/*.hpp
%{_includedir}/ck/library/tensor_operation_instance/*.hpp
%{_includedir}/ck/library/tensor_operation_instance/gpu/*.hpp
%{_includedir}/ck/library/tensor_operation_instance/gpu/quantization/*.hpp
%{_includedir}/ck/library/tensor_operation_instance/gpu/reduce/*.hpp
%{_includedir}/ck/library/tensor_operation_instance/gpu/softmax/*.hpp
%{_includedir}/ck/library/utility/*.hpp
%{_includedir}/ck/tensor/*.hpp
%{_includedir}/ck/tensor_description/*.hpp
%{_includedir}/ck/tensor_operation/gpu/block/*.hpp
%{_includedir}/ck/tensor_operation/gpu/device/*.hpp
%{_includedir}/ck/tensor_operation/gpu/device/impl/*.hpp
%{_includedir}/ck/tensor_operation/gpu/element/*.hpp
%{_includedir}/ck/tensor_operation/gpu/grid/*.hpp
%{_includedir}/ck/tensor_operation/gpu/grid/batchnorm_multiblock/*.hpp
%{_includedir}/ck/tensor_operation/gpu/grid/gemm_layernorm/*.hpp
%{_includedir}/ck/tensor_operation/gpu/thread/*.hpp
%{_includedir}/ck/tensor_operation/gpu/warp/*.hpp
%{_includedir}/ck/tensor_operation/operator_transform/*.hpp
%{_includedir}/ck/utility/*.hpp

%{_libdir}/rocm/gfx11/lib/cmake/%{name}/*.cmake
%{_libdir}/rocm/gfx11/lib/libdevice_operations.so
%{_libdir}/rocm/gfx11/lib/libutility.so

%if %{with test}
%files test
%{_libdir}/rocm/gfx11/bin/test_*
%{_libdir}/rocm/gfx11/lib/libgtest*
%endif

%changelog
* Sun Nov 19 2023 Tom Rix <trix@redhat.com> - 5.7.1-1
- Initial package
