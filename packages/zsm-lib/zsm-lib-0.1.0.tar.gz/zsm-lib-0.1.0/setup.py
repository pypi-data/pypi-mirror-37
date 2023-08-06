# SPDX-License-Identifier: BSD-2-Clause
import setuptools


setuptools.setup(
    name="zsm-lib",
    version="0.1.0",
    keywords="zfs snapshots freebsd linux",
    description="ZFS Snapshot Manager Library",
    long_description="Please see the project links.",
    project_urls={
        "Documentation": "https://zsm.readthedocs.io/",
        "Source": "https://gitlab.com/thnee/zsm",
    },
    license="BSD-2-Clause",
    author="Mattias Lindvall",
    author_email="mattias.lindvall@gmail.com",
    package_dir={"": "src"},
    packages=["zsm_lib"],
    python_requires=">=3.6",
    install_requires=["sarge~=0.1.4", "pyyaml~=3.12", "marshmallow~=3.0.0b14"],
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
