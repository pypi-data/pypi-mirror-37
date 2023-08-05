NL = b'\n'
DATA_SIZE = 4
FRAME_SIZE = 4
HEADER_SIZE = DATA_SIZE + FRAME_SIZE
MAX_CHUNK_SIZE = 65536

TIMESTAMP_SIZE = 8
ATTEMPTS_SIZE = 2
MSG_ID_SIZE = 16
MSG_HEADER = TIMESTAMP_SIZE + ATTEMPTS_SIZE + MSG_ID_SIZE
MAX_CHUNK_SIZE = 65

FRAME_TYPE_RESPONSE = 0
FRAME_TYPE_ERROR = 1
FRAME_TYPE_MESSAGE = 2
MAGIC_V2 = b'  V2'

HEARTBEAT = b'_heartbeat_'
PULSE = b'NOP\n'
BIN_OK = b'\x00\x00\x00\x06\x00\x00\x00\x00OK'

# nsq TCP commands
FIN = b'FIN'
REQ = b'REQ'
TOUCH = b'TOUCH'
RDY = b'RDY'
MPUB = b'MPUB'
CLS = b'CLS'
AUTH = b'AUTH'
SUB = b'SUB'
PUB = b'PUB'
DPUB = b'DPUB'

# connection status
CLOSED = 0
INIT = 1
CONNECTED = 2
SUBSCRIBED = 3
