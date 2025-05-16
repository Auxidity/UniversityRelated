import pytest
from shopping import ShoppingList

def test_add_item():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    assert shopping_list.items == {"bananas": 5}

def test_add_multiple_items():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    shopping_list.add("apples", 3)
    assert shopping_list.items == {"bananas": 5, "apples": 3}

def test_add_existing_item():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    shopping_list.add("bananas", 3)
    assert shopping_list.items == {"bananas": 8}

def test_number_of_items():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    shopping_list.add("apples", 3)
    assert shopping_list.number_of_items() == 2

def test_item_index():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    shopping_list.add("apples", 3)
    assert shopping_list.item(1) == "bananas"
    assert shopping_list.item(2) == "apples"

def test_amount_index():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    shopping_list.add("apples", 3)
    assert shopping_list.amount(1) == 5
    assert shopping_list.amount(2) == 3

def test_item_index_out_of_range():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    with pytest.raises(IndexError):
        shopping_list.item(3)

def test_amount_index_out_of_range():
    shopping_list = ShoppingList()
    shopping_list.add("bananas", 5)
    with pytest.raises(IndexError):
        shopping_list.amount(3)
