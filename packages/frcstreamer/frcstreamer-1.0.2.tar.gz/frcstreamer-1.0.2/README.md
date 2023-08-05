# frcstreamer
A Python package to obtain a single video feed for an FRC event, all video feeds for an FRC event, or all live FRC event feeds.

Usage:

To bring FRCStreamer in, simply import it and initialize it

```python
import frcstreamer

streamer = frcstreamer.FRCStreamer("tba_api_key")
```

To get one stream for an event, use the following command:

```python
streamer.get_stream_from_event("tba_event_key")
```

To get all streams for an event, do the following:

```python
streamer.get_event_streams("tba_event_key")
```


And finally, to get all live streams do:

```python
streamer.get_all_streams()
```

To get a TBA API key, create a TBA account at https://thebluealliance.com/account