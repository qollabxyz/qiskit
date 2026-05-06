# This code is part of Qiskit.
#
# (C) Copyright IBM 2022, 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
Job for the reference implementations of Primitives V1 and V2.
"""

# PrivimiteJob is dumbed down to run on the main thread (threading isn't enabled in our environment for security reasons)

import uuid

from qiskit.providers import JobError, JobStatus
from qiskit.providers.jobstatus import JOB_FINAL_STATES

from .base.base_primitive_job import BasePrimitiveJob, ResultT


class PrimitiveJob(BasePrimitiveJob[ResultT, JobStatus]):
    """Handle to a job from the reference implementations of the primitives in Qiskit.

    This is a concrete implementation of the :class:`.BasePrimitiveJob` interface.  See the
    documentation of that class for a discussion of the interface.

    Primitives implementers looking to create their own job classes should not subclass this, but
    instead subclass the interface definition :class:`.BasePrimitiveJob`.
    """

    def __init__(self, function, *args, **kwargs):
        """
        Args:
            function: A callable function to execute the job.
            args: any additional positional arguments
            kwargs: any additional keyword arguments
        """
        super().__init__(str(uuid.uuid4()))
        self._submitted = False
        self._result = None
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def _submit(self):
        self._result = self._function(*self._args, **self._kwargs)
        self._submitted = True

    def result(self) -> ResultT:
        return self._result

    def status(self) -> JobStatus:
        if self._submitted:
            return JobStatus.DONE
        raise JobError("Primitive Job has not been submitted yet.")

    def cancel(self):
        pass

    def done(self) -> bool:
        self.status()
        return True

    def running(self) -> bool:
        return False

    def cancelled(self) -> bool:
        return False

    def in_final_state(self) -> bool:
        return self.done()
