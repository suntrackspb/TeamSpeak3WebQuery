from dataclasses import dataclass


@dataclass
class ChannelListInfo:
    cid: int
    pid: int
    channel_name: str
    channel_needed_subscribe_power: int
    channel_order: int
    total_clients: int

    @staticmethod
    def from_dict(data: dict) -> 'ChannelListInfo':
        return ChannelListInfo(
            cid=int(data['cid']),
            pid=int(data['pid']),
            channel_name=data['channel_name'],
            channel_needed_subscribe_power=int(data['channel_needed_subscribe_power']),
            channel_order=int(data['channel_order']),
            total_clients=int(data['total_clients'])
        )
