---
title: "Acceptor-Connector Pattern"
classes: wide
categories:
  - Design Pattern - ACE Framework
tags:
  - Acceptor Connector
---

**Table of Contents**
- [Overview](#overview)
- [Simplified Acceptor-Connector framework implementation](#simplified-acceptor-connector-framework-implementation)
  - [Structure](#structure)
  - [Event infrastructure layer classes](#event-infrastructure-layer-classes)
  - [Connection management layer classes](#connection-management-layer-classes)
    - [ServiceHandler](#servicehandler)
    - [Acceptor](#acceptor)
    - [Connector](#connector)
  - [Application layer classes](#application-layer-classes)
    - [Server application](#server-application)
      - [AcceptorImpl](#acceptorimpl)
      - [InputHandler](#inputhandler)
    - [Client application](#client-application)
      - [Client](#client)
      - [ConnectorImpl](#connectorimpl)
      - [OutputHandler](#outputhandler)
      - [Dynamics](#dynamics)
  - [Directory and file structure](#directory-and-file-structure)


## Overview
This post introduces the **Acceptor-Connector pattern** [[POSA2](/references/post-references)], which **decouples connection establishment and initialization** from the components that perform application logic after a connection is established. I’m exploring this pattern through a **simplified** implementation inspired by the [Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html).  
My goal here is to share what I've learned through a simplified implementation.

## Simplified Acceptor-Connector framework implementation
I built a small, learning-oriented Acceptor-Connector framework to understand how the pattern works and how it fits into a layered design. 

This version keeps the core architectural ideas from ACE while intentionally skipping production-level complexity.

The source code is available at my [GitHub repository](https://github.com/yjung93/study_ACE_design_pattern).  

### Structure
The implementation is organized into three layers:

+ **Event infrastructure layer classes**
+ **Connection management layer classes**
+ **Application layer classes**

The relationships between classes in this framework are shown below.  
![Class diagram — Acceptor-Connector framework (v1.1)](/assets/images/acceptor_connector_class_diagram_v_1_1.png)

### Event infrastructure layer classes
This simplified framework is built on top of a **Reactor** framework that provides event demultiplexing and dispatching. For details, see the previous post: [Reactor Pattern](/design%20pattern%20-%20ace%20framework/post-reactor/).

### Connection management layer classes
This layer provides **generic, application-independent** connection and initialization services. It consists of:

+ **ServiceHandler**
+ **Acceptor**
+ **Connector**

#### ServiceHandler
+ Defines the interfaces needed by an application service implementation.
+ Concrete services typically act as a client, a server, or both in a peer-to-peer system.
+ Created by an **Acceptor** or **Connector** when a connection is established.
+ Provides a hook that the Acceptor/Connector calls to activate the service once the connection is ready.
+ Exposes a **transport endpoint** used by the application service to communicate with its peer. The endpoint type is parameterized (template) so the OS-specific I/O implementation stays separate from application logic.

![Class diagram — ServiceHandler](/assets/images/service_handler_class_diagram.png)

#### Acceptor
+ **Passively** establishes a connected transport endpoint.
+ Creates and initializes the associated **ServiceHandler** when a connection is accepted.
+ Decouples acceptance/initialization from the ServiceHandler that runs application logic.

![Class diagram — Acceptor](/assets/images/acceptor_class_diagram.png)

**Interaction sequence**  
![Sequence — connection acceptance via Acceptor](/assets/images/acceptor_connection_acceptance_equence.png)

#### Connector
+ **Actively** establishes a connected transport endpoint.
+ Creates and initializes the associated **ServiceHandler** when the connection completes.
+ Decouples initiation/initialization from the ServiceHandler that runs application logic.
+ Supports **synchronous** and **asynchronous** connection.

![Class diagram — Connector](/assets/images/connector_class_diagram.png)

**Interaction sequence (synchronous)**  
![Sequence — synchronous connect with Connector](/assets/images/connector_synchronous_Sequence.png)

**Interaction sequence (asynchronous)**  
![Sequence — asynchronous connect with Connector](/assets/images/connector_asynchronous_Sequence.png)

### Application layer classes
This layer customizes the generic strategies from the infrastructure and connection layers (via subclassing, composition, and/or template instantiation) to create concrete components that establish connections, exchange data, and implement service behavior.

#### Server application
Demonstration server: waits for client connections, accepts them, and echoes messages received from clients.

![Component diagram — example server (Acceptor-Connector)](/assets/images/example_acceptor_connector_server_diagram.png)

##### AcceptorImpl
- Concrete subclass of **Acceptor**.
- Plays the acceptor role by deriving from the Acceptor class.

##### InputHandler
- Concrete subclass of **ServiceHandler**.
- Handles client I/O and echoes back received messages.

#### Client application
Demonstration client: sends user-typed messages to the server and displays the responses.

![Component diagram — example client (Acceptor-Connector)](/assets/images/example_acceptor_connector_client_diagram.png)

##### Client
- A **facade** that composes a **Connector** and a **ServiceHandler**.

##### ConnectorImpl
- Concrete subclass of **Connector**.
- Plays the connector role by deriving from the Connector class.

##### OutputHandler
- Concrete subclass of **ServiceHandler**.
- Forwards user-typed messages to the server and prints replies.

##### Dynamics
This diagram shows how the client and server components interact to establish connections and run the service logic.

![Sequence — end-to-end example (client ↔ server)](/assets/images/example_acceptor_connector_Sequence.png)

### Directory and file structure
Related source files:

```bash
├── applications
│   ├── example_acceptor_connector
│   │   ├── AcceptorImpl.cpp
│   │   ├── AcceptorImpl.hpp
│   │   ├── Client.cpp
│   │   ├── Client.hpp
│   │   ├── ConnectorImpl.cpp
│   │   ├── ConnectorImpl.hpp
│   │   ├── InputHandler.cpp
│   │   ├── InputHandler.hpp
│   │   ├── MainClient.cpp
│   │   ├── MainServer.cpp
│   │   ├── OutputHandler.cpp
│   │   └── OutputHandler.hpp
├── framework
│   ├── acceptor_connector
│   │   └── 1_0
│   │       ├── Acceptor.cpp
│   │       ├── Acceptor.hpp
│   │       ├── Config.hpp
│   │       ├── Connector.cpp
│   │       ├── Connector.hpp
│   │       ├── ServiceHandler.cpp
│   │       ├── ServiceHandler.hpp
│   │       ├── SockAcceptor.cpp
│   │       ├── SockAcceptor.hpp
│   │       ├── SockConnector.cpp
│   │       ├── SockConnector.hpp
│   │       ├── SockStream.cpp
│   │       └── SockStream.hpp

```

