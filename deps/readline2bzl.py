#!/usr/bin/env python3

"""Script to help build readline with bazel."""

import argparse
import re
from pathlib import Path
from string import Template
from textwrap import indent
from typing import Set, Tuple

MATCH_FILES = re.compile(r"(?P<files>[\w]+\.\w+)")
MATCH_VARS = re.compile(r"\$\((?P<vars>[\w]+)\)")


BUILD_TEMPLATE = Template(
    """\
# Auto-generated with readline2bzl.py; do not edit.
cc_library(
    name = "readline",
    # Readline uses -I., so the headers aren't
    # properly checked. This results in outdated
    # makfile contents, so we use glob() instead.
    srcs = glob(["*.h"]) + [
${srcs}
    ],
    # INSTALLED_HEADERS
    hdrs = [
${hdrs}
    ],
    local_defines = [
        "HAVE_CONFIG_H",
        "READLINE_LIBRARY",
    ],
    includes = [
        ".",
    ],
    visibility = ["//visibility:public"],
)
"""
)


def main() -> None:
    """Produce a readline.bzl file that can build the readline project."""
    parser = argparse.ArgumentParser()
    parser.add_argument("makefile", type=Path)
    parser.add_argument("outfile", type=argparse.FileType("w"))
    args = parser.parse_args()

    srcs, hdrs = extract_file_lists(args.makefile)
    args.outfile.write(make_build_file(srcs, hdrs))


def make_build_file(srcs: Set[str], hdrs: Set[str]) -> str:
    """Create a build file that includes the given srcs and hdrs.."""
    srcs_string = indent("\n".join(f'"{src}",' for src in sorted(srcs)), " " * 8)
    hdrs_string = indent("\n".join(f'"{hdr}",' for hdr in sorted(hdrs)), " " * 8)

    return BUILD_TEMPLATE.substitute(srcs=srcs_string, hdrs=hdrs_string)


def extract_file_lists(makefile: Path) -> Tuple[Set[str], Set[str]]:
    """Extract file lists for srcs and hdrs."""
    with makefile.open() as f:
        contents = f.read()

    # Remove all multi-line definitions for ease of parsing
    contents = contents.replace("\\\n", "")

    objs = extract_files_recursively("OBJECTS", contents)

    return (
        extract_object_deps(objs, contents),
        extract_files_recursively("INSTALLED_HEADERS", contents),
    )


def extract_files_recursively(var: str, string: str) -> Set[str]:
    """Recursively extract the list of files assigned to a variable."""
    match = re.search(f"^{var} =(.*)$", string, flags=re.MULTILINE)
    assert match, "Invalid make file"

    line = match.group(1)

    variables = re.findall(MATCH_VARS, line)
    files = set(re.findall(MATCH_FILES, line))

    for variable in variables:
        files = files.union(extract_files_recursively(variable, string))

    return files


def extract_object_deps(objs: Set[str], string: str) -> Set[str]:
    """Extract the dependencies of the given set of objects."""
    srcs: Set[str] = set()

    for obj in objs:
        rules = re.findall(f"^{obj}: (.*)$", string, flags=re.MULTILINE)
        for rule in rules:
            srcs = srcs.union(
                filter(lambda f: f.endswith(".c"), set(re.findall(MATCH_FILES, rule)))
            )

    return srcs


if __name__ == "__main__":
    main()
