# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Half(Package):
    """This is a C++ header-only library to provide an IEEE-754 conformant
    half-precision floating point type along with corresponding
    arithmetic operators, type conversions and common mathematical
    functions. It aims for both efficiency and ease of use, trying to
    accurately mimic the behaviour of the builtin floating point types
    at the best performance possible. It automatically uses and
    provides C++11 features when possible, but stays completely
    C++98-compatible when neccessary."""

    homepage = "https://sourceforge.net/projects/half/"
    url      = "https://downloads.sourceforge.net/project/half/half/2.1.0/half-2.1.0.zip"

    maintainers = ['bvanessen']

    version('2.1.0', sha256='ad1788afe0300fa2b02b0d1df128d857f021f92ccf7c8bddd07812685fa07a25')

    patch('f16fix.patch')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree('include', prefix.include)