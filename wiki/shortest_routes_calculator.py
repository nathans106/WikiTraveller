from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List, Optional
from PySide6.QtCore import QObject, Signal
from wikipedia import WikipediaPage, DisambiguationError, PageError


class ShortestRoutesCalculator(QObject):
    route_found = Signal(object)

    def __init__(self):
        QObject.__init__(self)
        self.visited: Dict = {}
        self.goal_num: int = 5
        self.limit: int = 6
        self.routes: [[str]] = []
        self.executor = ThreadPoolExecutor()
        self.destination: Optional[WikipediaPage] = None

    def set_goal_num(self, goal_num: int):
        self.goal_num = goal_num

    def set_limit(self, limit: int):
        self.limit = limit

    def calculate(self, source: WikipediaPage, destination: WikipediaPage) -> [[str]]:
        self.destination = destination
        self._process_route([source.title])
        return self._get_shortest()

    def _process_route(self, route: [str]):
        length = len(route)
        assert length > 0

        last_title = route[-1]
        if last_title == self.destination.title:
            self._add_route(route)
            return

        if last_title in self.visited and self.visited[last_title] <= length:
            return
        else:
            self.visited[route[-1]] = length

        if length == self.limit:
            return

        try:
            last_page = WikipediaPage(title=last_title)
        except DisambiguationError:
            return
        except PageError:
            return

        next_routes = [route + [link] for link in last_page.links]
        for next_route in next_routes:
            self._process_route(next_route)

    def _add_route(self, route: [str]):
        self.routes.append(route)
        self.route_found.emit(route)

    def _get_shortest(self) -> [[str]]:
        self.routes.sort(key=len)
        shortest: [[str]] = []
        last_length: int = 0

        for route in self.routes:
            cur_length = len(route)

            if len(shortest) < self.goal_num:
                shortest.append(route)
                last_length = cur_length
            else:
                if cur_length == last_length:
                    shortest.append(cur_length)
                else:
                    return shortest

        return shortest
