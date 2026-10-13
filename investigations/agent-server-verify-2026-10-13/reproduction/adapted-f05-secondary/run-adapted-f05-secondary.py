"""Replay an isolated F05 recipe copy with the unmodified repository CLI."""

import importlib.util
import pathlib
import sys

original = pathlib.Path('/workspace/agent-sdk-verify/.agents/skills/verify-agent-server/scripts/control_agent_server.py')
spec = importlib.util.spec_from_file_location('verify_agent_server_adapted_f05_secondary', original)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
module.FEATURE_MAP_DIR = pathlib.Path(__file__).parent / 'feature-map'
sys.exit(module.main())
