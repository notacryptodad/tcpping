# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.    

import socket
import time
import sys
import statistics
from datetime import datetime
import argparse
from typing import Optional, List, Dict
import numpy as np
from collections import defaultdict
import dns.resolver

class TCPPinger:
    def __init__(self, target: str, port: int = 80, timeout: float = 2.0):
        """
        Initialize TCP Pinger
        
        Args:
            target: Target hostname or IP address
            port: Target port number
            timeout: Socket timeout in seconds
        """
        self.target = target
        self.port = port
        self.timeout = timeout
        self.resolved_ips = set()

    def resolve_hostname(self) -> List[str]:
        """
        Resolve hostname to get all associated IP addresses
        """
        try:
            # Try to parse as IP address first
            socket.inet_aton(self.target)
            self.resolved_ips = {self.target}
            return list(self.resolved_ips)
        except socket.error:
            # If not an IP address, resolve hostname
            try:
                # Get IPv4 addresses
                answers_a = dns.resolver.resolve(self.target, 'A')
                for answer in answers_a:
                    self.resolved_ips.add(answer.to_text())
                
                # Try to get IPv6 addresses
                try:
                    answers_aaaa = dns.resolver.resolve(self.target, 'AAAA')
                    for answer in answers_aaaa:
                        self.resolved_ips.add(answer.to_text())
                except dns.resolver.NoAnswer:
                    pass
                
                return list(self.resolved_ips)
            except dns.resolver.NXDOMAIN:
                print(f"Could not resolve hostname: {self.target}")
                return []
            except Exception as e:
                print(f"Error resolving hostname: {e}")
                return []

    def ping_once(self, ip: str) -> Optional[float]:
        """
        Perform a single TCP ping
        
        Returns:
            Round trip time in milliseconds if successful, None if failed
        """
        try:
            # Choose socket type based on IP version
            if ':' in ip:  # IPv6
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            else:  # IPv4
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
            sock.settimeout(self.timeout)
            
            start_time = time.time()
            result = sock.connect_ex((ip, self.port))
            end_time = time.time()
            
            sock.close()
            
            if result == 0:
                return (end_time - start_time) * 1000  # Convert to milliseconds
            return None
            
        except socket.error as e:
            return None
        finally:
            try:
                sock.close()
            except:
                pass

    def calculate_percentiles(self, times: List[float]) -> Dict[str, float]:
        """
        Calculate percentiles (p50, p90, p99) from a list of times
        """
        if not times:
            return {'p50': 0, 'p90': 0, 'p99': 0}
        
        return {
            'p50': np.percentile(times, 50),
            'p90': np.percentile(times, 90),
            'p99': np.percentile(times, 99)
        }

    def ping(self, count: int = 4, interval: float = 1.0):
        """
        Perform multiple TCP pings to all resolved IPs
        
        Args:
            count: Number of pings to perform per IP
            interval: Time between pings in seconds
        """
        ips = self.resolve_hostname()
        if not ips:
            return

        print(f"\nTCP ping to {self.target}:{self.port}")
        print(f"Resolved IPs: {', '.join(ips)}")
        print(f"Sending {count} TCP ping probes to each IP\n")

        # Store results for each IP
        results = defaultdict(lambda: {'successful': [], 'failed': 0})

        try:
            for i in range(count):
                for ip in ips:
                    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    result = self.ping_once(ip)
                    
                    if result is not None:
                        results[ip]['successful'].append(result)
                        print(f"[{timestamp}] Connected to {ip}: time={result:.2f}ms")
                    else:
                        results[ip]['failed'] += 1
                        print(f"[{timestamp}] Failed to connect to {ip}")

                if i < count - 1:  # Don't sleep after the last ping
                    time.sleep(interval)

        except KeyboardInterrupt:
            print("\nPing interrupted by user")

        # Print statistics for each IP
        print("\n=== TCP ping statistics per IP ===")
        
        for ip in ips:
            successful_pings = results[ip]['successful']
            failed_pings = results[ip]['failed']
            total_pings = len(successful_pings) + failed_pings

            print(f"\nIP: {ip}")
            print(f"Sent: {total_pings}, Successful: {len(successful_pings)}, "
                  f"Failed: {failed_pings} "
                  f"({(failed_pings/total_pings*100):.1f}% loss)")

            if successful_pings:
                percentiles = self.calculate_percentiles(successful_pings)
                print(f"RTT min/avg/max/mdev = "
                      f"{min(successful_pings):.2f}/"
                      f"{statistics.mean(successful_pings):.2f}/"
                      f"{max(successful_pings):.2f}/"
                      f"{statistics.stdev(successful_pings) if len(successful_pings) > 1 else 0:.2f} ms")
                print(f"Percentiles (p50/p90/p99) = "
                      f"{percentiles['p50']:.2f}/"
                      f"{percentiles['p90']:.2f}/"
                      f"{percentiles['p99']:.2f} ms")

def main():
    parser = argparse.ArgumentParser(description='TCP Ping Tool with IP Resolution')
    parser.add_argument('target', help='Target hostname or IP address')
    parser.add_argument('-p', '--port', type=int, default=80,
                       help='Target port number (default: 80)')
    parser.add_argument('-c', '--count', type=int, default=4,
                       help='Number of pings to send per IP (default: 4)')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                       help='Interval between pings in seconds (default: 1.0)')
    parser.add_argument('-t', '--timeout', type=float, default=2.0,
                       help='Timeout in seconds (default: 2.0)')

    args = parser.parse_args()

    pinger = TCPPinger(args.target, args.port, args.timeout)
    pinger.ping(args.count, args.interval)

if __name__ == "__main__":
    main()