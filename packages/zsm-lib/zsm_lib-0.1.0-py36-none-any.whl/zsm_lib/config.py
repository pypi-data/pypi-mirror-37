# SPDX-License-Identifier: BSD-2-Clause
from pathlib import Path
import platform

import yaml
from marshmallow import Schema, fields, validate
import marshmallow

from . import zfs


class ValidationError(Exception):
    pass


class DatasetField(fields.String):
    def _deserialize(self, value, attr, data):
        return zfs.Dataset(name=value)

    def _validate(self, value):
        datasets = zfs.get_datasets()

        for dataset in datasets:
            if dataset == value:
                return dataset

        raise marshmallow.ValidationError("Dataset does not exist")


class SnapshotDeltaSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.OneOf(
            choices=["weeks", "days", "hours", "minutes", "seconds"]
        ),
    )
    value = fields.Integer(required=True)


class SnapshotSchema(Schema):
    dataset = DatasetField(required=True)
    name = fields.String(required=True)
    delta = fields.Nested(SnapshotDeltaSchema, required=True)
    retention = fields.Integer(required=True)


class ConfigSchema(Schema):
    snapshots = fields.Nested(SnapshotSchema, many=True, required=True)


def get_platform_path() -> Path:
    system = platform.system()

    if system == "FreeBSD":
        return Path("/usr/local/etc/")

    if system == "Linux":
        return Path("/etc/")


def get_path() -> Path:
    return get_platform_path() / "zsm.yaml"


def load(data: str) -> dict:
    try:
        data = yaml.safe_load(data)

    except yaml.YAMLError as e:
        msg = "Invalid YAML"

        problem = getattr(e, "problem", None)
        if problem is not None:
            msg += f": {e.problem}"

        problem_mark = getattr(e, "problem_mark", None)
        if problem_mark is not None:
            msg += (
                f": line={e.problem_mark.line + 1} column={e.problem_mark.column + 1}"
            )

        raise ValidationError(msg)

    try:
        data = ConfigSchema().load(data)

    except marshmallow.ValidationError as e:
        raise ValidationError(e.messages)

    return data
