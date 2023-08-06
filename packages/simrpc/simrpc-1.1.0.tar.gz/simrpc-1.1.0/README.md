# SimRpc

## Why SimRpc

all of the popular rpc framework today, is fast and stable.

but it is kind of not good enough for you to easily start.
you have to accept all the rpc's definition,learn their structure, and you have to adapt your code to them.

so if you dont like them,and you havn't have other alternatives. may be **SimRpc** is suit for you

## Intruction

SimRpc is an rpc tools for you to easily transfer your code to rpc service(both client-side and server-side),built on top of zeromq and msgpack.


* **zeromq**

    assures the message transfer extremely fast and stable

* **msgpack**

    enables the message blazing small

## Usage

### Your Original Code

``` python
class a:
    def minus(self, x, y):
        print("x+y=", x - y)
        return x - y
def add(x, y):
    return x + y
```

### Client Side

#### 1) start an client instance

``` python
from simrpc.client import SimRpcClient
rpc_client = SimRpcClient()
```

or maybe you want to start a specific address

``` python
from simrpc.client import SimRpcClient
rpc_client = SimRpcClient(server_address="tcp://localhost:6666")
```

the **server_address** is a zeromq address.

for more information you can refer to **[zeromq](http://zeromq.org/)**.

#### 2) add @rpc_client.task decorator to your code

``` python

# response_only=True means you only want the result

class a:

    @rpc_client.task(response_only=True)
    def minus(self, x, y):
        print("x+y=", x - y)
        return x - y

# func=True means this is a funcion,not a class service

@rpc_client.task(response_only=True,func=True)
def add(x, y):
    return x + y
```

#### 3) Use these functions as usual

### Server Side

#### 1) start an server instance

```python
from server import SimRpcServer
server = SimRpcServer()
```

like client,you can also give specific addresses to server.

parameter|value|instruction
-|-|-
device_front_address|"tcp://127.0.0.1:5559"|address that receive message. used for client to connect.
device_backend_address|"tcp://127.0.0.1:5560"|address that send message to service worker.
worker_address|"tcp://127.0.0.1:5560"|address that worker connect to. usually the same with device_backend_address.for advanced infomation,you can refer to zeromq

**more ways of address(like ipc) are supported, you can refer to zeromq**

#### 2) register your service to server

* initial your class service as usual

```python
service = a()
server.register(service)
```

* or you let server to initial your service(just pass your init arguments to server.)

```python
settings = {
    "a": {
        "kwargs": {
            "name": "test"
        }
    }
}
service = a()
server.register_with_init(a, settings=settings)
```

#### 3) start your rpc server broker

```python
server.start_broker()
# if you also want to start worker in process ,you could use server.run(),this will start a few workers.

# server.run()
```

**with this broker,you can easily expand your service from both client-side and server-side**

#### 4) start more workers

```python
# the same as above but without server.start_broker()
server.run()
```

### For details,you can refer to examples

## Dependence

* **[Zeromq](http://zeromq.org/)**
* **[Msgpack](https://msgpack.org/index.html)**

## Coding

* **like this project, star it**
* **any suggestion is welcome**
* **this project is under MIT lisense**

more docs are writing.
