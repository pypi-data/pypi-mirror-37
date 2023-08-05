from collections import namedtuple

Robot = namedtuple("Robot", ["year", "robot_name", "key", "team_key"])
Datacache = namedtuple("Datacache", ["data", "last_modified", "expiry"])
Webcast = namedtuple("Webcast", ["type", "channel", "file"])
