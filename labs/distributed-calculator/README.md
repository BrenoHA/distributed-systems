# Distributed Calculator (Pyro5)

This project implements a distributed calculator using Pyro5, where a calculator object's methods are exposed and can be accessed by a remote client.

## Requirements

- Python 3.x
- Pyro5: Install it with the following command:
  ```bash
  pip install Pyro5
  ```

## How to Run

### 1. **Start the Pyro5 Nameserver**

Before running the server and client, start the Pyro5 nameserver. Run this command in a terminal:

```bash
python3 -m Pyro5.nameserver --host <your_server_ip>
```

### 2. **Run the Calculator Server**

Open another terminal and run the calculator server:

```bash
python server.py
```

### 3. **Run the Client**

Finally, in another terminal, run the client that will interact with the server:

```bash
python client.py
```

The client will ask the user which operation to perform, request the necessary parameters, and then call the remote method on the server.

## How It Works

- The **server** exposes the calculator methods as remote objects, allowing the client to call them over the network.
- The **client** uses Pyro5 to connect to the server, sends data for computation, and receives the results remotely.
