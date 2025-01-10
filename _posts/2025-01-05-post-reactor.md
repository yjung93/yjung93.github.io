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
- [Reacter Pattern](#reacter-pattern)
- [Simplifed Reactor Framework implementation](#simplifed-reactor-framework-implementation)
  - [Event infrastructure layer classes](#event-infrastructure-layer-classes)
    - [Reactor](#reactor)
    - [Event Handler](#event-handler)
  - [Application layer classes](#application-layer-classes)
    - [Server application](#server-application)
      - [Acceptor](#acceptor)
      - [ServerEventHandler](#servereventhandler)
    - [Client application](#client-application)
  - [How it works](#how-it-works)


## Overview
This page introduces the "Reactor Pattern", a powerfull design pattern widely used in high-performance networking application. We will explore this pattern through a simplifed implementation inspired by [the Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html) project.

## Reacter Pattern
The Reactor Pattern is a design pattern for handling servcie requests delivered concurrently to an application by one or more clients. It efficiently dimultiplexes and dispatches events to appropreate handler. It provides the following benifits.

- **Efficiency**: Handles multiple events using a single thread, reducing overhead.
- **Scalability**: Suitable for systems with many simultaneous connections.
- **Maintainability**: Promotes modular and decoupled code design.

## Simplifed Reactor Framework implementation
A simplified Reactor framework has been implemented to help understand the ractor pattern and to understand how to apply it in the framework. The source code of implementation is available on my [Git Repoisitory](https://github.com/yjung93/study_reactor_1_0)  This implementation retains the core architectural principles of ACE framework but removes unnecessary complexity for learning purposes.  

The relationship between classes in the Simplifed Reactor Framework is shown in the following diagram.

![alt text](/assets/images/reactor_class_diagram_v_1_1.jpg)

These classes play the following role in accordance with the Reactor Pattern.
- **Event infrastructure layer classes**  detects and demultiplexes events to eventhandler and then dispatches corresponding eventhook method of event handler implemented in applcation. it provides an application-independent approach for handling the event.

- **Application layer classes** performs application-defined processing by implementing event hook method. Application layer classes are desencants of event handler class.
  


### Event infrastructure layer classes

#### Reactor
- Manages and dispatches events to appropriate handlers
- Implements the select() system call to monitor multiple sockets for activity

```cpp
class Reactor {
public:
    int runReactorEventLoop();
    int registerHandler(EventHandler* handler, ReactorMask mask);
    int removeHandler(EventHandler* handler);
private:
    int handleEvents();
};
```
#### Event Handler
- Perform actions in response to events

```cpp
class EventHandler {
public:
    virtual int handleInput(int fd);
    virtual ~EventHandler();
};
```
### Application layer classes

#### Server application

![alt text](/assets/images/example_reactor.png)

##### Acceptor
- Responsible for accepting incoming client connections and creating corresponding ServerEventHandler instances.

```cpp
class Acceptor : public EventHandler {
public:
    void open();
    int handleInput(int fd);
};
```
##### ServerEventHandler
- Handles communication with individual clients. It echoes back received messages to demonstrate the functionality
 
```cpp
class ServerEventHandler : public EventHandler {
public:
    int handleInput(int fd);
};
```

#### Client application
- Communicates with server application for demonstration. it sends message user typed to server application and shows responded message from the server application.
- It is not implemented using framework.

### How it works
- The Acceptor listens for new client connections. When a connection is established, it creates a ServerEventHandler and registers it with the Reactor.
- The Reactor monitors all registered event handlers using the select() system call and delegates events to their respective handlers.
- The ServerEventHandler processes client messages and echoes them back​

![alt text](/assets/images/example_reactor_Sequence.png)

