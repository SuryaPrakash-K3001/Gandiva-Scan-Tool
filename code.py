import socket
import sys
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def scan_port(ip, port):
    """Scans a single port to check if it's open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set timeout for the connection attempt
            result = s.connect_ex((ip, port))
            if result == 0:
                return port
    except socket.error:
        pass
    return None


def scan_ports(ip, start_port, end_port, max_threads=50):
    """Scans ports in a specified range."""
    open_ports = []
    with ThreadPoolExecutor(max_threads) as executor:
        results = executor.map(lambda port: scan_port(ip, port), range(start_port, end_port + 1))
        for port in results:
            if port:
                open_ports.append(port)
    return open_ports


def save_report(ip, open_ports, output_file):
    """Saves the scan report to a file."""
    try:
        with open(output_file, 'w') as f:
            f.write(f"Port Scan Report for {ip}\n")
            f.write(f"Scan started at: {datetime.now()}\n\n")
            if open_ports:
                f.write("Open Ports:\n")
                for port in open_ports:
                    f.write(f"Port {port} is open.\n")
            else:
                f.write("No open ports found.\n")
            f.write("\nScan completed at: {}\n".format(datetime.now()))
        print(f"Report saved to {output_file}")
    except Exception as e:
        print(f"Error saving report: {e}")


def main():
    """Main function to handle argument parsing and scanning."""
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("ip", help="IP address to scan")
    parser.add_argument("start_port", type=int, help="Starting port number")
    parser.add_argument("end_port", type=int, help="Ending port number")
    parser.add_argument("--report", help="Path to save the scan report", default="scan_report.txt")
    args = parser.parse_args()

    ip = args.ip
    start_port = args.start_port
    end_port = args.end_port
    output_file = args.report

    print(f"Starting scan on {ip} from port {start_port} to port {end_port}")
    start_time = datetime.now()
    open_ports = scan_ports(ip, start_port, end_port)
    end_time = datetime.now()

    if open_ports:
        print("\nOpen Ports:")
        for port in open_ports:
            print(f"Port {port} is open.")
    else:
        print("\nNo open ports found.")

    print(f"\nScan completed in: {end_time - start_time}")
    save_report(ip, open_ports, output_file)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python port_scanner.py <IP> <Start Port> <End Port> --report <Output File>")
    else:
        main()
