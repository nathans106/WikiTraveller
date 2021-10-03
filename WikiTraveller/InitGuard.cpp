#include "InitGuard.h"

#include <curl/curl.h>

namespace wiki {
    InitGuard::InitGuard() {
        curl_global_init(CURL_GLOBAL_DEFAULT);
    }

    InitGuard::~InitGuard() {
        curl_global_cleanup();
    }
}
