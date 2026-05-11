from model import LostItem


_items = [
    LostItem(id=1, item_name="지갑", found_place="도서관 1층", found_time="2026-03-01 10:30", is_returned=False),
    LostItem(id=2, item_name="에어팟", found_place="기숙사 로비", found_time="2026-03-02 11:00", is_returned=True),
    LostItem(id=3, item_name="학생증", found_place="도서관 열람실", found_time="2026-03-03 09:20", is_returned=False),
    LostItem(id=4, item_name="우산", found_place="본관 입구", found_time="2026-03-04 14:10", is_returned=True),
    LostItem(id=5, item_name="노트북", found_place="컴퓨터실", found_time="2026-03-05 16:45", is_returned=False),
]


def get_items() -> list[LostItem]:
    return _items


def get_item_by_id(item_id: int) -> LostItem | None:
    for item in _items:
        if item.id == item_id:
            return item
    return None


def filter_items(returned: bool | None, place: str | None) -> list[LostItem]:
    results = _items

    if returned is not None:
        results = [item for item in results if item.is_returned == returned]

    if place is not None:
        results = [item for item in results if place in item.found_place]

    return results