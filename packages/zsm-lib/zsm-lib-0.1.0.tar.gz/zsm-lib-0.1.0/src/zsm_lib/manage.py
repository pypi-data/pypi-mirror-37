# SPDX-License-Identifier: BSD-2-Clause
from typing import Iterable

import logging
import datetime

from . import zfs


log = logging.getLogger(__name__)

SNAPSHOT_DELIMITER = "_"
SNAPSHOT_PREFIX = "zsm"
SNAPSHOT_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_snapshots(dataset: zfs.Dataset, subname: str) -> Iterable[zfs.Snapshot]:
    snapshots = zfs.get_snapshots(dataset=dataset)

    return list(
        filter(
            lambda snapshot: snapshot.name.startswith(
                SNAPSHOT_DELIMITER.join([SNAPSHOT_PREFIX, subname])
            ),
            snapshots,
        )
    )


def create_snapshot(dataset: zfs.Dataset, subname: str):
    timestamp = datetime.datetime.now().strftime(SNAPSHOT_TIMESTAMP_FORMAT)
    zfs.create_snapshot(
        dataset=dataset,
        name=SNAPSHOT_DELIMITER.join([SNAPSHOT_PREFIX, subname, timestamp]),
    )


def parse_snapshot(snapshot: zfs.Snapshot):
    _, subname, timestamp = snapshot.name.split("_")
    timestamp = datetime.datetime.strptime(timestamp, SNAPSHOT_TIMESTAMP_FORMAT)
    return subname, timestamp


def manage_snapshots(config, now: datetime.datetime, dry_run: bool) -> None:
    for snapshot_config in config["snapshots"]:
        create_snapshots(
            now=now,
            dataset=snapshot_config["dataset"],
            subname=snapshot_config["name"],
            delta_name=snapshot_config["delta"]["name"],
            delta_value=snapshot_config["delta"]["value"],
            dry_run=dry_run,
        )

    for snapshot_config in config["snapshots"]:
        destroy_snapshots(
            dataset=snapshot_config["dataset"],
            subname=snapshot_config["name"],
            retention=snapshot_config["retention"],
            dry_run=dry_run,
        )


def create_snapshots(
    now: datetime.datetime,
    dataset: zfs.Dataset,
    subname: str,
    delta_name: str,
    delta_value: int,
    dry_run: bool,
) -> None:
    snapshots = get_snapshots(dataset=dataset, subname=subname)

    if len(snapshots) == 0:
        log.info(
            f"[{dataset.name}:{subname}] No snapshots yet, creating the first one."
        )

        if not dry_run:
            create_snapshot(dataset=dataset, subname=subname)

    else:
        latest_snapshot = snapshots[0]
        _, latest_timestamp = parse_snapshot(snapshot=latest_snapshot)
        latest_age = now - latest_timestamp

        if latest_age > datetime.timedelta(**{delta_name: delta_value}):
            log.info(
                f"[{dataset.name}:{subname}] "
                f"Latest snapshot ({latest_snapshot.name}) is {latest_age} old, "
                "creating new."
            )

            if not dry_run:
                create_snapshot(dataset=dataset, subname=subname)

        else:
            log.info(
                f"[{dataset.name}:{subname}] "
                f"Latest snapshot ({latest_snapshot.name}) is only {latest_age} old, "
                "skipping."
            )


def destroy_snapshots(
    dataset: zfs.Dataset, subname: str, retention: int, dry_run: bool
) -> None:
    any_old_found = False

    while True:
        snapshots = get_snapshots(dataset=dataset, subname=subname)

        if len(snapshots) > retention:
            oldest_snapshot = snapshots[-1]

            log.info(
                f"[{dataset.name}:{subname}] "
                f"Found old snapshot ({oldest_snapshot.name}), destroying it."
            )

            if not dry_run:
                zfs.destroy_snapshot(snapshot=oldest_snapshot)

            any_old_found = True

        else:
            break

    if not any_old_found:
        log.info(f"[{dataset.name}:{subname}] There are no old snapshots to destroy.")
