import json
from dataclasses import dataclass
from datetime import datetime, time
from json import JSONEncoder


@dataclass(init=False)
class SwitchAggFlowStats:
    def __init__(self, switch_id: int):
        self.switch_id = switch_id
        self.bytes_per_second_received: dict[time, int] = dict()
        self.packets_per_second_received: dict[time, int] = dict()

    def add_agg_flow_stats(self, bytes_per_second: int, packets_per_second: int):
        time_of_stat = datetime.now().time()
        time_of_stat = time_of_stat.replace(microsecond=0)

        if time_of_stat not in self.bytes_per_second_received:
            self.bytes_per_second_received[time_of_stat] = bytes_per_second
            self.packets_per_second_received[time_of_stat] = packets_per_second
        else:
            self.bytes_per_second_received[time_of_stat] += bytes_per_second
            self.packets_per_second_received[time_of_stat] += packets_per_second

    def get_bytes_per_second_for(self, timestamp: datetime):
        time_of_request = timestamp.time()
        time_of_request = time_of_request.replace(time_of_request.hour, time_of_request.minute, time_of_request.second, 0)
        if time_of_request not in self.bytes_per_second_received:
            return 0
        return self.bytes_per_second_received[time_of_request]

    def get_packets_per_second_for(self, timestamp: datetime):
        time_of_request = timestamp.time()
        time_of_request = time_of_request.replace(time_of_request.hour, time_of_request.minute, time_of_request.second, 0)
        if time_of_request not in self.packets_per_second_received:
            return 0
        return self.packets_per_second_received[time_of_request]

    def __str__(self):
        return json.dumps(self, cls=SwitchAggFlowStatsEncoder)


class SwitchAggFlowStatsEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, SwitchAggFlowStats):
            return {
                'switch_id': o.switch_id,
                'bytes_per_second_received':  {str(k): v for k, v in o.bytes_per_second_received.items()},
                'packets_per_second_received': {str(k): v for k, v in o.packets_per_second_received.items()}
            }
        return super().default(o)


class SwitchAggFlowStatsDecoder(json.JSONDecoder):
    def object_hook(self, dct):
        if 'switch_id' in dct and 'bytes_per_second_received' in dct and 'packets_per_second_received' in dct:
            switch_id = dct['switch_id']
            stats = SwitchAggFlowStats(switch_id)
            stats.bytes_per_second_received = {time.fromisoformat(k): v for k, v in dct['bytes_per_second_received'].items()}
            stats.packets_per_second_received = {time.fromisoformat(k): v for k, v in dct['packets_per_second_received'].items()}
            return stats
        return dct