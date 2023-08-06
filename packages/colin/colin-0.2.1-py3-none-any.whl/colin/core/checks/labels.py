# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from .check_utils import check_label
from .dockerfile import DockerfileAbstractCheck
from .images import ImageAbstractCheck
from ..result import CheckResult


class LabelAbstractCheck(ImageAbstractCheck, DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, labels, required,
                 value_regex=None):
        super(LabelAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.labels = labels
        self.required = required
        self.value_regex = value_regex

    def check(self, target):
        passed = check_label(labels=self.labels,
                             required=self.required,
                             value_regex=self.value_regex,
                             target_labels=target.labels)

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])


class DeprecatedLabelAbstractCheck(ImageAbstractCheck, DockerfileAbstractCheck):

    def __init__(self, message, description, reference_url, tags, old_label, new_label):
        super(DeprecatedLabelAbstractCheck, self) \
            .__init__(message, description, reference_url, tags)
        self.old_label = old_label
        self.new_label = new_label

    def check(self, target):
        labels = target.labels
        old_present = labels is not None and self.old_label in labels

        passed = (not old_present) or (self.new_label in labels)

        return CheckResult(ok=passed,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
