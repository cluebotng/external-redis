#!/usr/bin/env python3
import json
import os
import sys
from dataclasses import dataclass
from pathlib import PosixPath
from typing import Optional, List, Union, Dict, Any


def write_config(config_path: PosixPath) -> None:
    config = {
        'bind': '*',
        'protected-mode': 'no',
        'port': 6379,
        'tcp-backlog': 511,
        'timeout': 0,
        'tcp-keepalive': 300,
        'loglevel': 'verbose',
        'logfile': '',
        'databases': 16,
        'always-show-logo': 'yes',
        'save': '',
        'dir': '/tmp',
        'io-threads': 1,
        'jemalloc-bg-thread': 'yes',
    }

    if raw_user_config := os.environ.get("REDIS_CONFIG"):
        user_config = json.loads(raw_user_config)
        config |= user_config

    config['requirepass'] = os.environ.get("REDIS_PASSWORD")
    if not config['requirepass']:
        raise RuntimeError("No REDIS_PASSWORD set")

    with config_path.open('w') as fh:
        for k, v in config.items():
            fh.write(f'{k} {v}\n')


def run_redis(config_path: PosixPath):
    # Note: We replace the current process, rather than running as a sub-process
    return os.execv("/layers/heroku_deb-packages/packages/usr/bin/redis-server",
                    ["redis-server", config_path.as_posix()])


def main():
    config_path = PosixPath("/tmp/redis.conf")
    write_config(config_path)
    run_redis(config_path)


if __name__ == "__main__":
    main()
