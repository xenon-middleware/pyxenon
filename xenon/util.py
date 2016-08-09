# PyXenon Xenon API wrapper
#
# Copyright 2015 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Utility functions """

import inspect
import os


def _local_function():
    """ local function for passing into module_path."""
    pass


def module_path(local_function=_local_function):
    """
    Returns the path of the given function without the use of __file__.

    Requires a function defined locally in the module.
    From http://stackoverflow.com/questions/729583

    @param local_function: function to get the file path from, by default gets
        the xenon.util file path.
    @raise ValueError: if the given function does not have a file associated
        to it (for example, in the interpreter or from eval()).
    @return: absolute path of the file of the given function
    """
    path = inspect.getsourcefile(local_function)
    if path is None or not os.path.exists(path):
        raise ValueError('Given function "{0}" is not installed in any file '
                         'or package.')
    return os.path.abspath(path)
