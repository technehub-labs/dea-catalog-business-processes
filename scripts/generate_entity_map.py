#!/usr/bin/env python3
"""Render the ECF poster and offline catalogue from a publication model.

Build the JSON first with scripts/build_publication_model.py. This command
never reads canonical entity YAML; all publication semantics and provenance
come from the validated model.

    python scripts/generate_entity_map.py --model out/process-catalogue.json \
      --output-dir out --pdf --png
"""
from __future__ import annotations

from render_publication_assets import main


if __name__ == "__main__":
    raise SystemExit(main())
