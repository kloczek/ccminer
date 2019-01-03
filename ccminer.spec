%global gittag0 %{version}-tpruvot

%if 0%{?fedora}
# GCC 7.3.1 compiler (Fedora 27), disable:
#   -fcf-protection -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1
%undefine _annotated_build
# Override from /usr/lib/rpm/redhat/rpmrc:
%global optflags %{__global_compiler_flags} -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection
%endif

Name:           ccminer
Version:        2.3
Release:        3%{?dist}
Summary:        CUDA miner project
License:        GPLv2 and GPLv3
URL:            https://github.com/tpruvot/%{name}

Source0:        https://github.com/tpruvot/%{name}/archive/%{gittag0}.tar.gz#/%{name}-%{gittag0}.tar.gz
Patch0:         %{name}-2.3-nvcc-arch.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cuda-devel
BuildRequires:  gcc-c++
BuildRequires:  jansson-devel
BuildRequires:  libcurl-devel >= 7.15.2
BuildRequires:  libstdc++-devel
BuildRequires:  libtool
BuildRequires:  openssl-devel

%if 0%{?fedora}
BuildRequires:  cuda-gcc-c++
%endif

%description
This is a CUDA accelerated mining application which handles:
    Decred (Blake256 14-rounds - 180 bytes)
    HeavyCoin & MjollnirCoin
    FugueCoin
    GroestlCoin & Myriad-Groestl
    Lbry Credits
    JackpotCoin (JHA)
    QuarkCoin family & AnimeCoin
    TalkCoin
    DarkCoin and other X11 coins
    Chaincoin and Flaxscript (C11)
    Saffroncoin blake (256 14-rounds)
    BlakeCoin (256 8-rounds)
    Qubit (Digibyte, ...)
    Luffa (Joincoin)
    Keccak (Maxcoin)
    Pentablake (Blake 512 x5)
    1Coin Triple S
    Neoscrypt (FeatherCoin)
    x11evo (Revolver)
    phi2 (LUXCoin)
    Scrypt and Scrypt:N
    Scrypt-Jane (Chacha)
    sib (Sibcoin)
    Skein (Skein + SHA)
    Signatum (Skein cubehash fugue Streebog)
    SonoA (Sono)
    Tribus (JH, keccak, simd)
    Woodcoin (Double Skein)
    Vanilla (Blake256 8-rounds - double sha256)
    Vertcoin Lyra2RE
    Ziftrcoin (ZR5)
    Boolberry (Wild Keccak)
    Monero (Cryptonight v7 with -a monero)
    Aeon (Cryptonight-lite)

%prep
%autosetup -p1 -n %{name}-%{gittag0}

# Make sure to pick up CUDA headers
# Add -fPIC to backend compiler for NVCC
sed -i \
    -e 's|-I$with_cuda/include|-I$with_cuda/include/cuda|g' \
    -e 's|NVCC="$with_cuda/bin/nvcc"|NVCC="$with_cuda/bin/nvcc -Xcompiler -fPIC"|' \
    configure.ac

%if 0%{?fedora}
# Use compat GCC for building
sed -i -e 's|nvcc -Xcompiler|nvcc -ccbin /usr/bin/cuda-g++ -Xcompiler|g' configure.ac
%endif

%build
autoreconf -vif

%configure --with-cuda=%{_prefix} --with-nvml=%{_libdir}

make
#%make_build

%install
%make_install

%files
%license LICENSE.txt
%doc README.txt
%{_bindir}/ccminer

%changelog
* Thu Jan 03 2019 Simone Caronni <negativo17@gmail.com> - 2.3-3
- Rebuild for CUDA 10.0 update.
- Update GCC build flags for GCC 7.3.1.
- Enable additional CUDA 10 architectures.

* Tue Aug 28 2018 Simone Caronni <negativo17@gmail.com> - 2.3-2
- Update for CUDA 9.2 with GCC 7.x.
- Do not required cuda-gcc in Fedora 27.

* Wed Jul 04 2018 Simone Caronni <negativo17@gmail.com> - 2.3-1
- Update to 2.3.

* Thu Jun 14 2018 Simone Caronni <negativo17@gmail.com> - 2.2.6-1
- Update to 2.2.6, drop Monero V7 patch.

* Wed May 09 2018 Simone Caronni <negativo17@gmail.com> - 2.2.5-2
- Add Monero V7 patch.
- Momentarily disable annobin plugin.
- Remove unsupported compiler flags.

* Mon Apr 23 2018 Simone Caronni <negativo17@gmail.com> - 2.2.5-1
- Update to 2.2.5.

* Mon Jan 15 2018 Simone Caronni <negativo17@gmail.com> - 2.2.4-1
- Update to 2.2.4.

* Thu Dec 14 2017 Simone Caronni <negativo17@gmail.com> - 2.2.3-1
- Update to 2.2.3.

* Wed Nov 01 2017 Simone Caronni <negativo17@gmail.com> - 2.2.2-1
- Update to 2.2.2.
- Override compiler with cuda-gcc for CUDA 9 on Fedora.
- Disable Compute architecture 2.x for CUDA 9.

* Sun Sep 10 2017 Simone Caronni <negativo17@gmail.com> - 2.2.1-1
- Update to 2.2.1.

* Mon Jul 24 2017 Simone Caronni <negativo17@gmail.com> - 2.1-1
- Update to 2.1.

* Tue May 30 2017 Simone Caronni <negativo17@gmail.com> - 2.0-2
- Update to 2.0 final.

* Fri Apr 28 2017 Simone Caronni <negativo17@gmail.com> - 2.0-1
- Update to latest release.
- Use GCC 5.3 on Fedora.

* Sun Nov 15 2015 Simone Caronni <negativo17@gmail.com> - 1.7.0-1
- Update to 1.7.0.

* Thu Oct 01 2015 Simone Caronni <negativo17@gmail.com> - 1.6.6-1
- Update to 1.6.6; rebuilt with CUDA 7.5.

* Wed Jul 29 2015 Simone Caronni <negativo17@gmail.com> - 1.6.5-1.C11
- Update to 1.6.5-C11.
- Switch to updated packaging guidelines for Github.

* Sat Apr 11 2015 Simone Caronni <negativo17@gmail.com> - 1.6.0-1.git.4426700
- Update to 1.6.0.

* Tue Jan 20 2015 Simone Caronni <negativo17@gmail.com> - 1.5.1-1.git.9adb7d7
- Update to 1.5.1.

* Wed Dec 10 2014 Simone Caronni <negativo17@gmail.com> - 1.5.0-1.git.70743eb
- -Update to latest 1.5.0 snapshot.

* Mon Nov 10 2014 Simone Caronni <negativo17@gmail.com> 1.4.7-1.git.2ab1e37
- First build.
