#!/usr/bin/env python3
"""
Run this file once: python setup_project.py
It creates a folder called "port-scanner" containing every project file.
Then open that folder in VS Code (File > Open Folder) or run: code port-scanner
"""

from pathlib import Path

FOLDER = Path("port-scanner")

FILES = {
    'portscanner.py': r'''#!/usr/bin/env python3
"""
Simple multithreaded TCP port scanner.

Only scan hosts you own or have explicit permission to test.
"""

import argparse
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def parse_ports(port_arg: str) -> list[int]:
    """Turn '22,80,1000-1010' into a sorted list of unique ports."""
    ports = set()
    for part in port_arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        elif part:
            ports.add(int(part))
    invalid = [p for p in ports if not 1 <= p <= 65535]
    if invalid:
        raise ValueError(f"Ports must be between 1 and 65535: {invalid[:5]}")
    return sorted(ports)


def scan_port(host: str, port: int, timeout: float, grab_banner: bool):
    """Try to connect to one port. Returns (port, service, banner) if open, else None."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((host, port)) != 0:
                return None

            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "unknown"

            banner = ""
            if grab_banner:
                try:
                    sock.sendall(b"\r\n")
                    banner = sock.recv(1024).decode(errors="ignore").strip()
                    banner = banner.splitlines()[0] if banner else ""
                except OSError:
                    pass
            return port, service, banner
    except OSError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Ports to scan, e.g. 80,443 or 1-1000 (default: 1-1024)")
    parser.add_argument("-t", "--timeout", type=float, default=0.5,
                        help="Seconds to wait per port (default: 0.5)")
    parser.add_argument("-w", "--workers", type=int, default=100,
                        help="Number of threads (default: 100)")
    parser.add_argument("-b", "--banner", action="store_true",
                        help="Try to grab a service banner from open ports")
    args = parser.parse_args()

    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        sys.exit(f"Error: {e}")

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        sys.exit(f"Error: could not resolve '{args.target}'")

    print(f"Scanning {args.target} ({ip}) - {len(ports)} ports")
    start = time.time()

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(scan_port, ip, p, args.timeout, args.banner)
                       for p in ports]
            results = [f.result() for f in futures]
    except KeyboardInterrupt:
        sys.exit("\nScan cancelled.")

    open_ports = [r for r in results if r]
    print(f"\n{'PORT':<8}{'SERVICE':<15}BANNER")
    print("-" * 45)
    for port, service, banner in open_ports:
        print(f"{port:<8}{service:<15}{banner}")

    print(f"\n{len(open_ports)} open port(s) found in {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
''',

    'README.md': r'''# Python Port Scanner

A simple multithreaded TCP port scanner written in pure Python (standard library only). Built as a beginner project to learn about sockets, threading, and how network services work.

## Features

- Scan single ports, lists, or ranges (`80`, `22,80,443`, `1-1000`)
- Multithreaded for fast scans
- Identifies common services (HTTP, SSH, etc.)
- Optional banner grabbing
- Adjustable timeout and thread count
- No dependencies. Python 3.9+

## Usage

```bash
python portscanner.py <target> [-p PORTS] [-t TIMEOUT] [-w WORKERS] [-b]
```

Examples:

```bash
# Scan the default range (1-1024) on your own machine
python portscanner.py 127.0.0.1

# Scan specific ports with banner grabbing
python portscanner.py 192.168.1.1 -p 22,80,443 -b

# Scan a wider range with a longer timeout
python portscanner.py scanme.nmap.org -p 1-5000 -t 1
```

Sample output:

```
Scanning 127.0.0.1 (127.0.0.1) - 1024 ports

PORT    SERVICE        BANNER
---------------------------------------------
22      ssh            SSH-2.0-OpenSSH_9.6
80      http

2 open port(s) found in 1.84s
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --ports` | Ports to scan | `1-1024` |
| `-t, --timeout` | Seconds to wait per port | `0.5` |
| `-w, --workers` | Number of threads | `100` |
| `-b, --banner` | Grab service banners | off |

## How it works

For each port, the scanner opens a TCP socket and calls `connect_ex()`. A return value of `0` means the connection succeeded, so the port is open. A thread pool runs many of these checks at once, which makes scanning much faster than doing them one by one.

## Legal and ethical use

Only scan systems you own or have **explicit written permission** to test. Unauthorized scanning may be illegal in your country. For safe practice, use your own machine (`127.0.0.1`), a home lab, or `scanme.nmap.org` (light scans only, per Nmap's policy).

## Ideas for improvement

- UDP scanning
- Export results to JSON or CSV
- Progress bar
- Scan multiple hosts / CIDR ranges
- Simple GUI or web front end

## License

MIT
''',

    '.gitignore': r'''__pycache__/
*.pyc
.venv/
venv/
.idea/
.vscode/
.DS_Store
''',

}


def main():
    FOLDER.mkdir(exist_ok=True)
    for name, content in FILES.items():
        path = FOLDER / name
        path.write_text(content, encoding="utf-8")
        print(f"Created {path}")
    print("\nDone! Open the 'port-scanner' folder in VS Code.")


if __name__ == "__main__":
    main()
