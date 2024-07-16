import uvicorn

from views import *

if __name__ == "__main__":
    try:
        uvicorn.run(app, host='localhost', port=8001)
    except KeyboardInterrupt:
        print("Server is shutting down...")
