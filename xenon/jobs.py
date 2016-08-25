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

"""
Job classes

Use as arguments in API. The `package` variable stores the Java package
name of the Xenon jobs API. Use xenon.jobs.JobDescription to submit a job with.
"""

from .java import JavaClass

package = 'nl.esciencecenter.xenon.jobs'
JobDescription = JavaClass(package + '.JobDescription')

__all__ = ['JobDescription']
