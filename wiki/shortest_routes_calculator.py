from typing import Dict, List
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

    def set_goal_num(self, goal_num: int):
        self.goal_num = goal_num

    def set_limit(self, limit: int):
        self.limit = limit

    def calculate(self, source: WikipediaPage, destination: WikipediaPage) -> [[str]]:
        self._populate_routes(source, destination, [source.title])
        return self._get_shortest()

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

    def _populate_routes(self, source: WikipediaPage, destination: WikipediaPage, cur_route: [str]):
        if source == destination:
            self._add_route(cur_route)
            return

        cur_length = len(cur_route)

        if cur_length == self.limit:
            return

        for link_title in source.links:
            if link_title in self.visited and self.visited[link_title] <= cur_length:
                break
            else:
                self.visited[link_title] = cur_length

            try:
                link = WikipediaPage(title=link_title)
            except DisambiguationError:
                break
            except PageError:
                break

            self._populate_routes(link, destination, cur_route + [link_title])

    def _add_route(self, route: [str]):
        self.routes.append(route)
        self.route_found.emit(route)
