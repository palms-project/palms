<div align="center">

# PALMS

<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/palms-project/palms?label=Github%20Release&logo=Github">
<img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/palms-project/palms/Development%20Release/master?label=Build&logo=Github">
<img alt="GitHub" src="https://img.shields.io/github/license/palms-project/palms?label=License">
<img alt="Python Versions" src="https://img.shields.io/badge/python-3.6+-blue.svg">
<a href="https://results.pre-commit.ci/latest/github/palms-project/palms/master"><img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/palms-project/palms/master.svg"></a>
<a href="https://www.codefactor.io/repository/github/palms-project/palms"><img src="https://www.codefactor.io/repository/github/palms-project/palms/badge" alt="CodeFactor" /></a>

<p align="center">
<a href="#installation">Installation</a> • <a href="#usage">Usage</a> • <a href="#citation">Citation</a>
</p>

</div>

> **PALMS**: Precise Acquisition LIBS Movement Software
>
> **LIBS**: Laser Induced Breakdown Spectroscopy

PALMS is a user-friendly control software for multi-axial LIBS robotic positioning systems.

Such systems optimize LIBS by replacing human hands with robotic equivalents to ensure high standards of data quality, efficiency, replicability, and safety.

The PALMS system is split into two parts: the client and the server. The client runs on the user's Windows PC and the server runs on the Raspberry Pi integrated into the robotic system.

## Installation

### Client

The client is available as a Windows executable. You can retrieve the latest stable version [here](https://github.com/palms-project/palms/releases/latest), and you can find the latest pre-release [here](https://github.com/palms-project/palms/releases/tag/latest).

On each release, the Windows executable is available as `palms.exe` (or `palms-dev.exe` for development releases). Download it and run it directly. Windows SmartScreen may throw up a warning; if it does click `More info` and then `Run anyway`.

### Server

The PALMS server can be installed with the provided install script.

To use it, you must configure it as shown below.

```diff
#### CONFIGURATION ####

- REMOTE_USER="pi"
- REMOTE_HOST="raspi"
+ REMOTE_USER="your user"
+ REMOTE_HOST="your host"

#### END CONFIGURATION ####
```

To run the script:

```shell
git clone https://github.com/palms-project/palms
cd PALMS
./src/server/install.sh
```

## Usage

For the client to communicate with the server, it must have some kind of network connection where it can access the server by the hostname `raspberrypi.local`. Additionally, port 35007 must be open on both the client and the server.

### Client

Double click the `palms.exe` file and the application should open.

### Server

The server runs as a daemon (it automatically starts on boot and runs continuously), so no action should be necessary after it is installed. If it acts strangely, try viewing the logs:

```shell
sudo journalctl -fu palms.service
```

Otherwise, check its status:

```shell
sudo systemctl status palms.service
```

As a last resort, try restarting it:

```shell
sudo systemctl restart palms.service
```

## Citation

View the poster [on ResearchGate](https://www.researchgate.net/publication/361947681_Precise_Acquisition_LIBS_Movement_Software_An_Easily_Usable_Control_Software_for_Robotized_Optomechanical_Systems).
If you use or reference PALMS, please cite the following:

```bibtex
@article{https://doi.org/10.13140/rg.2.2.36324.65926,
    doi = {10.13140/RG.2.2.36324.65926},
    url = {https://rgdoi.net/10.13140/RG.2.2.36324.65926},
    author = {Shaked, Gideon and Vallone, Max and Dubard, Robert and Ochatt, Claudia},
    language = {en},
    title = {Precise Acquisition {LIBS} Movement Software: An Easily Usable Control Software for Robotized Optomechanical Systems},
    publisher = {Unpublished},
    year = {2021}
}
```
