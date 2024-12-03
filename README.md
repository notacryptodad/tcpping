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
    
    Copy
    
    ```
    git clone https://github.com/yourusername/tcp-ping.git
    cd tcp-ping
    
    ```
    
2.  Create a virtual environment (recommended):
    
    Copy
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    ```
    
3.  Install dependencies:
    
    basic
    
    Copy
    
    ```
    pip install -r requirements.txt
    
    ```
    

## Usage

### Basic Command Format

scheme

Copy

```
```
python tcp_ping.py <hostname/IP> [-p PORT] [-c COUNT] [-i INTERVAL] [-t TIMEOUT]
```

```

### Arguments

-   `hostname/IP`: Target hostname or IP address (required)
-   `-p, --port`: Target port number (default: 80)
-   `-c, --count`: Number of pings to send per IP (default: 4)
-   `-i, --interval`: Interval between pings in seconds (default: 1.0)
-   `-t, --timeout`: Connection timeout in seconds (default: 2.0)

### Examples

1.  Basic ping to a hostname:
    
    Copy
    
    ```
    python tcp_ping.py google.com
    
    ```
    
2.  Ping specific port:
    
    Copy
    
    ```
    python tcp_ping.py google.com -p 443
    
    ```
    
3.  Increase number of pings:
    
    Copy
    
    ```
    python tcp_ping.py google.com -c 10
    
    ```
    
4.  Change interval and timeout:
    
    Copy
    
    ```
    python tcp_ping.py google.com -i 0.5 -t 1.0
    
    ```
    

### Sample Output

gradle

Copy

```
```
TCP ping to google.com:80
Resolved IPs: 142.250.72.78, 2404:6800:4008:c07::67
Sending 4 TCP ping probes to each IP

[10:15:20.123] Connected to 142.250.72.78: time=45.32ms
[10:15:20.124] Connected to 2404:6800:4008:c07::67: time=45.67ms
...

=== TCP ping statistics per IP ===

IP: 142.250.72.78
Sent: 4, Successful: 4, Failed: 0 (0.0% loss)
RTT min/avg/max/mdev = 45.32/46.21/47.11/0.54 ms
Percentiles (p50/p90/p99) = 46.15/47.01/47.11 ms

IP: 2404:6800:4008:c07::67
Sent: 4, Successful: 4, Failed: 0 (0.0% loss)
RTT min/avg/max/mdev = 45.67/46.54/47.43/0.58 ms
Percentiles (p50/p90/p99) = 46.48/47.33/47.43 ms
```

```

## Requirements

-   Python 3.6 or higher
-   Dependencies listed in requirements.txt

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
