# PALMS

<p align="center">
<img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/RE-PALMS/PALMS/Release/master?label=Client%20Build&logo=Github&style=for-the-badge">
<img alt="GitHub" src="https://img.shields.io/github/license/RE-PALMS/PALMS?style=for-the-badge">
</p>

> PALMS: Precision Accurate Movement System

> LIBS: Laser Induced Breakdown Spectroscopy

PALMS is 5-axis positioning system that optimizes LIBS by replacing human hands with a robotic arm to ensure high standards of data quality, efficiency, replicability, and safety.

# Usage

The PALMS system is split into two parts: the client and the server. The client runs on the user's Windows PC and the server runs on the Raspberry Pi integrated into the robotic system.

## Client

The client is available as a Windows executable. You can retrieve the latest stable version [here](https://github.com/RE-PALMS/PALMS/releases/tag/v0.1.0) and you can find the latest pre-release [here](https://github.com/RE-PALMS/PALMS/releases/latest).

On each release, the Windows executable is available as `palms.exe`. Download it and run it directly. Windows SmartScreen may throw up a warning; if it does click `More info` and then `Run anyway`.

To communicate with the server, the client PC must be plugged into the Raspberry Pi.

## Server
