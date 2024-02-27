import json
import uuid

from BubbleScan.serializers.scantron import ScantronJsonEncoder
from BubbleScan.domain.scantron import Scantron

"""
Module: test_scantron_serialization

This module contains a unit test for serializing a domain Scantron object.
"""

def test_serialize_domain_scantron():
    """
    Test the serialization of a domain Scantron object.
    """
    code = uuid.uuid4()
    
scantron = Scantron(
        code = code,
        first = "John",
        last = "Charlie", 
        idNumber = 34563,
    )
    
expected_json = f"""{{"code": "{code}", "first": "John", "last": "Charlie", "idNumber": 34563 }}
    """
    
json_scantron = json.dumps(scantron, cls = ScantronJsonEncoder)
    
assert json.loads(json_scantron) == json.loads(expected_json)
