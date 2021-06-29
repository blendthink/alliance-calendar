import dataclasses

from urllib3.util.url import Url


@dataclasses.dataclass(frozen=True)
class CalendarImageUrl:
    url: Url
