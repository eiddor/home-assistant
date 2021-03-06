"""Test Z-Wave switches."""
from homeassistant.components.switch import zwave

from tests.mock.zwave import (
   MockNode, MockValue, MockEntityValues, value_changed)


def test_get_device_detects_switch(mock_openzwave):
    """Test get_device returns a Z-Wave switch."""
    node = MockNode()
    value = MockValue(data=0, node=node)
    values = MockEntityValues(primary=value)

    device = zwave.get_device(node=node, values=values, node_config={})
    assert isinstance(device, zwave.ZwaveSwitch)


def test_switch_turn_on_and_off(mock_openzwave):
    """Test turning on a Z-Wave switch."""
    node = MockNode()
    value = MockValue(data=0, node=node)
    values = MockEntityValues(primary=value)
    device = zwave.get_device(node=node, values=values, node_config={})

    device.turn_on()

    assert node.set_switch.called
    value_id, state = node.set_switch.mock_calls[0][1]
    assert value_id == value.value_id
    assert state is True
    node.reset_mock()

    device.turn_off()

    assert node.set_switch.called
    value_id, state = node.set_switch.mock_calls[0][1]
    assert value_id == value.value_id
    assert state is False


def test_switch_value_changed(mock_openzwave):
    """Test value changed for Z-Wave switch."""
    node = MockNode()
    value = MockValue(data=False, node=node)
    values = MockEntityValues(primary=value)
    device = zwave.get_device(node=node, values=values, node_config={})

    assert not device.is_on

    value.data = True
    value_changed(value)

    assert device.is_on
