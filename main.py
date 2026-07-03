from fastapi import FastAPI
import socket
import time

app = FastAPI()


@app.get("/")
def home():
    try:
        with open("servers.txt", "r") as f:
            servers = [line.strip() for line in f if line.strip()]

        return {
            "status": "running",
            "servers_found": len(servers),
            "first_server": servers[0] if servers else "No servers found"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/scan")
def scan_servers():
    results = []

    try:
        with open("servers.txt", "r") as f:
            servers = [line.strip() for line in f if line.strip()]

        subscribe = (
            '{"id":1,"method":"mining.subscribe","params":[]}\n'
        ).encode()

        for server in servers:
            try:
                host, port = server.split(":")
                port = int(port)

                sock = socket.create_connection(
                    (host, port),
                    timeout=5
                )

                sock.settimeout(5)

                start = time.time()

                sock.sendall(subscribe)

                response = sock.recv(4096)

                elapsed = round(
                    (time.time() - start) * 1000,
                    2
                )

                sock.close()

                if response:
                    results.append({
                        "server": server,
                        "stratum_ms": elapsed
                    })

            except Exception:
                pass

        results.sort(
            key=lambda x: x["stratum_ms"]
        )

        return {
            "servers_tested": len(servers),
            "stratum_online": len(results),
            "best_server": results[0] if results else None,
            "top_10": results[:10]
        }

    except Exception as e:
        return {
            "error": str(e)
        }
