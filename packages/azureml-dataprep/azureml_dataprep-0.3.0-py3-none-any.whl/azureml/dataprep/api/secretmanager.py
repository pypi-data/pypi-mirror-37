# Copyright (c) Microsoft Corporation. All rights reserved.
from .engineapi.typedefinitions import Secret, RegisterSecretMessageArguments
from .engineapi.api import get_engine_api
from typing import Dict, List
import uuid


def register_secrets(secrets: Dict[str, str]) -> List[Secret]:
    return [register_secret(value, sid) for sid, value in secrets.items()]


def register_secret(value: str, id: str = None) -> Secret:
    id = id if id is not None else str(uuid.uuid4())
    return get_engine_api().register_secret(RegisterSecretMessageArguments(id, value))


def create_secret(id: str) -> Secret:
    return Secret(id)
