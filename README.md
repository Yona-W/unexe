# UNexe - Simple Nexe unpacker

Requirements: Python 3.4 or newer

Usage: `python unexe.py <filename>`


___

This is a barebones unpacker for Node.js Windows executables made using Nexe. I wrote it because I needed to reverse engineer a simple piece of malware that had been packed using it.

I have not tested it beyond that, and robustness was not one of my goals. Any changes to Nexe may break this.

As with any analysis tool, running this on an untrusted executable is a security risk. It is possible for an attacker to craft an executable specifically designed to exploit this tool. If you want to do reverse engineering or malware analysis, do that in a VM or a container with no mounted volumes. Make sure to properly review everything this script outputs before agreeing to any prompts. 
