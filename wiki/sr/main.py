from wiki.sr.program import Application
from wiki.sr.shortest_routes import shortest_routes


def print_callback(route):
    print(route)


routes = shortest_routes("diamonds", "world war two", 5, print_callback)
print('-----')
print('finished')
print('-----')
print(routes)
