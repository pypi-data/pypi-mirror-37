# coding=utf-8
# --------------------------------------------------------------------------
# Copyright © 2018 FINBOURNE TECHNOLOGY LTD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReconciliationBreak(Model):
    """A reconciliation break.

    :param instrument_uid: Unique instrument identifier
    :type instrument_uid: str
    :param properties:
    :type properties: list[~lusid.models.Property]
    :param units_difference: Difference in units
    :type units_difference: float
    :param cost_difference: Difference in cost
    :type cost_difference: float
    """

    _validation = {
        'instrument_uid': {'required': True},
    }

    _attribute_map = {
        'instrument_uid': {'key': 'instrumentUid', 'type': 'str'},
        'properties': {'key': 'properties', 'type': '[Property]'},
        'units_difference': {'key': 'unitsDifference', 'type': 'float'},
        'cost_difference': {'key': 'costDifference', 'type': 'float'},
    }

    def __init__(self, instrument_uid, properties=None, units_difference=None, cost_difference=None):
        super(ReconciliationBreak, self).__init__()
        self.instrument_uid = instrument_uid
        self.properties = properties
        self.units_difference = units_difference
        self.cost_difference = cost_difference
