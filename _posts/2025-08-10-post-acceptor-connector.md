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
- [Acceptor-Connector pattern \[POSA2\]](#acceptor-connector-pattern-posa2)
  - [Background](#background)
  - [Solution](#solution)
  - [Structure](#structure)
    - [Class diagram](#class-diagram)
    - [Dynamic](#dynamic)
- [Simplified Acceptor-Connector framework implementation](#simplified-acceptor-connector-framework-implementation)
  - [Design Choices](#design-choices)
  - [Structure](#structure-1)
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
This post covers the following topics:
- The **Acceptor-Connector pattern**  for decoupling connection establishment and initialization from application logic.
- A **simplified** implementation inspired by the [Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html). The source code is available at [https://github.com/yjung93/study_ACE_design_pattern](https://github.com/yjung93/study_ACE_design_pattern)

## Acceptor-Connector pattern [[POSA2](/references/post-references)]

### Background

Applications in connection-oriented network systems typically contain code for establishing connections and initializing application services. This code is complex and mostly independent of the application's core service logic. Therefore, it is beneficial to decouple the connection establishment and service initialization from the application service logic. This decoupling must satisfy the following factors:
- The application service should easily switch between different connection roles, such as a server, client, or both (peer-to-peer).
- The design of the connection establishment and service initialization must remain consistent and independent of changes to the application services or communication protocols.
- For large-scale networked systems, the latency of connection establishment must be minimized.

  
### Solution
Decouple the connection establishment and service initialization from the application service implementation by:

- Encapsulating the application services as peer service handlers. Each service handler implements one side of the end-to-end service in networked applications.
- Applying two factories: Acceptor and Connector.
  - **Acceptor**: Passively establishes a connection when requested by a client-side application service and initializes the associated service handler.
  - **Connector**: Actively establishes a connection and initializes the associated service handler.

### Structure
- **Passive-mode transport endpoint**: A factory that listens for connection requests, accepts them, and creates transport handles that encapsulate the newly connected transport endpoint. Data exchange is performed over the connected transport endpoint by reading from and writing to the transport handles.
- **Service handler**: Defines each side of an end-to-end service in networked applications. The concrete class of the service handler implements the application service on its side of the connection. It provides interface hook methods for initializing the service upon connection establishment.
- **Acceptor**: A factory that implements the passive-mode transport endpoint. It creates and initializes the associated service handler when a connection is established.
- **Connector**: A factory that implements the active-mode transport endpoint. It creates and initializes the associated service handler when a connection is established.
- **Dispatcher**: Demultiplexes various types of network events (such as connection requests and data requests) and dispatches them to registered acceptors, connectors, and service handlers.
- **Concrete service handlers**: Derive from the service handler and implement specific application services for each side of the end-to-end connection.


#### Class diagram
<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/acceptor_connector_pattern_class_diagram.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/acceptor_connector_pattern_class_diagram.svg" alt="Reactor PlantUML Diagram" width="100%">

#### Dynamic
Scenario 1: Passive connection establishment and initialization.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/acceptor_connector_pattern_dynamic_usecase_1.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/acceptor_connector_pattern_dynamic_usecase_1.svg" alt="Reactor PlantUML Diagram" width="100%">

Scenario 2: Synchronous active connection establishment and initialization.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/acceptor_connector_pattern_dynamic_usecase_2.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/acceptor_connector_pattern_dynamic_usecase_2.svg" alt="Reactor PlantUML Diagram" width="100%">

Scenario 3: Asynchronous active connection establishment and initialization.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/acceptor_connector_pattern_dynamic_usecase_3.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/acceptor_connector_pattern_dynamic_usecase_3.svg" alt="Reactor PlantUML Diagram" width="100%">


## Simplified Acceptor-Connector framework implementation

### Design Choices
This version keeps the core architectural ideas from ACE while intentionally skipping production-level complexity.

The following framework is used as infrastructure for this implementation:
- [Reactor framework](/design%20pattern%20-%20ace%20framework/post-reactor/)

The source code is available at [https://github.com/yjung93/study_ACE_design_pattern](https://github.com/yjung93/study_ACE_design_pattern) 

### Structure
The implementation is organized into three layers:

+ **Event infrastructure layer classes**
+ **Connection management layer classes**
+ **Application layer classes**

The relationships between classes in this framework are shown below.  

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_class_diagram.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_class_diagram.svg" alt="Reactor PlantUML Diagram" width="100%">

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

#### Acceptor
+ **Passively** establishes a connected transport endpoint.
+ Creates and initializes the associated **ServiceHandler** when a connection is accepted.
+ Decouples acceptance/initialization from the ServiceHandler that runs application logic.


**Interaction sequence**  

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_dynamic_acceptor.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_dynamic_acceptor.svg" alt="Reactor PlantUML Diagram" width="100%">

#### Connector
+ **Actively** establishes a connected transport endpoint.
+ Creates and initializes the associated **ServiceHandler** when the connection completes.
+ Decouples initiation/initialization from the ServiceHandler that runs application logic.
+ Supports **synchronous** and **asynchronous** connection.

**Interaction sequence (synchronous)**  

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_dynamic_connector_sync.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_dynamic_connector_sync.svg" alt="Reactor PlantUML Diagram" width="100%">

**Interaction sequence (asynchronous)**  

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_dynamic_connector_async.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_dynamic_connector_async.svg" alt="Reactor PlantUML Diagram" width="100%">

### Application layer classes
This layer customizes the generic strategies from the infrastructure and connection layers (via subclassing, composition, and/or template instantiation) to create concrete components that establish connections, exchange data, and implement service behavior.

#### Server application
Demonstration server: waits for client connections, accepts them, and echoes messages received from clients.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_server_class_diagram.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_server_class_diagram.svg" alt="Reactor PlantUML Diagram" width="100%">


##### AcceptorImpl
- Concrete subclass of **Acceptor**.
- Plays the acceptor role by deriving from the Acceptor class.

##### InputHandler
- Concrete subclass of **ServiceHandler**.
- Handles client I/O and echoes back received messages.

#### Client application
Demonstration client: sends user-typed messages to the server and displays the responses.

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_client_class_diagram.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_client_class_diagram.svg" alt="Reactor PlantUML Diagram" width="100%">


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

<!-- [AI Note]: The diagram below is generated from /_files/uml/plantUml/example_acceptor_connector_pattern_client_server_dynamic.puml -->
<img src="{{ site.baseurl }}/assets/images/uml/plantUml/example_acceptor_connector_pattern_client_server_dynamic.svg" alt="Reactor PlantUML Diagram" width="100%">


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

