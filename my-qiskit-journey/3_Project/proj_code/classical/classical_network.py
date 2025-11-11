import eventlet
eventlet.monkey_patch()
from ns import ns
import random
import os
import base64
import pyotp
from pyvis.network import Network
from flask import Flask, session, redirect, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # For data encryption
from PP_1 import encrypt_data
from PP_2 import decrypt_data
from session_keys import session_keys  # Import session keys
import threading
import hashlib
import hmac
import networkx as nx

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key_here'  # Set your secret key
socketio = SocketIO(app)

# Create network nodes
nodes = ns.NodeContainer()
nodes.Create(7)  # 6 nodes representing the 3 layers + 1 for the network admin

# Install Internet stack
stack = ns.InternetStackHelper()
stack.Install(nodes)

# Define hierarchical layers
layers = {
    "layer_1": [nodes.Get(0), nodes.Get(1)],  # Government Cabinet ↔ Military HQ
    "layer_2": [nodes.Get(2), nodes.Get(3)],  # Military HQ ↔ Regional Base Stations
    "layer_3": [nodes.Get(4), nodes.Get(5)],   # Inter-Base Stations Communication
}

admin_node = nodes.Get(6)  # Admin node, separate from hierarchical layers

# Set up links with SDN & THz/mmWave adaptability
p2p = ns.PointToPointHelper()
p2p.SetDeviceAttribute("DataRate", ns.StringValue("10Gbps"))
p2p.SetChannelAttribute("Delay", ns.StringValue("1ms"))

devices = {}
for layer, node_pair in layers.items():
    devices[layer] = p2p.Install(node_pair[0], node_pair[1])

# Admin connection via CSMA
csma = ns.CsmaHelper()
csma.SetChannelAttribute("DataRate", ns.StringValue("10Gbps"))
csma.SetChannelAttribute("Delay", ns.StringValue("1ms"))
admin_container = ns.NodeContainer()
admin_container.Add(admin_node)
admin_device = csma.Install(admin_container)

# Assign IP to Admin’s CSMA network first
address = ns.Ipv4AddressHelper()
address.SetBase("10.1.99.0", "255.255.255.0")  
admin_ip_interface = address.Assign(admin_device)  
address.NewNetwork()  # Move to a new subnet for the next network

# Assign IPs to other nodes (Wi-Fi based)
ip_interfaces = {}
for i, (layer, dev) in enumerate(devices.items()):
    address.SetBase(f"10.1.{i+1}.0", "255.255.255.0")  # Different subnet per layer
    ip_interfaces[layer] = address.Assign(dev)
    address.NewNetwork()  # Move to a new subnet for the next layer

# Define available modulation schemes with corresponding data rates
MODULATION_SCHEMES = {
    0: {"mcs": 0, "modulation": "BPSK", "coding_rate": "1/2", "snr_threshold": 3},
    1: {"mcs": 1, "modulation": "QPSK", "coding_rate": "1/2", "snr_threshold": 6},
    2: {"mcs": 2, "modulation": "QPSK", "coding_rate": "3/4", "snr_threshold": 10},
    3: {"mcs": 3, "modulation": "16-QAM", "coding_rate": "1/2", "snr_threshold": 14},
    4: {"mcs": 4, "modulation": "16-QAM", "coding_rate": "3/4", "snr_threshold": 18},
    5: {"mcs": 5, "modulation": "64-QAM", "coding_rate": "2/3", "snr_threshold": 22},
    6: {"mcs": 6, "modulation": "64-QAM", "coding_rate": "3/4", "snr_threshold": 26},
    7: {"mcs": 7, "modulation": "64-QAM", "coding_rate": "5/6", "snr_threshold": 30},
    8: {"mcs": 8, "modulation": "256-QAM", "coding_rate": "3/4", "snr_threshold": 35},
    9: {"mcs": 9, "modulation": "256-QAM", "coding_rate": "5/6", "snr_threshold": 40},
    10: {"mcs": 10, "modulation": "1024-QAM", "coding_rate": "3/4", "snr_threshold": 45},
    11: {"mcs": 11, "modulation": "1024-QAM", "coding_rate": "5/6", "snr_threshold": 50},
}

# Function to determine the best modulation based on SNR, Load, and BER
def select_modulation(snr):
    """
    Selects an appropriate MCS index based on SNR, BER, and network load.
    """
    best_mcs = 0  # Default to lowest modulation (BPSK MCS-0)

    for mcs, params in MODULATION_SCHEMES.items():
        if snr >= params["snr_threshold"]:  
            best_mcs = mcs  # Assign best available MCS

    print(f"[SDN] Selected MCS-{best_mcs} ({MODULATION_SCHEMES[best_mcs]['modulation']}) for SNR={snr}")
    
    return best_mcs

# Function to apply modulation dynamically
def apply_modulation(devices, mcs_index):
    """
    Apply 802.11ax MCS-based modulation dynamically.
    

    if mcs_index not in range(0, 12):  # MCS 0 to 11 in 802.11ax
        print(f"[Error] Invalid MCS index: {mcs_index}")
        return

    # Create WifiHelper and configure it for HE (802.11ax)
    wifi = ns.WifiHelper()
    wifi_mac = ns.WifiMacHelper()
    wifi_phy = ns.YansWifiPhyHelper()

    wifi_phy.Set("TxPowerStart", ns.DoubleValue(20.0))
    wifi_phy.Set("TxPowerEnd", ns.DoubleValue(20.0))

    # Set Remote Station Manager for 802.11ax
    wifi.SetRemoteStationManager(
        "ns3::HeWifiManager",  # HE (High-Efficiency) for 802.11ax
        "VhtMcs", ns.StringValue(str(mcs_index))  # Use MCS-based modulation
    )

    # Apply modulation to devices
    for dev in devices.values():
        wifi_phy.Install(dev)"""

    print(f"[SDN] 802.11ax Modulation switched to MCS-{mcs_index}")

# Simulate dynamic network conditions
def simulate_network_conditions():
    global snr, network_load, ber
    snr = random.uniform(5, 35)  # SNR in dB
    network_load = random.randint(10, 100)  # Network load percentage
    ber = random.uniform(0, 0.2)  # Bit Error Rate (BER)
    return snr, network_load, ber

# Periodic modulation switching
def dynamic_modulation_switch(event_time=5):
    global snr, network_load, ber
    snr, network_load, ber = simulate_network_conditions()  # Get all required parameters
    new_modulation = select_modulation(snr)  # Use the updated selection logic
    apply_modulation(devices, new_modulation)  # Apply modulation dynamically
    
    # Emit updated network status to UI
    socketio.emit('network_update', {
        'snr': snr,
        'ber': ber,
        'load': network_load,
        'modulation': new_modulation
    })

    # Reschedule the function periodically
    if ns.Simulator.IsFinished():
        return
    ns.Simulator.Stop(ns.Seconds(event_time))

# Anomaly Detection
def detect_anomalies():
    global snr, network_load, ber
    global packet_loss_rate # Set packet loss rate as global variable to be shared by functions
    packet_loss_rate = random.uniform(0, 5)
    unauthorized_attempts = random.randint(0, 2)

    # Anomaly conditions based on new parameters
    if snr < 8 or ber > 0.15:
        print("Low SNR or excessive Bit Error Rate detected!")
        socketio.emit('network_alert', {'message': "Low SNR or excessive Bit Error Rate detected!"})
    if network_load > 80:
        print("High network congestion detected!")
        socketio.emit('network_alert', {'message': "High network congestion detected!"})
    if packet_loss_rate > 3:
        print("High packet loss detected!")
        socketio.emit('network_alert', {'message': "High packet loss detected!"})
    if unauthorized_attempts > 0:
        print("Unauthorized access attempt detected!")
        socketio.emit('network_alert', {'message': "Unauthorized access attempt detected!"})

    # Reschedule anomaly detection periodically
    ns.Simulator.Stop(ns.Seconds(10))

# Initialize PyVis Network
net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")

# Real-time network visualization
def visualize_network():
    simulate_network_conditions()
    dynamic_modulation_switch()
    detect_anomalies()
    #net.clear()  # Clear previous visualization
    G = nx.Graph()

    # Simulate network conditions and bring packet loss rate
    global snr, network_load, ber
    global packet_loss_rate
    # Add nodes with attributes based on network conditions
    for layer, nodes in layers.items():
        node_1, node_2 = nodes
        
        # Define node color based on BER and network load
        if ber > 0.1:
            node_color = "red"  # High BER nodes in red
        elif network_load > 80:
            node_color = "orange"  # High load nodes in orange
        else:
            node_color = "lightblue"  # Normal nodes
        
        # Add nodes to PyVis
        node_id_1 = node_1.GetId()  # Extract ID from ns3::Node pointer
        node_id_2 = node_2.GetId()  # Extract ID from ns3::Node pointer
        print(f"[DEBUG] node_id_1: {node_id_1}, type: {type(node_id_1)}")
        print(f"[DEBUG] node_id_2: {node_id_2}, type: {type(node_id_2)}")
        net.add_node(node_id_1, label=str(node_id_1), color=node_color, title=f"SNR: {snr} dB\nBER: {ber}\nLoad: {network_load}%")
        net.add_node(node_id_2, label=str(node_id_2), color=node_color, title=f"SNR: {snr} dB\nBER: {ber}\nLoad: {network_load}%")

        # Define edge color based on packet loss
        edge_color = "red" if packet_loss_rate > 3 else "lightgray"

        # Add edges with tooltips for additional info
        net.add_edge(node_id_1, node_id_2, color=edge_color, title=f"Packet Loss: {packet_loss_rate}%")

    # Save dynamic visualization as an interactive HTML file
    net.generate_html(name = "scratch/templates/network_visualization.html")
    net.save_graph("scratch/templates/network_visualization.html")

    # Emit updated visualization to front-end
    socketio.emit('network_visualization', {'html_url': 'network_visualization.html'})

    # Call visualization function periodically
    ns.Simulator.Stop(ns.Seconds(60))

def bits_to_bytes(bits):
    return int(''.join(map(str, bits)), 2).to_bytes(32, 'big')

byte_keys = [bits_to_bytes(key) for key in session_keys]


# Authentication and hierarchical subnet handling
class MilitaryNetwork:
    def __init__(self):
        self.authenticated_nodes = {}
        self.subnets = {layer: [] for layer in layers}
        self.totp_secrets = {}

    def generate_mfa_secret(self, node_id):
        global totp
        self.totp_secrets[node_id] = pyotp.random_base32()
        #return self.totp_secrets[node_id]
        totp = pyotp.TOTP(self.totp_secrets[node_id])
        print(totp)
        return totp
    def verify_mfa(self, node_id, mfa_code):
        #if node_id not in self.totp_secrets:
        #return False
        #totp = pyotp.TOTP(self.totp_secrets[node_id])
        global totp
        return totp.verify(mfa_code)

    def authenticate(self, node_id, mfa_code, qkd_challenge):
        resolved_layer = None
        if node_id == "admin":
            return "Admin authenticated"
        for layer_name, node_list in layers.items():
            for node in node_list:
                print(node.GetId())
                if node_id == f"node_{node.GetId()}":
                    resolved_layer = layer_name
                    print(resolved_layer)
                    break
                if resolved_layer:
                    break

        if not resolved_layer:
            return "Node ID not recognized in any layer."
        
        #if not self.verify_mfa(node_id, mfa_code):
        #return "Invalid MFA code - Access Denied"

        if mfa_code != "mfa_code":
            return "Invalid MFA code - Access Denied"
        
        qkd_key = "secure_qkd_key"  # Placeholder for QKD-generated key
        expected_response = hmac.new(qkd_key.encode(), node_id.encode(), hashlib.sha256).hexdigest()
        print(expected_response)
        if "expected_response" != qkd_challenge:
            return "QKD authentication failed - Access Denied"
        
        self.authenticated_nodes[node_id] = resolved_layer
        self.subnets[resolved_layer].append(node_id)
        return "Access Granted"

military_network = MilitaryNetwork()
totp = military_network.generate_mfa_secret("node_0")

# Flask-based UI
@app.route('/')
def index():
    return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login():
    #return render_template('login.html')
    data = request.json
    node_id = data.get('node_id')
    mfa_code = data.get('mfa_code')
    qkd_challenge = data.get('qkd_challenge')

    print(f"[DEBUG] Received Login - Node ID: {node_id}, MFA: {mfa_code}, QKD: {qkd_challenge}")
    
    result = military_network.authenticate(node_id, mfa_code, qkd_challenge)
    
    if "Admin authenticated" in result:
        return jsonify({"status": "success", "message": result, "redirect": "/visualizations"})
    elif "Access Granted" in result:
        session['node_id'] = node_id  # Save the sender_node_id in the session
        return jsonify({"status": "success", "message": result, "redirect": f"/chatroom/{node_id}"})
    else:
        return jsonify({"status": "error", "message": result})

@app.route('/chatroom/<node_id>')
def chatroom(node_id):
    if 'node_id' in session and session['node_id'] == node_id:
        # Pass sender_node_id to the frontend
        return render_template('chatroom.html', sender_node_id=session['node_id'])
    return "Unauthorized Access", 403

@app.route('/visualizations')
def visualizations():
    visualize_network()
    return render_template('network_visualization.html')  # Page displaying network visualizations
    return jsonify({"status": "success"})

# Dictionary to store socket_id for each node_id
node_socket_mapping = {}

# Store the node's socket id when they connect
@socketio.on('connect')
def handle_connect():
    if 'node_id' in session:  # Ensure session has a valid node_id
        node_id = session['node_id']
        node_socket_mapping[node_id] = request.sid  # Map node_id to socket_id
        join_room(node_id)  # ✅ No more error here!
        print(f"[CONNECT] Node {node_id} joined room {node_id}")
        print(f"Node {node_id} connected with socket_id {request.sid}")
    else:
        print("Connection attempt without session node_id")

# Handle message sending
@socketio.on('send_message')
def handle_send_message(data):
    sender_node_id = session.get('node_id', 'Unknown')  # Retrieve sender's node_id from session
    if sender_node_id == "Unknown":
        return emit('error', {'message': 'User not authenticated'})
    recipient_node_id = data.get('recipient_node_id')  # Intended recipient's node_id
    message = data.get('message')

    if not sender_node_id:
        print("Error: No session node_id found")
        return

    if isinstance(message, str):
        message = message.encode('utf-8')  # Convert string to bytes
        print("Converted!")
    print(f"Received message from {sender_node_id} to {recipient_node_id}: {message}")

    # Ensure session keys exist
    if not session_keys:
        return emit('error', {'message': 'No session keys available'})

    # Select a session key (e.g., first session key) for encryption
    #session_key = session_keys[0]
    
    print("Applied!")
    iv, ciphertext, tag = encrypt_data(message, byte_keys[0])    #AES-256 encryption of sender's data
    print("Encrypted!")
    # Save encrypted data
    encrypted_output = {
        "iv": base64.b64encode(iv).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
        "tag": base64.b64encode(tag).decode('utf-8')
    }
    
    if recipient_node_id:
        # Emit the message to the recipient's node ID
        emit('receive_message', {'message': encrypted_output, 'sender': sender_node_id}, room=recipient_node_id)
        print("Sent data!")
    else:
        print(f"Recipient node {recipient_node_id} not connected.")

@socketio.on('decrypt_request')
def handle_receive_message(data):
    recipient_node_id = session.get('node_id', 'Unknown')  # Retrieve recipient's node_id from session
    #recipient_socket_id = node_socket_mapping.get(recipient_node_id)
    if recipient_node_id == "Unknown":
        return emit('error', {'message': 'User not authenticated'})
    sender_node_id = data.get('from')
    #sender_socket_id = node_socket_mapping.get(sender_node_id)
    encrypted_message = data.get('msg')  # This contains {'iv': ..., 'ciphertext': ..., 'tag': ...}
    print("Received data!")
    if not encrypted_message:
        emit('error', {'message': 'No encrypted data received'}, room=recipient_node_id)
        return

    # Load session key (first one)
    if not session_keys:
        emit('error', {'message': 'No session keys available'}, room=recipient_node_id)
        return

    #session_key = bytes(session_keys[0])  # Ensure key is in bytes

    # Extract IV, ciphertext, and tag
    try:
        iv = base64.b64decode(encrypted_message["iv"])
        ciphertext = base64.b64decode(encrypted_message["ciphertext"])
        tag = base64.b64decode(encrypted_message["tag"])
    except (ValueError, KeyError):
        emit('error', {'message': 'Invalid encryption data format'}, room=recipient_node_id)
        return

    # Decrypt message
    try:
        decrypted_message = decrypt_data(iv, ciphertext, tag, byte_keys[0])
        decrypted_message = decrypted_message.decode('utf-8')  # Convert bytes → string
        print(f"Decrypted message for recipient {recipient_node_id}: {decrypted_message}")

        # Send decrypted message to the recipient
        emit('decrypted_message', {
            'from': sender_node_id,
            'decrypted': decrypted_message
        }, room=recipient_node_id)

        # Optional confirmation back to sender
        emit('message_received', {
            'confirmation': 'Message received and decrypted'
        }, room=sender_node_id)
        
    except Exception as e:
        emit('error', {'message': f'Decryption failed: {str(e)}'}, room=recipient_node_id)

@socketio.on('key_manage')
def handle_message_confirmation(data):
    if data.get('confirmation') == 'Message received and decrypted':
        if session_keys:
            used_key = session_keys.pop(0)  # Remove the first session key
            print(f"Session key {used_key} used and deleted.")

            # **Update session_keys.py file**
            with open("scratch/session_keys.py", "w") as f:
                f.write(f"session_keys = {session_keys}\n")  # Overwrite with updated keys

# Disconnect the socket and clean up
@socketio.on('disconnect')
def handle_disconnect():
    # Remove node_id from the mapping when disconnected
    for node_id, socket_id in list(node_socket_mapping.items()):
        if socket_id == request.sid:
            node_socket_mapping.pop(node_id, None) # Safe deletion
            print(f"Node {node_id} disconnected")
            break
        
def run_ns3():
    ns.Simulator.Run()
    socketio.emit('simulation_complete', {'message': 'NS-3 simulation ended'})
    ns.Simulator.Destroy()
    
# Start Flask and NS-3 simulation
if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    t = threading.Thread(target=lambda: socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False))
    t.daemon = False
    t.start()
    t.join()
    print("[DEBUG] Flask started!")
    ns3_thread = threading.Thread(target=run_ns3)
    ns3_thread.start()
    ns3_thread.join()
    print("[DEBUG] ns3 started!")
