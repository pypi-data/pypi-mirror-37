from statsd import StatsClient


def statsd_from_config(config: dict) -> StatsClient:
    statsd_config = config["statsd"]

    client = StatsClient(**statsd_config)
    return client
