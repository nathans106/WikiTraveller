from typing import Optional, Set

from wikipedia import wikipedia

from wiki.sr.alg.callback import CallbackWrapper

no_max = -1


# Main function
def shortest_routes(source_title: str, destination_title, goal_num: Optional[int] = 0, callback=None):
    source_page = _first_page(source_title)
    destination_page = _first_page(destination_title)
    callback_wrapper = CallbackWrapper(callback)
    visited = {source_title}


def shortest_routes_internal(source_title: str, destination_title: str, visited: Set, goal_num: Optional[int] = None, callback=None):
    


    routes: [[str]] = []
    for link_title in source_page.links:
        if link_title in visited:
            break
        else:
            visited.add(link_title)

        if link_title == destination_title:
            route = [source_title, destination_title]
            routes.append(destination_title)
            callback(route)

        else:
            pre_route = [source_title]
            for link_route in shortest_routes(link_title, destination_title, goal_num, Callback(callback, link_title)):
                route = pre_route + link_route
                routes.append(route)
                callback(route)

    return _calculate(routes, goal_num)


# private_Functions
def _first_page(query) -> wikipedia.WikipediaPage:
    return wikipedia.WikipediaPage(wikipedia.search(query, 1))


def _calculate(routes: [[str]], goal_num: int) -> [[str]]:
    routes.sort(key=len)
    shortest: [[str]] = []
    last_length: int = 0

    for route in routes:
        cur_length = len(route)

        if len(shortest) < goal_num:
            shortest.append(route)
            last_length = cur_length
        else:
            if cur_length == last_length:
                shortest.append(cur_length)
            else:
                return shortest

    return shortest
