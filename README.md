# Python Port Scanner

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
