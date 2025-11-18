import sys
from scapy.all import sniff, IP, TCP, UDP
from typing import List, Dict, Any

# --- Configuration and Rules ---

# Define the structure for a single firewall rule
# ACTION: 'ACCEPT' (allow) or 'DROP' (block)
# PROTOCOL: 'TCP', 'UDP', 'ICMP', or 'ANY'
# SRC_IP: Specific IP or 'ANY'
# DST_PORT: Specific port or 'ANY' (Only applicable for TCP/UDP)
Rule = Dict[str, Any]

FIREWALL_RULES: List[Rule] = [
    # Rule 1: Block all TCP traffic to port 22 (SSH) from any source
    {
        "ACTION": "DROP", 
        "PROTOCOL": "TCP", 
        "SRC_IP": "ANY", 
        "DST_PORT": 22
    },
    
    # Rule 2: Block all UDP traffic originating from 192.168.1.100
    {
        "ACTION": "DROP", 
        "PROTOCOL": "UDP", 
        "SRC_IP": "192.168.1.100", 
        "DST_PORT": "ANY"
    },
    
    # Rule 3: Allow all TCP traffic to port 80 (HTTP) 
    {
        "ACTION": "ACCEPT", 
        "PROTOCOL": "TCP", 
        "SRC_IP": "ANY", 
        "DST_PORT": 80
    },
    
    # Rule 4: Default rule - ACCEPT everything else (Placed last to act as fallback)
    {
        "ACTION": "ACCEPT", 
        "PROTOCOL": "ANY", 
        "SRC_IP": "ANY", 
        "DST_PORT": "ANY"
    },
]

# --- Core Firewall Logic ---

def check_packet_against_rules(packet, rules: List[Rule]) -> str:
    """
    Checks a single packet against the ordered list of firewall rules.
    The first matching rule determines the action.

    :param packet: The captured Scapy packet object.
    :param rules: The list of firewall rules.
    :return: The action ('ACCEPT' or 'DROP') determined by the ruleset.
    """
    packet_protocol = None
    packet_src_ip = None
    packet_dst_port = None
    
    # Extract IP layer information
    if IP in packet:
        packet_src_ip = packet[IP].src
        packet_dst_ip = packet[IP].dst
        
        if TCP in packet:
            packet_protocol = "TCP"
            packet_dst_port = packet[TCP].dport
        elif UDP in packet:
            packet_protocol = "UDP"
            packet_dst_port = packet[UDP].dport
        else:
            # This handles ICMP, etc., which have an IP layer but no TCP/UDP ports
            packet_protocol = packet[IP].proto
    else:
        # Ignore non-IP traffic (e.g., ARP) for this simple simulation
        return "PASS_THROUGH" 

    # Iterate through rules in order
    for i, rule in enumerate(rules):
        rule_match = True

        # Check Protocol Match
        if rule["PROTOCOL"] != "ANY" and rule["PROTOCOL"] != packet_protocol:
            rule_match = False

        # Check Source IP Match
        if rule_match and rule["SRC_IP"] != "ANY" and rule["SRC_IP"] != packet_src_ip:
            rule_match = False

        # Check Destination Port Match (only for TCP/UDP)
        if rule_match and packet_protocol in ["TCP", "UDP"]:
            if rule["DST_PORT"] != "ANY" and rule["DST_PORT"] != packet_dst_port:
                rule_match = False
        
        # If all criteria match, apply the rule's action and stop checking
        if rule_match:
            return rule["ACTION"]

    # If no rules match (shouldn't happen with a proper default rule)
    return "ACCEPT" 


def process_packet(packet):
    """
    Callback function executed for every sniffed packet.
    """
    action = check_packet_against_rules(packet, FIREWALL_RULES)

    if IP in packet:
        summary = f"[{action:<10}] {packet[IP].src}:{packet.sport if TCP in packet or UDP in packet else ''} -> {packet[IP].dst}:{packet.dport if TCP in packet or UDP in packet else ''} | Proto: {packet.lastlayer().name}"
        
        if action == "DROP":
            print(f"\033[91m{summary}\033[0m") # Print blocked packets in RED
        elif action == "ACCEPT":
            print(f"\033[92m{summary}\033[0m") # Print accepted packets in GREEN
        else:
            print(summary) # Neutral color for PASS_THROUGH (non-IP)
    

def start_firewall(interface: str):
    """
    Starts the packet sniffer on the specified interface.
    """
    print(f"Starting simple firewall simulator on interface: {interface}")
    print("--- Rules Loaded ---")
    for i, rule in enumerate(FIREWALL_RULES):
        print(f"Rule {i+1}: {rule['ACTION']:<6} | Proto: {rule['PROTOCOL']:<4} | Src IP: {rule['SRC_IP']:<15} | Dst Port: {rule['DST_PORT']}")
    print("-" * 30)

    try:
        # Sniff packets and call process_packet for each one
        sniff(iface=interface, prn=process_packet, store=0)
    except OSError as e:
        print("\n[ERROR] Failed to start sniffing. You may need root/admin privileges.")
        print(f"Detail: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Firewall simulation stopped by user.")


if __name__ == "__main__":
    # The interface must be set to your local network card (e.g., 'eth0', 'wlan0', 'en0').
    # You must change this to match your system's interface name.
    
    # Common interface names:
    # Linux: 'eth0', 'wlan0'
    # macOS: 'en0', 'en1'
    # Windows: Look up interface index or name (e.g., 'Ethernet', 'Wi-Fi')

    # Try to determine a common default interface (you might need to adjust this!)
    if sys.platform.startswith('linux'):
        DEFAULT_INTERFACE = 'eth0'
    elif sys.platform == 'darwin': # macOS
        DEFAULT_INTERFACE = 'en0'
    elif sys.platform == 'win32':
        # Windows interfaces are harder to guess; 'Ethernet' or 'Wi-Fi' are common logical names
        DEFAULT_INTERFACE = 'Ethernet' 
    else:
        DEFAULT_INTERFACE = 'lo' # Loopback as a safe default

    print(f"NOTE: Default interface set to '{DEFAULT_INTERFACE}'.")
    print("You might need to update this variable to match your network card (e.g., 'wlan0' or 'en0').")
    print("Use Ctrl+C to stop the simulation.")
    
    start_firewall(interface=DEFAULT_INTERFACE)