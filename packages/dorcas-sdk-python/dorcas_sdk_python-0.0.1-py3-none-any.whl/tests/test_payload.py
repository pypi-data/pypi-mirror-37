import dorcas_sdk_python
import pytest


def test_payload_created():
    item = dorcas_sdk_python.PayloadItem('name', 'Emmanuel')
    assert item.name == 'name'


def test_string_conversion():
    item = dorcas_sdk_python.PayloadItem('name', 'Emmanuel')
    assert str(item) == 'PayloadItem<name=name, value=Emmanuel>'


def test_payload_bag():
    bag = dorcas_sdk_python.PayloadBag()
    assert len(bag.bag) == 0


def test_payload_bag_add_item_requires_payload_item():
    bag = dorcas_sdk_python.PayloadBag()
    with pytest.raises(TypeError):
        bag.add_item('ParamName')


def test_payload_bag_has_item():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_item(dorcas_sdk_python.PayloadItem('name', 'Emmanuel'))
    assert bag.has_item('name')


def test_payload_bag_remove_item():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_item(dorcas_sdk_python.PayloadItem('name', 'Emmanuel'))
    assert len(bag.remove_item(0).to_payload()) == 0


def test_payload_bag_works_with_payload_item():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_item(dorcas_sdk_python.PayloadItem('name', 'Emmanuel'))
    assert len(bag.bag) == 1


def test_payload_bag_add_simple_requires_string_name():
    bag = dorcas_sdk_python.PayloadBag()
    with pytest.raises(TypeError):
        bag.add_simple(dorcas_sdk_python.PayloadItem('name', 'Emmanuel'), [])


def test_payload_bag_add_simple():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_simple('name', 'Emmanuel')
    assert len(bag.bag) == 1


def test_payload_bag_remove_item_by_name():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_simple('name', 'Emmanuel')
    bag.add_simple('age', 25)
    bag.remove_item_by_name('name')
    assert len(bag.bag) == 1


def test_payload_bag_set_item_by_name():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_simple('name', 'Emmanuel')
    assert bag.to_payload()['name'] == 'Emmanuel'
    bag.set_item_by_name('name', 'Joshua')
    assert bag.to_payload()['name'] == 'Joshua'


def test_payload_bag_get_item_by_index():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_simple('name', 'Emmanuel')
    assert bag.get_item(0).value == 'Emmanuel'


def test_payload_bag_get_item_by_name():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_simple('name', 'Emmanuel')
    assert bag.get_item_by_name('name').value == 'Emmanuel'


def test_payload_bag_set_items():
    bag = dorcas_sdk_python.PayloadBag()
    bag.add_simple('name', 'Emmanuel')
    assert bag.get_item_by_name('name').value == 'Emmanuel'
    bag.set_items(dict(age=20, size=25, firstname='Emmanuel'))
    assert 'name' not in bag.to_payload()
    assert bag.get_item_by_name('firstname').value == 'Emmanuel'
