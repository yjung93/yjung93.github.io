---
title: "Reactor Pattern"
classes: wide
categories:
  - Design Pattern - ACE Framework
tags:
  - Reactor
---

**Table of Contents**
- [Overview](#overview)
- [Reactor Pattern \[POSA2\]](#reactor-pattern-posa2)
  - [Background](#background)
  - [Solution](#solution)
  - [Structure](#structure)
    - [Class Diagram](#class-diagram)
    - [Dynamic](#dynamic)
- [Simplified Reactor framework implementation](#simplified-reactor-framework-implementation)
  - [Structure](#structure-1)
  - [Core classes](#core-classes)
    - [Reactor](#reactor)
    - [EventHandler](#eventhandler)
  - [Interaction sequence](#interaction-sequence)
  - [Example: echo server and client](#example-echo-server-and-client)
    - [How it works](#how-it-works)
  - [Directory and file structure](#directory-and-file-structure)

## Overview
This post covers the following topics:
- The **Reactor pattern**  using a single event loop to demultiplex I/O events and dispatch them to registered handlers.
- A **simplified** implementation inspired by the [Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html), focusing on the essentials rather than production complexity. The source code is available at [https://github.com/yjung93/study_ACE_design_pattern](https://github.com/yjung93/study_ACE_design_pattern)


## Reactor Pattern [[POSA2](/references/post-references)]
The Reactor pattern is a design pattern for handling service requests delivered concurrently to an application by one or more clients. It efficiently demultiplexes and dispatches events to the appropriate handlers. It provides the following benefits:

- **Efficiency**: Handles multiple events using a single thread, reducing overhead.
- **Scalability**: Suitable for systems with many simultaneous connections.
- **Maintainability**: Promotes modular and decoupled code design.

### Background
Event-driven applications in distributed systems, even if originally designed to process service requests synchronously and serially, must often process multiple service requests simultaneously. The multiple concurrent events must be demultiplexed and dispatched to the appropriate application service handlers.

The following forces must be resolved to address this problem:
- To improve scalability and latency, the application should not block the thread when an event is triggered or exclude events from other sources.
- To maximize throughput, context switching, unnecessary synchronization, and data movement among CPUs should be avoided.
- Adding and improving services within the existing event demultiplexing and dispatching system should require minimal effort.
- The application's implementation should be decoupled from the complexities of multi-threading and synchronization.

### Solution

- Synchronously wait for events from different sources.
- Apply a mechanism that demultiplexes and dispatches events to the application services that process them.
- Decouple the demultiplexing and dispatching mechanisms from the application service implementation.

In Detail:
- An application implements a separate event handler for each service. 
- Event handlers are registered with the Reactor.
- The Reactor uses a synchronous event demultiplexer to wait for an indication that an event has occurred.
- The event demultiplexer notifies the Reactor when these events occur.
- The Reactor dispatches the event to the associated registered event handler.
- The event handler performs its application service.

### Structure
- **Handles**: Identify event sources such as network connections or open files. These are provided by the operating system.
- **Synchronous event demultiplexer**: A function that waits for the occurrence of one or more events. Calling this function blocks the thread until an event occurs. The `select()` system call is a common synchronous event demultiplexer for I/O events, supported by many operating systems.
- **Event handler**: Specifies an interface composed of one or more hook methods. These methods represent a set of operations that can be used to process application-specific events.
- **Concrete event handlers**: Specialize the event handler and implement the application's services.
- **Reactor**: Provides an interface for applications to register or unregister their event handlers and associated handles. It runs the application's event loop and waits for event indications on the associated handles using a synchronous demultiplexer. When an event occurs, it dispatches the event to the corresponding event handler registered by the application.

#### Class Diagram
<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/reactor_design_pattern_class_diagram.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/reactor_design_pattern_class_diagram.svg" alt="Reactor PlantUML Diagram" width="80%">
 
#### Dynamic
<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/reactor_design_pattern_sequence.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/reactor_design_pattern_sequence.svg" alt="Reactor PlantUML Diagram" width="100%">

## Simplified Reactor framework implementation
I built a small, learning-oriented framework that retains the core ideas from ACE (initiation dispatcher, event demultiplexing, handler registration) while keeping the code minimal. 

The source code is available at [https://github.com/yjung93/study_ACE_design_pattern](https://github.com/yjung93/study_ACE_design_pattern)


### Structure
At a high level:

+ **Reactor** – runs the event loop, waits for events, dispatches to handlers.
+ **EventHandler** – base class; concrete handlers implement the I/O logic.
 

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/reactor_class_diagram_v_1_2.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/reactor_class_diagram_v_1_2.svg" alt="Reactor PlantUML Diagram" width="60%">


### Core classes

#### Reactor
- Maintains a registry of active handlers.
- Uses a synchronous demultiplexer (e.g., `select`) to wait for activity.
- Dispatches `handleInput(fd)` on the ready handlers.
- Provides `registerHandler()` and `removeHandler()` to manage the registry and lifetime.


#### EventHandler
- Base interface for application-specific handlers.
- Stores the OS handle/FD and a back-reference to the `Reactor`.
- Overridable `handleInput(fd)` method contains the actual I/O logic for each handler.


### Interaction sequence
1. Handlers register themselves (or are registered by an acceptor) with the `Reactor`.
2. The `Reactor` blocks in `select()` and wakes when one or more FDs are ready.
3. For each ready FD, the corresponding handler’s `handleInput(fd)` is invoked.
4. Handlers may read/write, create new handlers (e.g., for new connections), or deregister on close.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/reactor_Sequence.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/reactor_Sequence.svg" alt="Reactor Sequence Diagram" width="80%">

### Example: echo server and client
For a quick demo, I built a tiny echo server using:
- An **Acceptor**-like handler for passive opens (creates a per-connection handler).
- A **Server handler** that reads data and echoes it back.
- A simple **client** that connects, sends user input, and prints the response.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_reactor.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_reactor.svg" alt="Example Reactor Diagram" width="60%">

#### How it works
- The Acceptor listens for new client connections. When a connection is established, it creates a ServerEventHandler and registers it with the Reactor.
- The Reactor monitors all registered event handlers using the select() system call and delegates events to their respective handlers.
- The ServerEventHandler processes client messages and echoes them back.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_reactor_Sequence.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_reactor_Sequence.svg" alt="Example Reactor Sequence Diagram" width="90%">

This shows how the Reactor’s single event loop can manage multiple connections cleanly, while each handler stays focused on its own responsibility.

### Directory and file structure
Related source files for the Reactor demo:

```bash
├── applications
│   ├── example_reactor
│   │   ├── MainClient.cpp
│   │   ├── MainServer.cpp
│   │   ├── ServerEventHandler.cpp
│   │   ├── ServerEventHandler.hpp
│   │   └── Acceptor.cpp / Acceptor.hpp     # minimal acceptor used by the server
├── framework
│   └── v_1_0
│       ├── Reactor.cpp
│       ├── Reactor.hpp
│       ├── EventHandler.cpp
│       └── EventHandler.hpp
```