FROM qa-agent-server:acca181a-local-pricing
RUN mv /workspace/agent-sdk-verify /agent-server
ENV PATH=/agent-server/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHONPATH=/agent-server/openhands-sdk:/agent-server/openhands-tools:/agent-server/openhands-workspace:/agent-server/openhands-agent-server
WORKDIR /agent-server
ENTRYPOINT ["/agent-server/.venv/bin/python", "-m", "openhands.agent_server"]
