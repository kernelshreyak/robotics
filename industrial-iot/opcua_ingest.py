from opcua import Client
import time
import logging

logger = logging.getLogger(__name__)

# OPC UA endpoint (adjust to your Windows IP)
SERVER_URL = "opc.tcp://shreyak-laptop:53530/OPCUA/SimulationServer"
# Node ID of the simulated variable you want to read
NODE_ID = "ns=3;i=1003"

# Duration to read (seconds)
READ_DURATION = 10
READ_INTERVAL = 0.5  # seconds between reads

try:
    client = Client(SERVER_URL)
    client.connect()

    node = client.get_node(NODE_ID)

    print(f"Reading {NODE_ID} for {READ_DURATION} seconds...")
    start = time.time()

    while time.time() - start < READ_DURATION:
        value = node.get_value()
        print(f"{time.strftime('%H:%M:%S')}  Value = {value}")
        time.sleep(READ_INTERVAL)

    client.disconnect()
    print("Done.")

except Exception as e:
    logger.error("Error in OPC UA connection: " + str(e))
