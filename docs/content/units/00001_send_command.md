---
title: Fastrak Device 
authors:
  - joe_starr
date: 2026-07-13
---

## Description

This unit describes the functionality of the Fastrak Device connection class. The class maintains a
serial connection to a physical Fastrak to which it issues commands.

### Members

#### Data

A `bytearray` of data from a data stream session.

### Interfaces

#### Constructor and Valid Class Function

The constructor method takes in a collection of data:

- Serial port name: A string representing which serial port to use to connect to the Fastrak.  
- Baudrate: A baudrate to use for the serial connection.
- Serial timeout: How long to wait for the serial connection.
- Station ID: The ID of the station (peripheral slot) to use on the Fastrak.
- Run setup flag: Indicates if the constructor should also set up the Fastrak.

##### State Machine

```mermaid
stateDiagram-v2
    state "Initalize members" as im
    state "Run basic setup" as rbs 
    state do_setup <<choice>>
    [*] --> im
    im --> do_setup
    do_setup --> [*]: Setup not requested
    do_setup --> rbs: Setup requested
    rbs --> [*]

```

#### Connect

Attempt to connect the configured serial device.

##### State Machine

```mermaid
stateDiagram-v2
    state "Connect device" as cd 
    state is_connected <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is connected
    is_connected --> cd: Is not connected
    cd --> [*]

```

#### Enable Stream

Enable the streaming of data from a Fastrak device.

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak into continuous mode" as sc
    state "Create polling thread" as cpt 
    state "Set streaming on" as ss 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> [*]: Is streaming 
    is_running --> sc: Is not streaming 
    sc --> cpt
    cpt --> ss 
    ss --> [*]

```

#### Disable Stream

Disable the streaming of data from a Fastrak device.

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak out of continuous mode" as sc
    state "Close polling thread" as cpt 
    state "Set streaming off" as ss 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> sc: Is streaming 
    is_running --> [*]: Is not streaming 
    sc --> cpt
    cpt --> ss 
    ss --> [*]

```

#### Read Line

Request a single data entry from the Fastrak.  

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak to supply a data record" as sc
    state "Get response" as ss 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> sc: Is streaming 
    is_running --> [*]: Is not streaming 
    sc --> ss
    ss --> [*]

```

#### Boresight

Zero the Fastrak.  

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak to unboresight" as cfu 
    state "Command Fastrak to boresight" as sc
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> cfu: Is streaming 
    is_running --> [*]: Is not streaming 
    cfu --> sc
    sc --> [*]

```

#### Basic Setup

Run the basic setup for the Fastrak. This sets an active station and output data format.

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak stations off" as sc
    state "Command Fastrak configured station on" as cfcs
    state "Command Fastrak into binary mode" as cfibm
    state "Command Fastrak output format" as cfof
    state is_connected <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is connected
    is_connected --> sc: Is not connected 
    sc --> cfcs
    cfcs --> cfibm
    cfibm --> cfof
    cfof --> [*]

```

## Unit Test Description

### Constructor

#### Positive Tests

> [!test-card] "Initialized component"
>
> Data is passed to the constructor and stored in the private data.
>
> **Inputs:**
> 
> Each argument and all combinations of optional arguments.
>
> **Expected Output:**
>
> Positive response.

#### Negative Tests

No tests for the constructor.

### Connect

#### Positive Tests

> [!test-card] "Device Connected"
>
> A serial device is already connected to an instance of the class. The connect method is called.
>
> **Inputs:**
>
> An instance of the class with a mocked serial device connected.
>
> **Expected Output:**
>
> No response.
>

> [!test-card] "Device Not Connected"
>
> A serial device is not connected to an instance of the class. The connect method is called.
>
> **Inputs:**
>
> A serial mocked device available.
>
> **Expected Output:**
>
> A device is connected.
>

#### Negative Tests

No tests for the connect method.

### Enable Stream

#### Positive Tests

> [!test-card] "A stream is requested"
>
> A stream is requested to start.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is not already running.
>
> **Expected Output:**
>
> The method returns successfully, and a stream is running.
>

> [!test-card] "A stream is running"
>
> A stream is requested to start, but the device is already streaming.  
>
> **Inputs:**
>
> - The mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> No response is given.
>

#### Negative Tests

> [!test-card] "A device is not connected"
>
> A stream is requested to start, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

### Disable Stream

#### Positive Tests

> [!test-card] "A stream is requested to close"
>
> A stream is requested to stop.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> The method returns successfully, and a stream is closed and marked not running.
>

#### Negative Tests

> [!test-card] "No stream is running"
>
> A stream is requested to stop, but the device is not streaming.  
>
> **Inputs:**
>
> - The mocked serial device is connected.
> - A stream is not running.
>
> **Expected Output:**
>
> A not running exception is raised.
>

### Read Line

#### Positive Tests

> [!test-card] "A single data frame is requested"
>
> A single data frame is requested from the Fastrak.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is not running
>
> **Expected Output:**
>
> The device responds with a data frame.  
>

#### Negative Tests

> [!test-card] "A single data frame is requested"
>
> A single data frame is requested from the Fastrak.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running
>
> **Expected Output:**
>
> The device responds with an exception.  
>

> [!test-card] "A device is not connected"
>
> A data frame is requested, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

### Boresight

#### Positive Tests

> [!test-card] "The boresight of a device is requested"
>
> The device is requested to boresight.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is not running.
>
> **Expected Output:**
>
> No response.  
>

#### Negative Tests

> [!test-card] "The boresight of a device is requested"
>
> The device is requested to boresight.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> An exception is raised.
>

> [!test-card] "A device is not connected"
>
> The device is requested to boresight, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

### Basic Setup

#### Positive Tests

> [!test-card] "Command the device to basic setup state"
>
> The device is commanded into its normal operating state.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
>
> **Expected Output:**
>
> No response.  
>

#### Negative Tests

> [!test-card] "A device is not connected"
>
> The device is commanded into its normal operating state, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

> [!test-card] "Command the device to basic setup state, but stream is running"
>
> The device is commanded into its normal operating state, but a stream is running.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> A streaming exception is raised.
>
