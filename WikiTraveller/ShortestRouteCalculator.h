#pragma once

#include "Page.h"

#include <list>
#include <memory>
#include <queue>
#include <optional>
#include <set>
#include <stdexcept>

namespace wiki {
using Route = std::list<Page>;


class ShortestRouteCalculator {
public:
    class LimitReachedError : public std::runtime_error {
    public:
        LimitReachedError() : std::runtime_error("Route limit reached") {}
    };

    ShortestRouteCalculator() = default;
    ShortestRouteCalculator(int limit);

    Route calculate(const Page& source, const Page destination);

private:
    bool ProcessRoute(const Route& route);

    std::unique_ptr<Page> destination = nullptr;
    std::queue<Route> queue;
    std::set<Page> visited;
    int limit = 4;
};
}
