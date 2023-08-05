from abc import ABCMeta

import pytest

from clusterone.business_logic.generic_commands import ListCommand


class BaseListCommandUnderTest(ListCommand):
    __metaclass__ = ABCMeta
    enumerate = False
    table_header = ("Test",)
    entity_name = "test"

    @staticmethod
    def _entity_to_row(entity_data):
        prop0 = entity_data["prop0"]
        prop1 = entity_data["prop1"]

        return prop0, prop1


class TestListCommand(object):
    @pytest.mark.parametrize("input_table_data, expected_table_data", [
        ((("first_item",),), (("1", "first_item"),)),
        ((("a", "b", "c", "d"),), (("1", "a", "b", "c", "d"),)),
        ((("first_item",), ("second_item",),), (("1", "first_item"), ("2", "second_item"),)),
        ((("a", "b", "c", "d"), ("e", "f", "g", "h"),), (("1", "a", "b", "c", "d"), ("2", "e", "f", "g", "h"),)),
    ])
    def test_enumerate_table_data(self, input_table_data, expected_table_data):
        assert tuple(ListCommand._enumerate_table_data(input_table_data)) == expected_table_data

    @pytest.mark.parametrize("input_entity_name, expected_output", [
        ("test_object", "You don't seem to have any test_objects yet. Try 'just create test_object' to make one."),
        ("project", "You don't seem to have any projects yet. Try 'just create project' to make one."),
    ])
    def test_when_no_entities_are_found_output_contains_info_on_how_to_create_one(self, client, input_entity_name,
                                                                                  expected_output):
        class ListCommandUnderTest(BaseListCommandUnderTest):
            entity_name = input_entity_name

            def _gather_entity_data(self):
                return []

        cmd = ListCommandUnderTest(client=client)

        result = cmd.execute()

        assert result["output"] == expected_output

    def test_when_notebooks_are_found_output_is_table_string(self, client, mocker):
        class ListCommandUnderTest(BaseListCommandUnderTest):
            enumerate = False
            table_header = ("My prop 0", "My prop 1")

            def _gather_entity_data(self):
                return [{"prop0": "value0", "prop1": "value1"}, {"prop0": "value2", "prop1": "value3"}]

        make_table_fn_mock = mocker.Mock(return_value="example table string")
        cmd = ListCommandUnderTest(client=client, make_table_fn=make_table_fn_mock)

        result = cmd.execute()

        args, kwargs = make_table_fn_mock.call_args
        call_table_data = tuple(args[0])
        call_table_header = kwargs["header"]
        assert call_table_data == (("value0", "value1"), ("value2", "value3"))
        assert call_table_header == ("My prop 0", "My prop 1")

        assert result["output"] == "example table string"

    def test_when_enumerate_is_on_then_table_data_is_enumerated(self, client, mocker):
        class ListCommandUnderTest(BaseListCommandUnderTest):
            enumerate = True
            table_header = ("some header",)

            def _gather_entity_data(self):
                return [{"prop0": "a", "prop1": "b"}, {"prop0": "c", "prop1": "d"}]

        make_table_fn_mock = mocker.Mock(side_effect=lambda x, header: {"data": x, "header": header})
        cmd = ListCommandUnderTest(client=client, make_table_fn=make_table_fn_mock)

        result = cmd.execute()

        assert tuple(result["output"]["data"]) == (("1", "a", "b"), ("2", "c", "d"))
        assert result["output"]["header"] == ("#", "some header")

    def test_when_enumerate_is_off_then_table_data_is_not_enumerated(self, client, mocker):
        class ListCommandUnderTest(BaseListCommandUnderTest):
            enumerate = False
            table_header = ("some other header",)

            def _gather_entity_data(self):
                return [{"prop0": "e", "prop1": "f"}, {"prop0": "g", "prop1": "h"}]

        make_table_fn_mock = mocker.Mock(side_effect=lambda x, header: {"data": x, "header": header})
        cmd = ListCommandUnderTest(client=client, make_table_fn=make_table_fn_mock)

        result = cmd.execute()

        assert tuple(result["output"]["data"]) == (("e", "f"), ("g", "h"))
        assert result["output"]["header"] == ("some other header",)
