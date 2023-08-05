from __future__ import absolute_import
import pkg_resources
import setuptools
import setuptools.command.build_ext
import setuptools.command.test


__author__ = 'Shashank Shekhar'
__version__ = '0.13'
__email__ = 'shashank.f1@gmail.com'
__download_url__ = 'https://github.com/shkr/routesimilarity/archive/0.1.tar.gz'

try:
    import Cython.Build
    __cython = True
except ImportError:
    __cython = False


class BuildExtension(setuptools.command.build_ext.build_ext):
    def build_extensions(self):
        numpy_includes = pkg_resources.resource_filename("numpy", "core/include")

        for extension in self.extensions:
            if not hasattr(extension, "include_dirs") or \
                    (hasattr(extension, "include_dirs") and numpy_includes not in extension.include_dirs):
                extension.include_dirs.append(numpy_includes)

        setuptools.command.build_ext.build_ext.build_extensions(self)


__extensions = [
    setuptools.Extension(
        name="routesimilarity.directed_hausdorff",
        sources=[
            "routesimilarity/directed_hausdorff.{}".format("pyx" if __cython else "c")
        ],
        extra_compile_args = ["-O3", "-ffast-math", "-march=native"]
    )
]

if __cython:
    __extensions = Cython.Build.cythonize(__extensions)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name='routesimilarity',
  packages=['routesimilarity'],
  version=__version__,
  license='MIT',
  description='Methods for similarity scoring between routes',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author=__author__,
  author_email=__email__,
  url='https://github.com/shkr/routesimilarity',
  download_url=__download_url__,
  keywords=['route', 'similarity', 'hausdorff'],
  install_requires=[
    'geopy',
    'numpy>=1.15'
   ],
  setup_requires=[
    'cython>=0.28',
    'numpy>=1.15'
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3'
  ],
  ext_modules=__extensions,
  cmdclass={"build_ext": BuildExtension}
)
