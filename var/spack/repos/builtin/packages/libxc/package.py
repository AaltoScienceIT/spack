# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxc(AutotoolsPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "http://www.tddft.org/programs/octopus/wiki/index.php/Libxc"
    url      = "http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz"
    git      = "https://gitlab.com/libxc/libxc.git"

    version('4.3.4', tag='4.3.4')
    version('4.3.2', tag='4.3.2')
    version('4.2.3', tag='4.2.3')
    version('3.0.0', tag='3.0.0')
    version('2.2.2', tag='2.2.2')
    version('2.2.1', tag='2.2.1')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def url_for_version(self, version):
        if version < Version('3.0.0'):
            return ("http://www.tddft.org/programs/octopus/"
                    "down.php?file=libxc/libxc-{0}.tar.gz"
                    .format(version))

        return ("http://www.tddft.org/programs/octopus/"
                "down.php?file=libxc/{0}/libxc-{0}.tar.gz"
                .format(version))

    @property
    def libs(self):
        """Libxc can be queried for the following parameters:

        - "static": returns the static library version of libxc
            (by default the shared version is returned)

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        libraries = ['libxc']

        # Libxc installs both shared and static libraries.
        # If a client ask for static explicitly then return
        # the static libraries
        shared = ('static' not in query_parameters)

        # Libxc has a fortran90 interface: give clients the
        # possibility to query for it
        if 'fortran' in query_parameters:
            if self.version < Version('4.0.0'):
                libraries = ['libxcf90'] + libraries
            else:  # starting from version 4 there is also a stable f03 iface
                libraries = ['libxcf90', 'libxcf03'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    def setup_environment(self, spack_env, run_env):
        optflags = '-O2'
        if self.compiler.name == 'intel':
            # Optimizations for the Intel compiler, suggested by CP2K
            #
            # Note that not every lowly login node has advanced CPUs:
            #
            #   $ icc  -xAVX -axCORE-AVX2 -ipo hello.c
            #   $ ./a.out
            #   Please verify that both the operating system and the \
            #   processor support Intel(R) AVX instructions.
            #
            # NB: The same flags are applied in:
            #   - ../libint/package.py
            #
            # Related:
            #   - ../fftw/package.py        variants: simd, fma
            #   - ../c-blosc/package.py     variant:  avx2
            #   - ../r-rcppblaze/package.py AVX* in "info" but not in code?
            #   - ../openblas/package.py    variants: cpu_target!?!
            #   - ../cp2k/package.py
            #
            # Documentation at:
            # https://software.intel.com/en-us/cpp-compiler-18.0-developer-guide-and-reference-ax-qax
            #
            optflags += ' -xSSE4.2 -axAVX,CORE-AVX2 -ipo'
            if which('xiar'):
                spack_env.set('AR', 'xiar')

        spack_env.append_flags('CFLAGS',  optflags)
        spack_env.append_flags('FCFLAGS', optflags)

    def configure_args(self):
        args = ['--enable-shared']
        return args

    def check(self):
        # libxc provides a testsuite, but many tests fail
        # http://www.tddft.org/pipermail/libxc/2013-February/000032.html
        pass
