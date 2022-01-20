# GDQ Analytics Client

This is a Python package for emitting analytics events from the GDQ Donation Tracker and any other source that would like to be tracked.

This library does not do any tracking itself, but rather provides an interface for sending events to another server over HTTP.

This library also does not currently do any validation on the response from the ingest server.

## Configuration

The `Config` class in this package exposes a number of properties that can change the behavior of the client.

```python
# The URL of the event ingest server.
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
# Path for the primary ingestion endpoint. e.g., `hostname.com/track`
path: str = "/track",
# Path for ingesting events when in test mode.
test_path: str = "/test",
# Path for retrieving statistics on events from the ingestion server.
latest_path: str = "/latest",
```

To set this configuration, create a new instance of `Config` and pass it to the `set_config` method in this package.

## Usage

```python
import analytics

analytics.set_config(analytics.Config(test_mode=True))

analytics.track('donation_received', {'amount': 25.00, 'donor_id': 111111})
```

### Buffering

By default, every event will immediately be sent over the network to the ingest server. This can be really inefficient, so the package also supports buffering events to be sent in batches.

When buffering events, be sure to call `flush()` to actually send the events. There is no mechanism for automatically sending events after some period of time unless `max_buffer_size` is exceeded.

```python
import analytics

# This configuration happens statically
analytics.set_config(analytics.Config(buffered=True))

# Spread out through an application, multiple events get tracked. These could be
# during API requests or at any other time.
analytics.track('donation_received', {'amount': 25.00, 'donor_id': 111111})
analytics.track('donation_received', {'amount': 50.00, 'donor_id': 123456})
analytics.track('donation_received', {'amount': 5.00, 'donor_id': 789})

# After the request is finished, or at some other reasonable time, call flush
# to actually send the events to the server.
analytics.flush()
```
