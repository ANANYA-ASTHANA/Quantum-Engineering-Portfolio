import getpass
import subprocess

# Authentication Credentials
USER_AUTH = {
    "user1": "securepass123", "user2": "eqkdpass456",  # E91
    "user3": "tfpass789", "user4": "qkdpass987",       # TF-QKD
    "user5": "mdipass654", "user6": "qncpass321"       # MDI-QKD
}

# Node List Access Control
NODE_LIST_ACCESS_CODE = "accessnodes789"    #Ideally, different network layers should require different access codes, but here we shall use a single access code for simplicity.

# Node List (Mapped to username)
NODE_LIST = {
    "user1": "NodeA", "user2": "NodeB",     #The nodes are ideally required to have a MAC-Based Identification,
    "user3": "NodeC", "user4": "NodeD",     #but for our simulation of multiple nodes on the same system, we shall be using the current approach.
    "user5": "NodeE", "user6": "NodeF"
}

# User QKD Protocol Mapping
USER_QKD_PROTOCOLS = {
    "user1": "E91", "user2": "E91",
    "user3": "TF-QKD", "user4": "TF-QKD",
    "user5": "MDI-QKD", "user6": "MDI-QKD"
}

def authenticate_user():
    """Authenticates user before granting access to quantum network."""
    print("\n🔐 Quantum Network Authentication 🔐")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    if username in USER_AUTH and USER_AUTH[username] == password:
        print("✅ Authentication successful.")
        return username
    else:
        print("❌ Authentication failed.")
        exit(1)

def get_node_list():
    """Authenticates user for access to the quantum node list."""
    print("\n📜 Secure Access to Quantum Node List 📜")
    access_code = getpass.getpass("Enter access code for node list: ")

    if access_code == NODE_LIST_ACCESS_CODE:
        print("\nAvailable Quantum Nodes:")
        for user, node in NODE_LIST.items():
            print(f" - {node}")
        return list(NODE_LIST.values())
    else:
        print("❌ Access Denied.")
        exit(1)

def determine_qkd_protocol(username):
    """Determines the QKD protocol for the authenticated user."""
    protocol = USER_QKD_PROTOCOLS.get(username, "Unknown")
    if protocol == "Unknown":
        print("❌ User is not assigned a QKD protocol.")
        exit(1)
    print(f"🔑 Assigned QKD Protocol: {protocol}")
    return protocol

def tf_qkd(my_node, target_node):
    """Placeholder simulation of the Twin-Field QKD (TF-QKD) protocol.
    print(f"\n🔄 Establishing TF-QKD between {my_node} and {target_node}...")
    print("📡 Sending weak coherent pulses through an untrusted relay...")
    print(f"✅ Secure key established between {my_node} and {target_node} via TF-QKD.")"""
    user_process = subprocess.Popen(["python3", "TF_QKD.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = user_process.communicate()
    print("OUTPUT:", output)
    print("ERROR:", error)

def mdi_qkd(my_node, target_node):
    """Placeholder simulation of the Measurement-Device-Independent QKD (MDI-QKD) protocol.
    print(f"\n🔄 Establishing MDI-QKD between {my_node} and {target_node}...")
    print("📡 Alice and Bob send qubits to an untrusted relay for Bell-state measurement...")
    print(f"✅ Secure key established between {my_node} and {target_node} via MDI-QKD.")"""
    user_process = subprocess.Popen(["python3", "MDI_QKD.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = user_process.communicate()
    print("OUTPUT:", output)
    print("ERROR:", error)

def initiate_qkd_session(user, protocol):
    """Chooses the correct QKD protocol and initiates the session."""
    #processes = []
    if protocol == "E91":
        if user == "user1":
            print("🚀 Launching Alice's QKD script...")
            user1_process = subprocess.Popen(["python3", "user1_e91.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output1, error1 = user1_process.communicate()
            print("OUTPUT:", output1)
            print("ERROR:", error1)
            #processes.append(user1_process)
        elif user == "user2":
            print("🚀 Launching Bob's QKD script...")
            user2_process = subprocess.Popen(["python3", "user2_e91.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output2, error2 = user2_process.communicate()
            print("OUTPUT:", output2)
            print("ERROR:", error2)
            #processes.append(user2_process)
        else:
            print("❌ Unauthorized access to selected protocol. Exiting.")
            exit(1)    
    elif protocol == "TF-QKD":
        tf_qkd(my_node, selected_node)
    elif protocol == "MDI-QKD":
        mdi_qkd(my_node, selected_node)
    else:
        print("❌ Unknown QKD protocol. Exiting.")
        exit(1)
    # ✅ Ensure both scripts run in parallel
    #for process in processes:
        #process.wait()  # Wait for each subprocess to finish

if __name__ == "__main__":
    # Step 1: Authenticate user
    user = authenticate_user()

    # Step 2: Authenticate access to node list
    available_nodes = get_node_list()

    # Step 3: User selects a node
    print("\n🔘 Select a node to establish a QKD session:")
    selected_node = input("Enter the node name: ")

    if selected_node not in available_nodes:
        print("❌ Invalid node selection. Exiting.")
        exit(1)

    # Step 4: Determine the user's assigned QKD protocol
    qkd_protocol = determine_qkd_protocol(user)

    # Step 5: Identify the current node using entered username (Ideally, should be MAC-Based)
    my_node = NODE_LIST.get(user, "Unknown")

    if my_node == "Unknown":
        print("❌ Unrecognized node. Exiting.")
        exit(1)

    # Step 6: Initiate QKD session with the chosen protocol
    initiate_qkd_session(user, qkd_protocol)
