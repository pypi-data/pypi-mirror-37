# STDLIB Imports
import os
import threading

# 3rd Party Imports
import pika
from pika.exceptions import (
    ConnectionClosed,
    ChannelClosed,
    ChannelError,
)

# Local Imports
from pcte_dynaprov import (
    rmqlog,
    q
)


rmqhost = os.environ.get('RMQ_HOST', default='localhost')
rmqport = os.environ.get('RMQ_PORT', default=5672)
rmquser = os.environ.get('RMQ_USER', default='guest')
rmqpassword = os.environ.get('RMQ_PASSWORD', default='guest')
rmqex = os.environ.get('RMQ_EXCHANGE', default='SLAMREXCH')
rmqchan = os.environ.get('RMQ_CHANNEL', default='PCTE')
rmqq = os.environ.get('RMQ_QUEUE', default='PROVISIONING')


def rmq_daemon():
    rmqlog.debug(f"""
    Starting Thread with the following information:
        RabbitMQ Connection Details:\tamqp://{rmquser}:{rmqpassword}@{rmqhost}:{rmqport}/
        RabbitMQ Exchange:\t\t{rmqex}
        RabbitMQ Queue:\t\t{rmqq}
    """)

    def work(ch, method, properties, body):
        q.put(body)

    creds = pika.credentials.PlainCredentials(
        username=rmquser,
        password=rmqpassword
    )
    try:
        conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rmqhost,
                port=rmqport,
                credentials=creds,
                retry_delay=10,
                socket_timeout=30,
                blocked_connection_timeout=30))
        try:
            chan = conn.channel()
            chan.queue_declare(queue=rmqq)
            chan.basic_consume(
                work,
                queue=rmqq,
                no_ack=True,
            )
            rmqlog.info('Starting the RabbitMQ Consumer')
            chan.start_consuming()
        except ChannelClosed as e:
            rmqlog.error(f'RabbitMQ Channel Error... {e}')
        except ChannelError as e:
            rmqlog.error(f'RabbitMQ Channel Error... {e}')
    except ConnectionClosed as e:
        rmqlog.error(f'RabbitMQ Connection Error... {e}')


def start_daemon():
    threads = []
    t = threading.Thread(target=rmq_daemon)
    t.daemon = True
    t.start()
    threads.append(t)