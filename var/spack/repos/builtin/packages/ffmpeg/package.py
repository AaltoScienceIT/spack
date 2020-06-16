# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ffmpeg(AutotoolsPackage):
    """FFmpeg is a complete, cross-platform solution to record,
    convert and stream audio and video."""

    homepage = "https://ffmpeg.org"
    url      = "http://ffmpeg.org/releases/ffmpeg-4.1.1.tar.bz2"

    version('4.3', sha256='a7e87112fc49ad5b59e26726e3a7cae0ffae511cba5376c579ba3cb04483d6e2')
    version('4.1.1',   '4a64e3cb3915a3bf71b8b60795904800')
    version('4.1',   'b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5')
    version('3.2.4', 'd3ebaacfa36c6e8145373785824265b4')

    variant('shared', default=True,
            description='build shared libraries')

    variant('aom', default=False,
            description='build Alliance for Open Media libraries')
    variant('x264', default=False,
            description='Build with libx264 support')

    depends_on('yasm@1.2.0:')
    depends_on('aom', when='+aom')
    depends_on('libx264', when='+x264')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        if '+shared' in spec:
            config_args.append('--enable-shared')

        if '+aom' in spec:
            config_args.append('--enable-libaom')
        else:
            config_args.append('--disable-libaom')

        if '+x264' in spec:
            config_args += ['--enable-gpl', '--enable-libx264']

        return config_args
