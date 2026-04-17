from __future__ import annotations

import argparse
import sys
from importlib import resources
from pathlib import Path


DEFAULT_IMAGE = "sinnet.jpg"
RACCHETTA_IMAGE = "racchetta.jpg"
PALLINA_IMAGE = "pallina.jpg"


def resolve_image_name(args: argparse.Namespace) -> str:
    if args.racchetta:
        return RACCHETTA_IMAGE
    if args.pallina:
        return PALLINA_IMAGE
    return DEFAULT_IMAGE


def resolve_target_dir(servizio_path: str | None) -> Path:
    target = Path(servizio_path).expanduser() if servizio_path else Path.cwd()

    if target.exists() and not target.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {target}")

    target.mkdir(parents=True, exist_ok=True)
    return target


def copy_image(image_name: str, target_dir: Path, overwrite: bool = False) -> Path:
    """Copy one packaged image into target_dir and return destination path."""
    destination = target_dir / image_name

    if destination.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {destination}")

    source = resources.files("tennis.assets").joinpath(image_name)
    destination.write_bytes(source.read_bytes())
    return destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tennis",
        description="Save sinnet.jpg, racchetta.jpg, or pallina.jpg.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-racchetta",
        "--racchetta",
        action="store_true",
        help="save racchetta.jpg",
    )
    group.add_argument(
        "-pallina",
        "--pallina",
        action="store_true",
        help="save pallina.jpg",
    )

    parser.add_argument(
        "-servizio",
        "--servizio",
        metavar="PATH",
        help="destination directory path (default: current directory)",
    )
    parser.add_argument(
        "-matchpoint",
        "--matchpoint",
        action="store_true",
        help="overwrite destination image if it already exists",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        image_name = resolve_image_name(args)
        target_dir = resolve_target_dir(args.servizio)
        output_path = copy_image(image_name, target_dir, overwrite=args.matchpoint)
    except FileExistsError as err:
        print(err, file=sys.stderr)
        print("Use --matchpoint to overwrite.", file=sys.stderr)
        return 1
    except NotADirectoryError as err:
        print(err, file=sys.stderr)
        return 1
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        print("Missing packaged image asset.", file=sys.stderr)
        return 1

    print(f"Tennis! Created: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
