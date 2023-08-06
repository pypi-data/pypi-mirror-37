#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

# keep in sync with main.py (!)
version = "0.2.10"
desc = "Tool to log and analyze TCP flows."
longdesc = "Tool to log and analyze TCP flow internals, such as CWND, RTT, SSTthresh, throughput, losses and more."

setup(
        name = "tcplog",
        packages = [
            "tcplog",
            "tcplog.utils",
            "tcplog.backends",
            "tcplog.backends.input",
            "tcplog.backends.output",
            "tcplog.backends.gui"
            ],
        entry_points = {
            "console_scripts": [
                'tcplog = tcplog.main:main'
                ],
            },
        version = version,
        description = desc,
        long_description = longdesc,
        author = "Karlsruhe Institute of Technology - Institute of Telematics",
        author_email = "telematics@tm.kit.edu",
        maintainer = "Michael Koenig",
        maintainer_email = "michael.koenig2@student.kit.edu",
        url = "https://git.scc.kit.edu/CPUnetLOG/TCPlog/",
        license = "BSD",
        platforms = "Linux",
        zip_safe = False,
        install_requires = [
            'tcpinfo>=0.2.1'#,
            # 'netifaces>=0.10.4'

        ],
        extras_require = {
            'Live visualization':  ["tcpliveplot>=0.2"]
        },
        keywords = ['tcp', 'flow', 'log', 'analyze', 'network', 'traffic'],
        classifiers = [
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Operating System :: POSIX :: Linux',
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'Natural Language :: English',
            'Intended Audience :: Education',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Science/Research',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Telecommunications Industry',
            'Topic :: Scientific/Engineering',
            'Topic :: Internet',
            'Topic :: System :: Logging',
            'Topic :: System :: Networking',
            'Topic :: System :: Networking :: Monitoring',
            'Topic :: System :: Operating System Kernels :: Linux',
            'Topic :: Utilities'
        ]
        )
