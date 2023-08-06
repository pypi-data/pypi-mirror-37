# SPDX-License-Identifier: BSD-2-Clause
import logging
from typing import Generator
from collections import namedtuple

import sarge


log = logging.getLogger(__name__)

Dataset = namedtuple("Dataset", ["name"])
Snapshot = namedtuple("Snapshot", ["dataset", "name"])


class ZfsOperationFailed(Exception):
    pass


def run(cmd: str) -> sarge.Pipeline:
    log.debug(f"Run: {cmd}")

    p = sarge.run(cmd, stdout=sarge.Capture(), stderr=sarge.Capture())

    if p.returncode != 0:
        raise ZfsOperationFailed(list(get_out(p.stderr))[0])

    return p


def get_out(out: sarge.Capture, skip_first=False) -> Generator[str, None, None]:
    first_line = True

    while True:
        line = out.readline()

        if not line:
            break

        if skip_first and first_line:
            first_line = False
            continue

        line = line.decode("utf-8")

        # Remove trailing newline.
        line = line.strip()

        yield line


def get_datasets():
    p = run("zfs list -t filesystem -o name")
    return [Dataset(name=line) for line in get_out(p.stdout, skip_first=True)]


def get_snapshots(dataset: Dataset):
    p = run(f"zfs list -r -t snapshot -o name -S creation {dataset.name}")
    snapshots = []
    for line in get_out(p.stdout, skip_first=True):
        _, name = line.split("@")
        snapshots.append(Snapshot(dataset=dataset, name=name))
    return snapshots


def create_snapshot(dataset: Dataset, name: str):
    run(f"zfs snapshot {dataset.name}@{name}")


def destroy_snapshot(snapshot: Snapshot):
    run(f"zfs destroy {snapshot.dataset.name}@{snapshot.name}")
