from .offset import OffsetNumber


_topic_offset_heads: dict[str, int] = {}


def next_offset(topic: str) -> OffsetNumber:
    head = _topic_offset_heads.get(topic)
    if head is None:
        return 0
    return head + 1


def set_head(topic: str, offset: OffsetNumber) -> None:
    _topic_offset_heads[topic] = offset
