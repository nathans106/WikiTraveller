from PySide6.QtCore import Slot
from wikipedia import WikipediaPage, search

from wiki.shortest_routes_calculator import ShortestRoutesCalculator


@Slot(object)
def print_callback(route: [str]):
    print(route)


def _first_page(query) -> WikipediaPage:
    return WikipediaPage(search(query, 1))


calculator = ShortestRoutesCalculator()
calculator.set_limit(3)
diamonds = _first_page('chemistry')
ww2 = _first_page('bunsen')
calculator.route_found.connect(print_callback)
routes = calculator.calculate(diamonds, ww2)

print('-----')
print('finished')
print('-----')
print(routes)
