#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the execution time logic.

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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import Fore, OrderedDict, Style, path, time
from PyFunceble.helpers import Dict, File


class ExecutionTime:  # pylint: disable=too-few-public-methods
    """
    Set and return the exection time of the program.

    Arguments:
        - action: str
            'start' or 'stop'
        - last
            Tell the subsystem if we are at the very end of the test.
    """

    def __init__(self, action="start", last=False):
        # We parse the action to the class scope.
        self.action = action

        if self._authorization():
            # * The execution time disaply is activated.
            # or
            # * The Travis CI mode is activated.

            if self.action == "start":
                # The action is equal to `start`.

                # We set the starting time.
                self._starting_time()
            elif self.action == "stop":
                # * The action is not equal to `start`.
                # and
                # * The action is equal to `stop`

                # We set the ending time.
                self._stoping_time()

                # And we print the execution time.
                print(
                    Fore.MAGENTA
                    + Style.BRIGHT
                    + "\nExecution time: "
                    + self.format_execution_time()
                )

        self._save(last=last)

    @classmethod
    def _authorization(cls):
        """
        Check the execution authorization.
        """

        if (
            PyFunceble.CONFIGURATION["show_execution_time"]
            or PyFunceble.CONFIGURATION["travis"]
        ):
            return True

        return False

    def _save(self, last=False):
        """
        Save the current time to the file.

        Argument:
            - last: bool
                Tell us if we are at the really end of the testing.
        """

        if self._authorization() and PyFunceble.CONFIGURATION["logs"]:
            self.file = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                + PyFunceble.OUTPUTS["logs"]["filenames"]["execution_time"]
            )

            if path.isfile(self.file):
                content = Dict().from_json(File(self.file).read())
            else:
                content = {}

            if self.action == "start":
                if "final_total" in content and content["final_total"]:
                    del content["final_total"]

                if "data" in content:
                    content["data"].append([PyFunceble.CONFIGURATION["start"]])
                else:
                    content["data"] = [[PyFunceble.CONFIGURATION["start"]]]
            elif self.action == "stop":
                try:
                    content["data"][-1].append(PyFunceble.CONFIGURATION["end"])

                    start = content["data"][0][0]
                    end = content["data"][-1][-1]

                    content["current_total"] = self.format_execution_time(start, end)

                    if last:
                        content["final_total"] = content["current_total"]

                        print(
                            Fore.MAGENTA
                            + Style.BRIGHT
                            + "Global execution time: "
                            + content["final_total"]
                        )
                except KeyError:
                    pass

            Dict(content).to_json(self.file)

    @classmethod
    def _starting_time(cls):  # pragma: no cover
        """
        Set the starting time.
        """

        # We set the starting time as the current time.
        PyFunceble.CONFIGURATION["start"] = int(time())

    @classmethod
    def _stoping_time(cls):  # pragma: no cover
        """
        Set the ending time.
        """

        # We set the ending time as the current time.
        PyFunceble.CONFIGURATION["end"] = int(time())

    @classmethod
    def _calculate(cls, start=None, end=None):
        """
        calculate the difference between starting and ending time.

        Returns: dict
            A dics with `days`,`hours`,`minutes` and `seconds`.
        """

        if start and end:
            # The start and end time is explicitly given.

            # We get the difference between the ending and the starting time.
            time_difference = int(end) - int(start)
        else:
            # The start and end time is not explicitly given.

            # We get the difference between the ending and the starting time.
            time_difference = (
                PyFunceble.CONFIGURATION["end"] - PyFunceble.CONFIGURATION["start"]
            )

        # We initiate an OrderedDict.
        # Indeed, we use an ordered dict because we want the structuration and the
        # order to stay always the same.
        # As a dictionnary is always unordered, we can use it. Otherwise the time will
        # not be shown correctly.
        data = OrderedDict()

        # We calculate and append the day to our data.
        data["days"] = str(time_difference // (24 * 3600)).zfill(2)

        # We calculate and append the hours to our data.
        data["hours"] = str(time_difference // 3600).zfill(2)

        # We calculate and append the minutes to our data.
        data["minutes"] = str((time_difference % 3600) // 60).zfill(2)

        # We calculate and append the minutes to our data.
        data["seconds"] = str(time_difference % 60).zfill(2)

        # We finaly return our data.
        return data

    def format_execution_time(self, start=None, end=None):
        """
        Format the calculated time into a human readable format.

        Returns: str
            A human readable date.
        """

        # We return the formated execution time.
        return ":".join(list(self._calculate(start, end).values()))
