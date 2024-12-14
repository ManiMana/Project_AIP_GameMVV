import pytest
from unittest.mock import patch, mock_open, MagicMock, ANY
import json
import os
from ППППП import VirtualVirusApp, save_money, load_money, INITIAL_POINTS, create_new_strawberry, create_new_mushroom, create_new_oclock,
import unittest

@pytest.fixture(autouse=True)
def no_pygame_init():
    with patch('pygame.init'), patch('pygame.display.set_mode', return_value=MagicMock()), \
         patch('pygame.Surface', return_value=MagicMock()), \
         patch('pygame.font.Font', return_value=MagicMock()):
        yield

# Тестирование функции save_money
def test_save_money():
    money = 100
    with patch("builtins.open", mock_open()) as mocked_file:
        save_money(money)
        mocked_file.assert_called_once_with("money.txt", "w")
        mocked_file().write.assert_called_once_with("100")

# Тестирование функции load_money
def test_load_money():
    # Положительный сценарий
    with patch("builtins.open", mock_open(read_data="200")):
        money = load_money()
        assert money == 200

    # Отрицательный сценарий (файл не найден)
    with patch("builtins.open", side_effect=FileNotFoundError):
        money = load_money()
        assert money == 0

def test_strawberry_creation():
    strawberry = Strawberry(100, 200)
    assert strawberry.rect.topleft == (100, 200)
    assert strawberry.visible is True
    assert strawberry.speed == 5

def test_mushroom_creation():
    mushroom = Mushroom(150, 250)
    assert mushroom.rect.topleft == (150, 250)
    assert mushroom.visible is True
    assert mushroom.speed == 5

def test_oclock_creation():
    oclock = Oclock(200, 300)
    assert oclock.rect.topleft == (200, 300)
    assert oclock.visible is True
    assert oclock.speed == 1

def test_create_new_strawberry():
    strawberry = create_new_strawberry()
    assert isinstance(strawberry, Strawberry)
    assert strawberry.rect.y == 0
    assert 0 <= strawberry.rect.x <= 1440 - strawberry.rect.width

def test_create_new_mushroom():
    mushroom = create_new_mushroom()
    assert isinstance(mushroom, Mushroom)
    assert mushroom.rect.y == 0
    assert 0 <= mushroom.rect.x <= 1440 - mushroom.rect.width

def test_create_new_oclock():
    oclock = create_new_oclock()
    assert isinstance(oclock, Oclock)
    assert oclock.rect.y == 0
    assert 0 <= oclock.rect.x <= 1440 - oclock.rect.width



if __name__ == "__main__":
    pytest.main()