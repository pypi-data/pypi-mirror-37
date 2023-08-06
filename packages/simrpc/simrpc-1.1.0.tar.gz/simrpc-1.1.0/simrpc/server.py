import zmq
import asyncio
import time
import inspect
import logging
from concurrent.futures import ThreadPoolExecutor
from zmq.asyncio import Context
from .message import encode_msg, decode_msg_body

logger = logging.getLogger(__package__)


class SimRpcServer:

    def __init__(
        self, async_task=False,
        device_front_address="tcp://127.0.0.1:5559",
        device_backend_address="tcp://127.0.0.1:5560",
        worker_address="tcp://localhost:5560",
        max_workers=30,
        period_task_name="period_tasks",
    ):
        self.data = {}
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.thread_tasks = set()
        self.device_front_address = device_front_address
        self.device_backend_address = device_backend_address
        self.worker_address = worker_address
        self.async_task = async_task
        self.period_task_name = period_task_name

    def register(self, instance):
        name = instance.__class__.__name__
        if name == "function":
            self.data[instance.__name__] = instance
        else:
            self.data[name] = instance

    def register_with_init(self, *args, cls_list=None, settings=None, **kwargs):
        for cls in cls_list:
            try:
                cls_settings = settings.get(cls.__name__, {})
                instance = cls(*cls_settings.get("args", ()),
                               **cls_settings.get("kwargs", {}))
            except Exception as tmp:
                logger.exception(tmp)
                instance = None
            if instance:
                self.register(instance)

    def zmq_device(self):
        logger.info('start zmq queue')
        while True:
            try:
                context = zmq.Context()
                # Socket facing clients
                frontend = context.socket(zmq.XREP)
                frontend.bind(self.device_front_address)
                # Socket facing services
                backend = context.socket(zmq.XREQ)
                backend.bind(self.device_backend_address)
                logger.info('start zmq queue end')
                zmq.device(zmq.QUEUE, frontend, backend)
            except Exception as e:
                logger.exception(e)
                logger.info("bringing down zmq device")
            finally:
                frontend.close()
                backend.close()
                context.term()

    def dispatch(self, message):
        message = encode_msg(message)
        service = message['service']
        entry = message['entry']
        if service == "function":
            entry = self.data.get(entry)
        else:
            instance = self.data.get(service)
            if instance and hasattr(instance, entry):
                entry = getattr(instance, entry)
        if callable(entry):
            result = entry(*message['args'], **message['kwargs'])
        else:
            result = None
        message = decode_msg_body({"response": result})
        return message

    async def async_dispatch(self, message):
        message = encode_msg(message)
        service = message['service']
        entry = message['entry']
        if service == "function":
            entry = self.data.get(entry)
        else:
            instance = self.data.get(service)
            if instance and hasattr(instance, entry):
                entry = getattr(instance, entry)
        if callable(entry):
            result = entry(*message['args'], **message['kwargs'])
            if inspect.isawaitable(result):
                result = await result
        else:
            result = None
        message = decode_msg_body({"response": result})
        return message

    def thread_run(self):
        # add period auto update task actor
        self.executor.submit(self.period_actor)
        num_thread = 4 if self.async_task else 20
        for i in range(num_thread):
            t = self.executor.submit(self.actor)
        while True:
            logger.info("check heathy status")
            dead_thread = set()
            for thread in self.executor._threads:
                if not thread.is_alive():
                    thread._tstate_lock.release()
                    thread.stop()
                    dead_thread.add(thread)
            self.executor._threads -= dead_thread
            for i in range(len(dead_thread)):
                t = self.executor.submit(self.actor)
            time.sleep(300)

    def start_broker(self):
        self.executor.submit(self.zmq_device)

    def run(self):
        self.thread_run()

    def tasks(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect(self.worker_address)
        while True:
            #  Wait for next request from client
            message = socket.recv()
            try:
                message = self.dispatch(message)
            except Exception as tmp:
                message = ""
                logger.exception(tmp)
            socket.send(message)

    async def async_tasks(self):
        context = Context()
        socket = context.socket(zmq.REP)
        socket.connect(self.worker_address)
        while True:
            #  Wait for next request from client
            message = await socket.recv()
            # print(message)
            try:
                message = await self.async_dispatch(message)
            except Exception as tmp:
                message = ""
                logger.exception(tmp)
            await socket.send(message)

    def actor(self):
        if self.async_task:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            task = loop.create_task(self.async_tasks())
            loop.run_forever()
        else:
            self.tasks()

    def period_actor(self):
        if self.async_task:
            tasks = []
            for obj in self.data.values():
                if obj.__class__.__name__ != "function":
                    if hasattr(obj, self.period_task_name):
                        tt = getattr(obj, self.period_task_name)()
                        tasks += tt

            if tasks:
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    asyncio.gather(*tasks)
                    loop.run_forever()
                except Exception as tmp:
                    logger.exception(tmp)
