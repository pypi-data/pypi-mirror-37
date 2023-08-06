import logging
from queue import Queue
from threading import Thread
from time import time
from twilio.rest import Client
import multiprocessing



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class MessageWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        logger.info('Created {}'.format(self.name))

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            client, msg = self.queue.get()
            try:
                logger.info('{}: Sending message ({})'.format(self.name,msg))
                client.send_message(msg)
            except Exception as error:
                logger.error('{}: Error {} sending message ({})'.format(self.name,error,msg))
            finally:
                self.queue.task_done()
                self.queue


class MessageClient:
    """A wrapper client to talk to Twilio Messaging Services."""

    def __init__(self, acct_sid, auth_token):
        """Initialize client with appropriate twilio authentication."""
        self.account_sid = acct_sid
        self.auth_token = auth_token
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, query_params):

        message = self.client.messages.create(
            body=query_params.body,
            from_=query_params.from_,
            media_url=query_params.media_url,
            to=query_params.to
        )
        return message.sid

    def enqueue_messages(self, messages):

        ts = time()

        # Create a queue to communicate with the worker threads
        queue = Queue()
        # Create 2 worker threads for each core
        for x in range(multiprocessing.cpu_count() * 2):
            worker = MessageWorker(queue)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()
        # Put the tasks into the queue as a tuple
        for msg in messages:
            logger.info('Queueing message ({})'.format(msg))
            queue.put((self,msg))
        # Causes the main thread to wait for the queue to finish processing all the tasks
        queue.join()
        logging.info('Took %s seconds', time() - ts)
