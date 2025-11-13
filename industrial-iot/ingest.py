import time

from opcua import Client

# --- Connect to CODESYS OPC UA server ---
url = "opc.tcp://192.168.29.10:4840"  # Soft PLC running on another machine on LAN (in this case)
client = Client(url)

try:
    client.connect()
    print("✅ Connected to OPC UA server")

    # --- Browse for nodes (optional, to discover available tags) ---
    # root = client.get_root_node()
    # print("Root children:", root.get_children())

    # --- Get node handles using their browse names or node IDs ---
    # These names come from your CODESYS Symbol Configuration
    opcua_node_prefix = "ns=4;s=|var|CODESYS Control Win V3 x64.Application.FIO"
    machine_on_node = client.get_node(f"{opcua_node_prefix}.Start_Button")
    speed_set_node = client.get_node(f"{opcua_node_prefix}.Speed_Set")
    speed_actual_node = client.get_node(f"{opcua_node_prefix}.Conveyor_Motor_Speed")
    # sensor_node = client.get_node("ns=4;s=|var|PLC_PRG.End_Sensor")

    # --- Continuous reading loop ---
    while True:
        machine_on = machine_on_node.get_value()
        speed_set = speed_set_node.get_value()
        speed_actual = speed_actual_node.get_value()
        # sensor = sensor_node.get_value()

        print(
            f"Machine ON: {machine_on} | Speed Set: {speed_set:.2f} | "
            f"Speed Actual: {speed_actual:.2f} |"
            # f"End Sensor: {sensor}"
        )

        time.sleep(0.5)

except Exception as e:
    print("❌ Error:", e)

finally:
    client.disconnect()
    print("🔌 Disconnected")
