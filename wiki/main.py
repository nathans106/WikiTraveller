from PySide6.QtCore import Slot
from wikipedia import WikipediaPage, search

from wiki.shortest_routes_calculator import ShortestRoutesCalculator


count = 0

@Slot(object)
def print_callback(route: [str]):
    print(route)

@Slot(str)
def receive_page(title: str):
    global count
    count += 1
    print(count)

def _first_page(query) -> WikipediaPage:
    return WikipediaPage(search(query, 1))


calculator = ShortestRoutesCalculator()
calculator.set_limit(3)
diamonds = _first_page('united kingdom')
ww2 = _first_page('ireland')
calculator.route_found.connect(print_callback)
calculator.page_visited.connect(receive_page)
routes = calculator.calculate(diamonds, ww2)

print('-----')
print('finished')
print('-----')
print(routes)
