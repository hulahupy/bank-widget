"""Модуль для обработки банковских операций."""

from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по заданному статусу.

    Аргументы:
        operations: Список словарей с данными о банковских операциях
        state: Статус для фильтрации (по умолчанию 'EXECUTED')

    Возвращает:
        Новый список, содержащий только операции с указанным статусом
    """
    return [op for op in operations if op.get('state') == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Аргументы:
        operations: Список словарей с данными о банковских операциях
        descending: Порядок сортировки. True - убывание (сначала новые)

    Возвращает:
        Новый отсортированный список
    """
    return sorted(operations, key=lambda x: x.get('date', ''), reverse=descending)