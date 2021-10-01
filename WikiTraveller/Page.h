#pragma once

#include <list>
#include <string>

class Page
{
public:
    bool operator==(const Page& rhs);

    std::list<Page> links() const;

    static Page firstPage(const std::string& title);
};
