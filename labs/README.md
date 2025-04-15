# Distributed Systems Course

This repository contains the implementation of various labs for the Distributed Systems course. The labs demonstrate concepts such as client-server communication, multithreading, and distributed architectures.

## Folder Structure

- `lab1/`: Contains the implementation of the first lab. This lab involves creating a **distributed calculator** and a **distributed chat application**

## Labs Overview

### Lab 1: Distributed Calculator and Chat Applications

- **Objective**:
  - Build distributed calculator and chat applications demonstrating client-server communication
- **Features**:
  - Calculator server evaluates mathematical expressions from multiple concurrent clients
  - Chat server enables real-time messaging between multiple clients using multithreading
  - Both applications use Python's socket library for network communication
  - Chat messages are broadcasted to all connected clients

### Lab 2: ...

## Running the Labs

### Lab 1 - Distributed Calculator

1. Navigate to the `lab1` directory.
2. Start the server by running the following command in one terminal:
   ```bash
   python server.py
   ```
3. In another terminal, run the client:
   ```bash
   python client.py
   ```

## Requirements

- Python 3.x
- No additional dependencies are required for these labs. All code uses Python's built-in `socket` and `threading` libraries.

## License

This project is licensed
