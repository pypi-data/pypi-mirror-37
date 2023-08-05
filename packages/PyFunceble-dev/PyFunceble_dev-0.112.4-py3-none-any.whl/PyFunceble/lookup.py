#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the lookup interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long

import PyFunceble
from PyFunceble import socket


class Lookup:
    """
    This class can be used to NSLOOKUP or WHOIS lookup.
    """

    @classmethod
    def nslookup(cls):
        """
        Implementation of UNIX nslookup.
        """

        try:
            # We try to get the addresse information of the given domain or IP.
            socket.getaddrinfo(
                PyFunceble.CONFIGURATION["domain"], 80, 0, 0, socket.IPPROTO_TCP
            )

            # It was done successfuly, we return True.
            # Note: we don't need to read the addresses so we consider as successful
            # as long as there is no error.
            return True

        except (OSError, socket.herror, socket.gaierror):
            # One of the listed exception is matched.

            # It was done unsuccesfuly, we return False.
            return False

    @classmethod
    def whois(cls, whois_server, domain=None, timeout=None):  # pragma: no cover
        """
        Implementation of UNIX whois.

        Arguments:
            - whois_server: str
                The whois server to use to get the record.
            - domain: str
                The domain to get the whois record from.
            - timeout: int
                The timeout to apply to the request.

        Returns: None or str
            None: No whois record catched.
            str: The whois record.
        """

        if domain is None:
            # The domain is not given (localy).

            # We consider the domain as the domain or IP we are currently testing.
            domain = PyFunceble.CONFIGURATION["domain"]

        if timeout is None:
            # The time is not given (localy).

            # We consider the timeout from the configuration as the timeout to use.
            timeout = PyFunceble.CONFIGURATION["seconds_before_http_timeout"]

        if whois_server:
            # A whois server is given.

            # We initiate a socket.
            req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if timeout % 3 == 0:
                # The timeout is modulo 3.

                # We report the timeout to our initiated socket.
                req.settimeout(timeout)
            else:
                # The timeout is not modulo 3.

                # We report 3 seconds as the timeout to our initiated socket.
                req.settimeout(3)

            try:
                # We try to connect to the whois server at the port 43.
                req.connect((whois_server, 43))
            except socket.error:
                # We got an error.

                # We return None.
                return None

            # We send end encode the domain we want the data from.
            req.send((domain + "\r\n").encode())

            # We initiate a bytes variable which will save the response
            # from the server.
            response = b""

            while True:
                # We loop infinitly.
                try:
                    # We try to receive the data in a buffer of 4096 bytes.
                    data = req.recv(4096)
                except (socket.timeout, ConnectionResetError):
                    # We got an error.

                    # We close the connection.
                    req.close()

                    # And we return None.
                    return None

                # Everything goes right.

                # We append data to the response we got.
                response += data

                if not data:
                    # The data is empty.

                    # We break the loop.
                    break

            # We close the connection.
            req.close()

            try:

                # We finally decode and return the response we got from the
                # server.
                return response.decode()

            except UnicodeDecodeError:
                # We got an encoding error.

                # We decode the response.
                # Note: Because we don't want to deal with other issue, we
                # decided to use `replace` in order to automatically replace
                # all non utf-8 encoded characters.
                return response.decode("utf-8", "replace")

        # The whois server is not given.

        # We return None.
        return None
