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
- [Simplified Reactor framework implementation](#simplified-reactor-framework-implementation)
  - [Structure](#structure)
  - [Core classes](#core-classes)
    - [Reactor](#reactor)
    - [EventHandler](#eventhandler)
  - [Interaction sequence](#interaction-sequence)
  - [Example: echo server and client](#example-echo-server-and-client)
    - [How it works](#how-it-works)
  - [Directory and file structure](#directory-and-file-structure)

## Overview
The **Reactor pattern** uses a single event loop to demultiplex I/O events and dispatch them to registered handlers. This post is exploring the pattern through a **simplified** implementation inspired by [the Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html), focusing on the essentials rather than production complexity. My goal here is to share what I’ve been studying and building.

## Simplified Reactor framework implementation
I built a small, learning-oriented framework that retains the core ideas from ACE (initiation dispatcher, event demultiplexing, handler registration) while keeping the code minimal. 

The source code is available at my [GitHub repository](https://github.com/yjung93/study_ACE_design_pattern).

### Structure
At a high level:

+ **Reactor** – runs the event loop, waits for events, dispatches to handlers.
+ **EventHandler** – base class; concrete handlers implement the I/O logic.
 
![UML — Reactor, EventHandler, Acceptor/ServerHandler relationships](/assets/images/reactor_class_diagram_v_1_1.jpg)

### Core classes

#### Reactor
- Maintains a registry of active handlers.
- Uses a synchronous demultiplexer (e.g., `select`) to wait for activity.
- Dispatches `handleInput(fd)` on the ready handlers.
- Provides `registerHandler()` and `removeHandler()` to manage the registry and lifetime.

![alt text](/assets/images/reactor_class_diagram.png)

#### EventHandler
- Base interface for application-specific handlers.
- Stores the OS handle/FD and a back-reference to the `Reactor`.
- Overridable `handleInput(fd)` method contains the actual I/O logic for each handler.

![alt text](/assets/images/eventhandler_class_diagram.png)

### Interaction sequence
1. Handlers register themselves (or are registered by an acceptor) with the `Reactor`.
2. The `Reactor` blocks in `select()` and wakes when one or more FDs are ready.
3. For each ready FD, the corresponding handler’s `handleInput(fd)` is invoked.
4. Handlers may read/write, create new handlers (e.g., for new connections), or deregister on close.

![alt text](/assets/images/reactor_Sequence.png)

### Example: echo server and client
For a quick demo, I built a tiny echo server using:
- An **Acceptor**-like handler for passive opens (creates a per-connection handler).
- A **Server handler** that reads data and echoes it back.
- A simple **client** that connects, sends user input, and prints the response.

![alt text](/assets/images/example_reactor.png)

#### How it works
- The Acceptor listens for new client connections. When a connection is established, it creates a ServerEventHandler and registers it with the Reactor.
- The Reactor monitors all registered event handlers using the select() system call and delegates events to their respective handlers.
- The ServerEventHandler processes client messages and echoes them back​

![alt text](/assets/images/example_reactor_Sequence.png)


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