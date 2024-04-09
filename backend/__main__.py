import uvicorn
from config import config

if __name__ == "__main__":
    uvicorn.run("backend.server:app",
                host=config.server_host,
                port=config.server_port,
                reload=True)
