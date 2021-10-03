#include "httpsGet.h"

#include <stdio.h>
#include <curl/curl.h>
#include <stdexcept>
#include <sstream>

static int count = 0;

namespace wiki {
    void HttpsGet::get() {
        auto* curl = curl_easy_init();
        if (!curl) {
            throw std::runtime_error("Failed to initialise curl");
        }

        curl_easy_setopt(curl, CURLOPT_URL, "https://example.com/");

#ifdef SKIP_PEER_VERIFICATION
        /*
         * If you want to connect to a site who isn't using a certificate that is
         * signed by one of the certs in the CA bundle you have, you can skip the
         * verification of the server's certificate. This makes the connection
         * A LOT LESS SECURE.
         *
         * If you have a CA cert for the server stored someplace else than in the
         * default bundle, then the CURLOPT_CAPATH option might come handy for
         * you.
         */
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
#endif

#ifdef SKIP_HOSTNAME_VERIFICATION
        /*
         * If the site you're connecting to uses a different host name that what
         * they have mentioned in their server certificate's commonName (or
         * subjectAltName) fields, libcurl will refuse to connect. You can skip
         * this check, but this will make the connection less secure.
         */
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
#endif

        /* Perform the request, res will get the return code */
        const auto res = curl_easy_perform(curl);

        /* always cleanup */
        curl_easy_cleanup(curl);

        /* Check for errors */
        if (res != CURLE_OK) {

            std::stringstream ss;
            ss << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
            throw std::runtime_error(ss.str());
        }
    }
}

