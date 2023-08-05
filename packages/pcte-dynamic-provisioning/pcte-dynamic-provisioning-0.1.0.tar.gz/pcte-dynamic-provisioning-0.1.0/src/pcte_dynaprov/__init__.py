import logging
import queue

# Initialize Logging
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG
)
mainlog = logging.getLogger('pcte-dynamoprovision.main')
apilog = logging.getLogger('pcte-dynamoprovision.api')
rmqlog = logging.getLogger('pcte-dynamoprovision.rmq')
parselog = logging.getLogger('pcte-dynamoprovision.parser')
outputlog = logging.getLogger('pcte-dynamoprovision.output')
clilog = logging.getLogger('pcte-dynamoprovision.cli')

q = queue.Queue()


__version__ = u'0.1\N{GREEK SMALL LETTER ALPHA}'