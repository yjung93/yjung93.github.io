---
title: "Acceptor Connector Pattern"
classes: wide
categories:
  - Design Pattern - ACE Framework
tags:
  - Acceptor Connector
---

**Table of Contents**
- [Overview](#overview)
- [Simplifed Acceptor Connector Framework implementation](#simplifed-acceptor-connector-framework-implementation)
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
  - [Directory and file Structure](#directory-and-file-structure)


## Overview
This page introduces the "Acceptor Connector Pattern" [[POSA2](/references/post-references)]  which decouple the connection and initialization of cooperating peer services in networked application from the implementation performing application services after conntction and initialization is completed. This page will explore this pattern through a simplifed implementation inspired by [the Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html) project.

## Simplifed Acceptor Connector Framework implementation

A simplified Acceptor Connector framework has been implemented to help understand the Acceptor-Connector pattern and to understand how to apply it in the framework. The source code of implementation is available on my [Git Repoisitory](https://github.com/yjung93/study_reactor_1_0)  This implementation retains the core architectural principles of ACE framework but removes unnecessary complexity for learning purposes.  


### Structure
The implemtation of the Acceptor-Connector pattern can be broken down into three layers.
+ Event infrastructure layer classes
+ Connection management layer classes
+ Application layer classes
  
The relationship between classes in this Framework is shown in the following diagram.
![alt text](/assets/images/acceptor_connector_class_diagram_v_1_1.png)

### Event infrastructure layer classes
The simplified acceptor-connector framework is implemented on top of reactor framework which performs as a infrasctructure layer. This layer performs generic, applicationtion- independenct stratage for dispatching event. The more detail description is available in the previous post [Reactor Pattern](/design%20pattern%20-%20ace%20framework/post-reactor/)

### Connection management layer classes
This layer performs generic, application-independent connection and initialization services.
It consists of the following classes.
+ ServiceHandler
+ Acceptor
+ Connector

#### ServiceHandler

+ Provides required interfaces for application service implementation.
+ The application service is the concrete class of service handler and typically plays role as a client, server or both in peer to peer service in a networked system.
+ Created by Acceotpr or Connector when connection is established.
+ Provides hook method called by an Acceptor or Connector for activation of service on connection being established.
+ Provides a data-mode transport endpoint used by application service to cummunicate with it's peer applciation service. The type of the transport endpoint is parameterized by template type. The implementation of parameterized transport endpoint varies across operation system and it separate low-level implementation from application service level. 

![alt text](/assets/images/service_handler_class_diagram.png)

#### Acceptor
+ Passively establish a connected transport endpoint.
+ Create and initialize an associated service handler on connection establishment.
+ Decouples the above roles from the service handler implementation, which performs an application service process.

![alt text](/assets/images/acceptor_class_diagram.png)

Dynamics

![alt text](/assets/images/acceptor_connection_acceptance_equence.png)

#### Connector
+ Actively establish a connected transport endpoint
+ Create and initialize an associated service handler.
+ Decouples the above roles from the service handler implementation which performs application servic process.
+ It support a synchronous and asynhronous connection.

![alt text](/assets/images/connector_class_diagram.png)

Dynamics

Synchronous connection.
![alt text](/assets/images/connector_synchronous_Sequence.png)

Aynchronous connection.
![alt text](/assets/images/connector_asynchronous_Sequence.png)

### Application layer classes
This layer then customizes the generic strategies performed by the other two layers via subclassing, object composition, and/or parameterized type instantiation, to create concrete components that establish connections, exchange data, and perform service-specific processing. 

#### Server application
- Communicates with a client application for a demonstration. it wait and accept the connection from the client and replies back messages clients sent.

![alt text](/assets/images/example_acceptor_connector_server_diagram.png)

##### AcceptorImpl
- The concrete class of an Acceptor class
- Plays a role as a acceptor by deriving the accectpr class.

##### InputHandler
- The concrete class of a serviceHandler class.
- Handles communication with client. It echoes back received messages to demonstrate the functionality.
 

#### Client application
- Communicates with a server application for demonstration. it sends message user typed to server application and shows responded message from the server application.


![alt text](/assets/images/example_acceptor_connector_client_diagram.png)

##### Client
- The facade class integrates instance of Connector and ServiceHandler.

##### ConnectorImpl
- The concrete class of the Conenctor class
- Plays a role as a connector by deriving the Connector class.

##### OutputHandler
- The concrete class of a serviceHandler class.
- Handles communication with server. It foward user typed message to server and displays received message from the server.


##### Dynamics
This diagram illustrates how components of a client and server application interact to establish connections and handle application services.

![alt text](/assets/images/example_acceptor_connector_Sequence.png)

### Directory and file Structure
The related souce files.

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