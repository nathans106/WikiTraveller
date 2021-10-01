
#include "ShortestRouteCalculator.h"
#include <cassert>

namespace wiki {
    ShortestRouteCalculator::ShortestRouteCalculator(int limit) : limit(limit) {}

    Route ShortestRouteCalculator::calculate(const Page& source, const Page destination) {
        this->destination = std::make_unique<Page>(std::move(destination));
        queue.push({ source });

        while (!queue.empty()) {
            const auto route = queue.front();
            queue.pop();

            if (ProcessRoute(route)) {
                return route;
            }
        }

        throw LimitReachedError();
    }

    bool ShortestRouteCalculator::ProcessRoute(const Route& route) {
        assert(!route.empty());
        auto& from = route.back();
        visited.insert(from);

        if (from == *destination) {
            return true;
        }

        if (route.size() >= limit) {
            return false;
        }

        for (const auto& newPage : from.links()) {
            if (visited.find(newPage) == visited.end()) {
                auto newRoute = route;
                newRoute.push_back(newPage);
                queue.push(newRoute);
            }
        }

        return false;
    }
}
