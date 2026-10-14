FROM qa-agent-server:acca181a-local-uid
ENTRYPOINT ["python", "-c", "import time; time.sleep(600)"]
