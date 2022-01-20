from typing import Dict, List
import simplejson as json

import requests


class Config:
    ingest_url: str

    def __init__(
        self,
        *,
        ingest_host: str = "http://localhost:5000",
        # Delay sending track events over the network until `flush` is called.
        buffered: bool = False,
        # Maximum number of buffered events before `flush` will be called
        # automatically to avoid an overflow.
        max_buffer_size: int = 100,
        # Don't emit any events to the ingest host. Tracks will still work and
        # be buffered, but no HTTP calls will be made.
        no_emit: bool = False,
        # Use the `test_path` endpoint instead of actually ingesting events.
        test_mode: bool = False,
        path: str = "/track",
        test_path: str = "/test",
        latest_path: str = "/latest",
    ):
        self.ingest_host = ingest_host
        self.buffered = buffered
        self.max_buffer_size = max_buffer_size
        self.path = path
        self.latest_path = latest_path
        self.test_path = test_path
        self.test_mode = test_mode
        self.no_emit = no_emit

        resolved_path = test_path if test_mode else path
        self.ingest_url = f"{ingest_host}{resolved_path}"


config = Config()


def set_config(new_config: Config):
    global config
    config = new_config


EVENT_BUFFER = []


def track(event_name: str, data: Dict):
    """Track a single analytics event.

    If `config.buffered` is set, the event won't be sent immediately, but rather
    in a batch with any other pending events when `flush` is called.
    """
    event_content = {"event_name": str(event_name), "properties": data}
    if not config.buffered:
        _send_track([event_content])
        return

    EVENT_BUFFER.append(event_content)
    if len(EVENT_BUFFER) >= config.max_buffer_size:
        flush()


def flush():
    """Send all buffered events to the ingest server."""
    _send_track(EVENT_BUFFER)
    EVENT_BUFFER.clear()


def get_latest():
    return requests.get(f"{config.ingest_host}{config.latest_path}").json()


def _send_track(events: List[Dict]):
    if config.no_emit:
        return None

    return requests.post(
        config.ingest_url,
        data=_serialize(events),
        headers={"Content-Type": "application/json"},
    )


def _serialize(data):
    return json.dumps(data, use_decimal=True)
