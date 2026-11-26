import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "generate_entity_map", ROOT / "scripts" / "generate_entity_map.py")
generate_entity_map = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(generate_entity_map)


def test_entity_map_command_delegates_to_the_publication_model_renderer():
    assert generate_entity_map.main.__module__ == "render_publication_assets"
