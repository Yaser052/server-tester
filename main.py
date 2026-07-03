from fastapi import FastAPI

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
