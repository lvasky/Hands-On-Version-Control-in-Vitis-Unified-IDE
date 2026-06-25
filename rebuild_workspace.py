#!/usr/bin/env python3
"""
Rebuild this Vitis workspace from source-controlled inputs.

Usage:
    vitis -s rebuild_workspace.py
    vitis -s rebuild_workspace.py --force
    

Default mode opens the workspace and builds existing components. Use --force
when generated platform/application files were intentionally omitted from Git
and Vitis cannot build the partially restored component directories.

Refer to ./logs/builder.py to modify Workspace configurations
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

import vitis

# Workspace configurations
WORKSPACE = Path(__file__).resolve().parent
PLATFORM_NAME = "platform"
APP_NAME = "hello_world"
DOMAIN_NAME = "standalone_psu_cortexa53_0"
CPU_NAME = "psu_cortexa53_0"
OS_NAME = "standalone"
APP_TEMPLATE = "hello_world"

PLATFORM_DIR = WORKSPACE / PLATFORM_NAME
PLATFORM_HW_DIR = PLATFORM_DIR / "hw"
APP_DIR = WORKSPACE / APP_NAME
APP_SRC_DIR = APP_DIR / "src"


def as_vitis_path(path: Path) -> str:
    return path.resolve().as_posix()


def find_xsa() -> Path:
    xsa_files = sorted(PLATFORM_HW_DIR.glob("*.xsa"))
    if len(xsa_files) != 1:
        found = ", ".join(str(path) for path in xsa_files) or "none"
        raise RuntimeError(
            f"Expected exactly one XSA under {PLATFORM_HW_DIR}, found: {found}"
        )
    return xsa_files[0]


def platform_xpfm() -> Path:
    return PLATFORM_DIR / "export" / PLATFORM_NAME / f"{PLATFORM_NAME}.xpfm"


def remove_component_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def recreate_components(client) -> None:
    with tempfile.TemporaryDirectory(prefix="vitis_rebuild_") as temp_name:
        temp_dir = Path(temp_name)
        saved_xsa = temp_dir / find_xsa().name
        saved_src = temp_dir / "app_src"

        shutil.copy2(find_xsa(), saved_xsa)
        if APP_SRC_DIR.exists():
            shutil.copytree(APP_SRC_DIR, saved_src)

        remove_component_dir(APP_DIR)
        remove_component_dir(PLATFORM_DIR)

        platform = client.create_platform_component(
            name=PLATFORM_NAME,
            hw_design=as_vitis_path(saved_xsa),
            os=OS_NAME,
            cpu=CPU_NAME,
        )
        platform.build()

        comp = client.create_app_component(
            name=APP_NAME,
            platform=as_vitis_path(platform_xpfm()),
            domain=DOMAIN_NAME,
            template=APP_TEMPLATE,
        )

        if saved_src.exists():
            remove_component_dir(APP_SRC_DIR)
            shutil.copytree(saved_src, APP_SRC_DIR)

        comp = client.get_component(name=APP_NAME)
        comp.build()


def build_existing_components(client) -> None:
    platform = client.get_platform_component(name=PLATFORM_NAME)
    platform.build()

    comp = client.get_component(name=APP_NAME)
    comp.build()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild the platform and hello_world Vitis components."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="recreate generated component directories before building",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    client = vitis.create_client()
    try:
        client.set_workspace(path=as_vitis_path(WORKSPACE))
        if args.force:
            recreate_components(client)
        else:
            build_existing_components(client)
    finally:
        vitis.dispose()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
