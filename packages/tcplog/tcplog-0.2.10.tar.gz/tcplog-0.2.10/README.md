TCPlog - Tool to log and analyze TCP flows.
================================================================================
Tool to log and analyze TCP flow internals, such as CWND, RTT, SST, throughput, losses and more.

![TCPlog screenshot](screenshot.png)


Based on
--------------------------------------------------------------------------------
TCPlog is written in Python3 and tested on GNU/Linux 4.{1-18}.

Recommended at least kernel 4.1.

Requires kernel module "tcp_probe" available and loaded
OR python extension "tcpinfo" installed.


Requirements
--------------------------------------------------------------------------------
* python3
* Kernel module "tcp_probe"
* python extension "tcpinfo" (see https://git.scc.kit.edu/CPUnetLOG/TCPinfo/)


Optional dependencies
--------------------------------------------------------------------------------
* python program "TCPlivePLOT" (see https://git.scc.kit.edu/CPUnetLOG/TCPlivePLOT/)


Installation of TCPlog
--------------------------------------------------------------------------------
* system-wide installation:
    * sudo pip3 install .
* local installation (places binary in ~/.local/bin --> check your $PATH):
    * pip3 install --user .
* local installation via PIP:
    * pip3 install --user tcplog

Running TCPlog
--------------------------------------------------------------------------------
* ./tcplog.py OR
* tcplog (after installation)


Kernel module "tcp_probe"
--------------------------------------------------------------------------------
To load module run as root:

> modprobe tcp_probe full=1 port=0 && chmod 444 /proc/net/tcpprobe

Requires at least Kernel 3.19


Python extension "tcpinfo"
--------------------------------------------------------------------------------
To install module from pip run:

> pip3 install tcpinfo

Requires at least Kernel 4.1


Misc/FAQ
--------------------------------------------------------------------------------
* use "--help" for all available parameters
* use "--gui-help" for information about curses-gui
* For curses-gui environment variable "term" needs to be set - try:
    > export TERM="xterm-256color"

