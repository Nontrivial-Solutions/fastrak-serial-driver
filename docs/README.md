---
title: Polhemus Fastrak Serial Driver
authors:
  - joe_starr
---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![White Logo image](https://brainmade.org/white-logo.svg){width=10%}](https://brainmade.org)

![hero](./infra/assets/logo.svg){width=40%}

/// caption

///

## Note to Reader

### What Am I?

This repository contains an opinionated python serial driver for the
[Polhemus Fastrak](https://polhemus.com/all-trackers/fastrak).

### About the Documentation

The following document describes the "rules" and expectation for development. The
["Code Comments"](./content/code/) page contains the technical context descriptions found in the
source files. The ["Use Cases"](./content/use_cases/) page contains a collection of use cases and a
use case diagram for the tool. The ["Decisions"](./content/madr/) page contains a collection of
[architectural decision records](https://adr.github.io/madr/) [@Kopp2018] giving context on why this
tool is the way it is.

### Issues

If you discover an issue with this repository or have a question, please feel free to open an issue.
I've included templates for the following issues:

- 🖋️ Spelling and Grammar: Found some language that is incorrect?
- 🤷 Clarity: Found a section that just makes no sense?
- ❓ Question: Do you have a general question?
- 🐞 Bug: Found an error in the code?
- 🚀 Enhancement: Have a suggestion for improving the toolchain?

[:fontawesome-solid-paper-plane: Open Issue!](https://github.com/Nontrivial-Solutions/psychopy-6dof/issues/new/choose){ .md-button }

## 📃 Cite Me

## ⚖️ License

Documentation:
[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)

Code:
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Planning and Administration

### Tasks

Tasks are tracked as GitHub issues.

### Version Control

The toolchain shall be kept under Git versioning. Development shall take place on branches with
`main` on GitHub as a source of truth. GitHub pull requests shall serve as the arbiter for inclusion
on main with the following quality gates:

- Running and passing the unit test suite.
- Running and passing linting and style enforcers.
- Successful generation of documentation.

#### Release Tagging

The project shall be tagged when a new feature or bug fix is merged into main. The tag shall follow
[semantic versioning](https://semver.org) for labels.

```text
vMAJOR.MINOR.PATCH
```

### Project Structure

Files and directories shall be lower case, where capital is not required by a tool, and contain no
`' '`.

```text


```

### Directories of Interest

- Docs: This directory contains the high level documentation for the tool.

### Define a Unit

A unit shall be a Python module.

### Quality

The tool and its units shall fail-safe, that is the tool and its units can fail, but the failure
must be detectable. A segfault is okay, an off by one error that computes the wrong value is not.

#### Unit Testing

Each internal unit shall have a unit test suite.

#### Integration Testing

The plugin shall have manual integration testing.

### Requirements

#### Functional Requirements

> [!requirement-card] "Psychopy Support"
>
> The tool shall be compliant with the Psychopy plugin interface.

> [!requirement-card] "System Support"
>
> The tool shall support Windows as a primary target. The tool shall design for OSX with minimal
> testing and support.

##### Use Cases  

Nonfunctional requirements are described as a collection of [use cases](./content/usecase/usecase/)
and [actors](./content/usecase/actors/) which are collected into the following use case diagram:

```mermaid
flowchart LR
  aU["👤 Trial Runner"]
  aP["👤 Psychopy"]
  aDD["👤 Device Failure"]

  SR(["Start Recording"])
  HEF(["Handle Failure"])

  subgraph Commands 
      CRS(["Command Recording Start"])
      CRSto(["Command Recording Stop"])
      CDI(["Command Device Init"])
  end

  subgraph Configuration 
      CfFM(["Configure Fail Mode"])
      CfSD(["Configure Serial Device"])
      CfBDT(["Configure Backend Device Type"])
  end

  aU --> SR
  aP --> CfFM
  aP --> CfSD
  aP --> CfBDT
  aDD --> HEF

   SR -. include .-> HEF 

   SR -. include .-> CRS 
   SR -. include .-> CRSto 
   SR -. include .-> CDI 

   CRS -. include .-> HEF 
   CDI -. include .-> HEF 
```

##### Architectural Decisions

Architectural decisions [MADR](<https://github.com/adr/madr>) [@Kopp2018] serve as the primary
documentation for architectural decisions.

The following is the order of operations for the proposal of a MADR:

1. Create a branch for a proposal with the name:

    ```text
    proposal-{{short title}}
    ```

2. Create a pull request with this template.
3. In the branch create a Markdown file based on the
    [MADR Template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md). Name the
    Markdown file:

    ```text
    {{issue# padded to five digits}}-{{title}}
    ```

4. When a decision is made change the status to:
    - "accepted" and pull the branch into main branch
    - "rejected" and pull the branch into main branch

#### Nonfunctional Requirements

##### Colors

Diagrams included in documentation for features (use case and unit descriptions) are expected to use
the [COLORS](https://clrs.cc) color palette.

##### Technologies

###### Languages and Frameworks

- git
- Python
- mermaid.js
- prek
- tombi
- rumdl
- ruff
- uv
- MADR[@Kopp2018]

###### Documentation of Implementation

###### Code Style Guide

Python code shall be formatted with ruff using the included style settings. Markdown files shall be
formatted with ruff using the included style settings. TOML files shall be formatted with tombi
using the included style settings.

## Design and Documentation

### System

#### Block Diagram

```mermaid
flowchart LR
    sdofc["6DOF Component"]
    bsdofd["Base 6DOF Device"]
    sdofbd["6DOF Backend Device"]
    sdofd["6DOF Device"]
    sdofrd["6DOF Response Device"]
    tsdofd@{ shape: processes, label: "{{Typed}}<br>6DOF Device" }
    external["{{External Typed}}<br>Device Module"]

    sdofbd --> sdofc
    sdofd --> sdofbd
    tsdofd  --> sdofd
    bsdofd --> tsdofd 
    sdofrd --> tsdofd 
    external --> tsdofd
```

#### Class Diagram

```mermaid
classDiagram
    Sdofcomponent--|> BaseDeviceComponent
    Sdofcomponent -- SdofDeviceBackend 
    Sdofcomponent -- Sdof 
    SdofDeviceBackend -- Sdof 

    FastrakSdofDevice--o SdofDevice 
    SdofDevice  --o SdofDeviceBackend
    SdofResponse--o SdofDevice 

    SdofResponse--|>BaseResponse
    FastrakSdofDevice --|> BaseSdofDevice
    SdofDeviceBackend--|> DeviceBackend
    BaseSdofDevice--|>BaseDevice 


    class Sdofcomponent{
        + __init__()
        + writePreCode(buff)
        + writeStartCode(buff)
        + writeRunOnceInitCode(buff)
        + writeInitCode(buff)
        + writeFrameCode(buff)
        + writeRoutineEndCode(buff)
        + writeExperimentEndCode(buff)
    }

    class SdofDeviceBackend{
        + __init__()
        + writeDeviceCode(buff)
    }

    class SdofDevice{
        + __new__(**)
        + resolveBackend(cls)
        + getBackends(cls)
        + getAvailableDevices()
        }
    class SdofResponse{}

    class BaseSdofDevice{
        + __init__(**)
        + addListener(listener,startLoop)
        + clearListeners()
        + dispatchMessages( clear)
        + open()
        + close()
        + stop()
        + start()
        + poll()
        + bind()
        + unbind()
        + unbindAll()
        + getTime()
        + bool isOpen
        + bool isStarted
        + list[object] clients 
        + int clientCount
        + bool canClose 
        + float time 
        }

    class Sdof{
        + __init__(**)
        + addListener(listener,startLoop)
        + clearListeners()
        + dispatchMessages( clear)
        + open()
        + close()
        + stop()
        + start()
        + poll()
        + bind()
        + unbind()
        + unbindAll()
        + getTime()
        + bool isOpen
        + bool isStarted
        + list[object] clients 
        + int clientCount
        + bool canClose 
        + float time 
        }

    class FastrakSdofDevice{}


    class BaseDeviceComponent{<<interface>>}
    class DeviceBackend{<<interface>>}
    class BaseResponse{<<interface>>}
    class BaseDevice{<<interface>>}


```

#### Unit Designs

Unit designs for the following components is restricted to the requirements of a PsychoPy plugin and
omitted. From [ADR 00005](./content/madr/00005_plugin_architecture.md) we further restrict the
design to that of the built-in PsychoPy microphone component.

- SdofDevice
- Sdofcomponent
- SdofResponse
- SdofDeviceBackend
- BaseSdofDevice

##### Fastrak 6DOF Device
