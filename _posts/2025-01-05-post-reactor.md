---
title: "Reactor Pattern"
excerpt_separator: "<!--more-->"
categories:
  - Design Pattern - ACE Framework
tags:
  - Reactor
---
**Table of Contents**
- [Overview](#overview)
- [Reacter Pattern](#reacter-pattern)
- [Simplifed Reactor Framework implementation](#simplifed-reactor-framework-implementation)
  - [Key components](#key-components)
  - [Reactor class](#reactor-class)
  - [EventHandler class](#eventhandler-class)
- [Example application using simplifed Reactor Framework](#example-application-using-simplifed-reactor-framework)
  - [Overview](#overview-1)
  - [Server](#server)
  - [Client](#client)


## Overview
This page introduces the "Reactor Pattern", a powerfull design pattern widely used in high-performance networking application. We will exploer this pattern through a simplifed implementation inspired by [the Adaptive Communication Environment (ACE)](https://www.dre.vanderbilt.edu/~schmidt/ACE.html) project.

## Reacter Pattern
The Reactor Pattern is a design pattern for handling servcie requets delivered concurrently to an application by one or more clients. It efficiently dimultiplex and dispatch events to appropreate handler. It provides the following benifits.

- **Efficiency**: Handles multiple events using a single thread, reducing overhead.
- **Scalability**: Suitable for systems with many simultaneous connections.
- **Maintainability**: Promotes modular and decoupled code design.


## Simplifed Reactor Framework implementation
A simplified Reactor framework has been implemented to help understand the Ractor pattern and to understand how to apply it in the framework. The source code of implementation is available on my [Git Repoisitory](https://github.com/yjung93/study_reactor_1_0)  This implementation retains the core architectural principles of ACE framework but removes unnecessary complexity for learning purposes.  

### Key components

- **Reactor**: Manages and dispatches events to appropriate handlers
- **Event Demultiplexer**: Waits for events and notifies the Reactor. In this implementation this part is implemented in Reactor component using selecor.
- **Event Handler**: Perform actions in response to events

The relationship between classes in the Simplifed Reactor Framework as shown in the following diagram.

![alt text](/assets/images/reactor_class_diagram_v_1_1.jpg)

These classes plays the following role in accordance with the Reactor Pattern.
- **Event infrastructure layer classes**  etects and demultiplexes events to eventhandler and then dispatch corresponding eventhook method of event handler implemented in applcation. it provides application indepentent approach for handling event.

- **Application layer classes** performs appliation-defined processing by implementing event hook method. Applicationlayer classes are desencants of event handler class.
  

### Reactor class

### EventHandler class

## Example application using simplifed Reactor Framework
### Overview

![alt text](/assets/images/example_reactor.png)


### Server
### Client

