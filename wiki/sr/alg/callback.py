class CallbackWrapper:
    def __init__(self, callback):
        self._callback = callback

    def __callback__(self, route):
        if self._callback is not None:
            self._callback(route)

    def next(self, link_title):
        return [link_title]


class CallbackPropogator:
    def __init__(self, callback, link_title):
        self._callback = callback
        self._route: [str] = callback.next(link_title)

    def __call__(self, route: [str]):
        self._callback(self._route + route)

    def next(self, link_title: str) -> [str]:
        return self._route + [link_title]
