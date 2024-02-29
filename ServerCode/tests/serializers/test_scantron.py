"""
Module: test_scantron_serialization

This module contains a unit test for serializing a domain Scantron object.
"""

import json
import uuid

from bubbleScan.serializers.scantron import ScantronJsonEncoder
from bubbleScan.domain.scantron import Scantron

def test_serialize_domain_scantron():
    """
    Test the serialization of a domain Scantron object.
    """
    code = uuid.uuid4()

scantron = Scantron(
        code = uuid.uuid4(),
        first = "John",
        last = "Charlie",
        id_number = 34563,
    )

expected_json = f"""{{"code": "{uuid.uuid4()}", "first": "John", 
"last": "Charlie", "id_number": 34563 }}
    """

json_scantron = json.dumps(scantron, cls = ScantronJsonEncoder)

assert json.loads(json_scantron) == json.loads(expected_json)
