# TCP Ping Tool

## Purpose

This tool performs TCP ping operations to test connectivity and measure latency to remote hosts. Unlike traditional ICMP ping, TCP ping attempts to establish a TCP connection to a specific port, which is useful for:

-   Testing service availability on specific ports
-   Measuring network latency in environments where ICMP is blocked
-   Resolving and testing all IP addresses (both IPv4 and IPv6) associated with a hostname
-   Gathering detailed latency statistics including percentiles (p50, p90, p99)

## Features

-   Supports both IPv4 and IPv6 addresses
-   Resolves all IP addresses for a given hostname
-   Provides detailed statistics per IP address
-   Calculates min/avg/max/mdev RTT times
-   Shows p50, p90, and p99 percentiles
-   Configurable ping count, interval, and timeout
-   Handles connection failures gracefully

## Installation

1.  Clone the repository:
    
    ```
    git clone https://github.com/yourusername/tcp-ping.git
    cd tcp-ping
    ```
    
2.  Create a virtual environment (recommended):
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
3.  Install dependencies:
    
    ```
    pip install -r requirements.txt
    ```
    

## Usage

### Basic Command Format

```
python tcp_ping.py <hostname/IP> [-p PORT] [-c COUNT] [-i INTERVAL] [-t TIMEOUT]
```

### Arguments

-   `hostname/IP`: Target hostname or IP address (required)
-   `-p, --port`: Target port number (default: 80)
-   `-c, --count`: Number of pings to send per IP (default: 4)
-   `-i, --interval`: Interval between pings in seconds (default: 1.0)
-   `-t, --timeout`: Connection timeout in seconds (default: 2.0)

### Examples

1.  Basic ping to a hostname:
    
    ```
    python tcp_ping.py google.com
    ```
    
2.  Ping specific port:
    
    ```
    python tcp_ping.py google.com -p 443
    ```
    
3.  Increase number of pings:
    
    ```
    python tcp_ping.py google.com -c 10
    ```
    
4.  Change interval and timeout:
    
    ```
    python tcp_ping.py google.com -i 0.5 -t 1.0
    ```
    

### Sample Output

```
python main.py google.com -p 443 -c 10

TCP ping to google.com:443
Resolved IPs: 142.250.199.78
Sending 10 TCP ping probes to each IP

[00:30:30.476] Connected to 142.250.199.78: time=4.44ms
[00:30:31.486] Connected to 142.250.199.78: time=5.66ms
[00:30:32.497] Connected to 142.250.199.78: time=5.21ms
[00:30:33.508] Connected to 142.250.199.78: time=7.24ms
[00:30:34.520] Connected to 142.250.199.78: time=5.26ms
[00:30:35.531] Connected to 142.250.199.78: time=17.12ms
[00:30:36.551] Connected to 142.250.199.78: time=22.33ms
[00:30:37.576] Connected to 142.250.199.78: time=8.40ms
[00:30:38.590] Connected to 142.250.199.78: time=11.49ms
[00:30:39.603] Connected to 142.250.199.78: time=29.71ms

=== TCP ping statistics per IP ===

IP: 142.250.199.78
Sent: 10, Successful: 10, Failed: 0 (0.0% loss)
RTT min/avg/max/mdev = 4.44/11.69/29.71/8.63 ms
Percentiles (p50/p90/p99) = 7.82/23.07/29.05 ms
```

## Requirements

-   Python 3.10 or higher
-   Dependencies listed in requirements.txt

## License

Apache License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
