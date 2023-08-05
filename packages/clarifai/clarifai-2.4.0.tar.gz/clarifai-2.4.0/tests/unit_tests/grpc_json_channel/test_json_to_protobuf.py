import unittest

from clarifai.rest.grpc.grpc_json_channel import dict_to_protobuf
from clarifai.rest.grpc.proto.clarifai.api.concept_pb2 import Concept as ConceptPB


class TestJsonToProtobuf(unittest.TestCase):
  _multiprocess_can_split_ = True

  def test_concept_with_no_value(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name'})
    assert converted.value == 1.0

  def test_concept_with_value_non_zero(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name', 'value': 0.5})
    assert converted.value == 0.5

  def test_concept_with_value_zero(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name', 'value': 0.0})
    assert converted.value == 0.0

  def test_concept_with_value_one(self):
    converted = dict_to_protobuf(ConceptPB, {'id': 'some-id', 'name': 'Some Name', 'value': 1.0})
    assert converted.value == 1.0
