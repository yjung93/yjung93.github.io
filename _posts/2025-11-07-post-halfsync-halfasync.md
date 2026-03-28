---
title: "HalfSync/HalfAsync Pattern"
classes: wide
categories:
  - Design Pattern - ACE Framework
tags:
  - HalfSync/HalfAsync
---

**Table of Contents**
- [Overview](#overview)
- [Half-Sync/Half-Async pattern \[POSA2\]](#half-synchalf-async-pattern-posa2)
  - [Background](#background)
  - [Solution](#solution)
  - [Structure](#structure)
- [Simplified implementation](#simplified-implementation)
  - [class diagram](#class-diagram)
  - [sequence diagram](#sequence-diagram)
- [Example Application using simplified Task framework](#example-application-using-simplified-task-framework)
  - [Server application](#server-application)
    - [Accepror](#accepror)
    - [AsyncService](#asyncservice)
    - [SyncService](#syncservice)
  - [class diagram](#class-diagram-1)
  - [Sequence Diagram](#sequence-diagram-1)
    - [Interoperation between Async and Sync service layer](#interoperation-between-async-and-sync-service-layer)
    - [Life Cycle of Async/Sync Service component](#life-cycle-of-asyncsync-service-component)
  - [Directory and file structure](#directory-and-file-structure)


## Overview

This post covers the following topics:
- The **Half-Sync/Half-Async pattern**  for decoupling asynchronous operations from synchronous processing.
- A **simplified** implementation inspired by the [Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html). The source code is available at [https://github.com/yjung93/study_ACE_design_pattern](https://github.com/yjung93/study_ACE_design_pattern)

## Half-Sync/Half-Async pattern [[POSA2](/references/post-references)]

The **Half-Sync/Half-Async pattern** simplifies programming in concurrent systems by decoupling asynchronous and synchronous service processing without reducing performance.

### Background
Concurrent software systems are often designed with a mixture of synchronous and asynchronous processing services.
- An asynchronous-processing-based design is efficient for handling time-critical events such as hardware interrupts or software signal events. 
- A synchronous-processing-based design, in contrast, simplifies the programming effort.

To achieve both programming simplicity and high performance, we need to combine these two approaches in the software architecture.

### Solution
Decompose the system into two layers, a synchronous service layer and an asynchronous service layer, each running in a different thread. Add a message-queue layer between them so that the two layers communicate via the queue.

- The asynchronous service layer acts as a time-critical, low-level layer. It wakes up on events such as hardware interrupts or software signals from the underlying system and forwards the corresponding messages to the synchronous service layer via the message queue.
- The synchronous service layer implements higher-level, long-duration application services such as database queries or file reading/writing on a separate, independent thread.   

### Structure
This pattern is organized into three layers:

+ **Asynchronous (or reactive) service layer**
+ **Synchronous service layer**
+ **Message-queue layer between async and sync layers**

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/halfsync_halfasync_structure.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/halfsync_halfasync_structure.svg" alt="Reactor PlantUML Diagram" width="70%">


## Simplified implementation

The design pattern is applied to the **Task Framework** [[SH03](/references/post-references)] of ACE.

The simplified **Task framework** is implemented to better understand how the pattern works and how it fits into a layered design. 

This version keeps the core architectural ideas from ACE while intentionally skipping production-level complexity.

The source code is available at [https://github.com/yjung93/study_ACE_design_pattern](https://github.com/yjung93/study_ACE_design_pattern). 

The framework consists of the following components:
- **Task class**
  - Base class of synchronous services. It embeds a message queue and a worker thread, enabling the concrete class to perform services in the synchronous service layer.  
- **Message Queue**
  - The asynchronous service layer passes messages through this queue to the synchronous service layer.   
- **Worker Thread**
  - The thread on which the synchronous service runs. It wakes up when it receives a message from the asynchronous service layer and performs the synchronous application service.
- **Sync service**
  - Concrete subclass of `Task`. It receives messages from the asynchronous service layer and performs synchronous application services.

### class diagram
<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_halfsync_halfasync_framework_class.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_halfsync_halfasync_framework_class.svg" alt="Reactor PlantUML Diagram" width="60%">

### sequence diagram

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_halfsync_halfasync_framework_sequence.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_halfsync_halfasync_framework_sequence.svg" alt="Reactor PlantUML Diagram" width="100%">


## Example Application using simplified Task framework

### Server application
- Demonstration server that waits for client connections, accepts them, and echoes messages received from clients.
- Consists of `Acceptor` and `AsyncService` running on the main thread, and `SyncService` running on a separate thread.

#### Accepror
- Accepts incoming connections and creates `AsyncService` and `SyncService` objects when a connection is established.
- Registers the `AsyncService` object with the `Reactor` so it can receive callback events when a message arrives from a client.

#### AsyncService
- Receives external events from the `Reactor` and forwards the corresponding messages to `SyncService` via the message queue.

#### SyncService
- Concrete subclass of the `Task` class.
- Processes synchronous services on a separate, independent thread.

### class diagram



<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_halfsync_halfasync_application_class.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_halfsync_halfasync_application_class.svg" alt="Reactor PlantUML Diagram" width="70%">


### Sequence Diagram

#### Interoperation between Async and Sync service layer

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_halfsync_halfasync_application_interoperation_async_sync.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_halfsync_halfasync_application_interoperation_async_sync.svg" alt="Reactor PlantUML Diagram" width="100%">


#### Life Cycle of Async/Sync Service component

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_halfsync_halfasync_application_lifecycle_async_sync.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_halfsync_halfasync_application_lifecycle_async_sync.svg" alt="Reactor PlantUML Diagram" width="100%">


### Directory and file structure
Related source files:

```bash
├── applications
│   ├── example_half-sync_half-async
│   │   ├── Acceptor.cpp
│   │   ├── Acceptor.hpp
│   │   ├── AsyncService.cpp
│   │   ├── AsyncService.hpp
│   │   ├── MainClient.cpp
│   │   ├── MainServer.cpp
│   │   ├── SyncService.cpp
│   │   └── SyncService.hpp
├── framework
│   ├── reactor
│   │   └── 1_0
│   │       ├── EventHandler.cpp
│   │       ├── EventHandler.hpp
│   │       ├── Reactor.cpp
│   │       └── Reactor.hpp
│   └── task
│       └── 1_0
│           ├── Task.cpp
│           └── Task.hpp

```
