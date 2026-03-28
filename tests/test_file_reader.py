"""
Tests for file_reader module.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_reader import read_csv_file, read_excel_file


def test_read_csv_file_valid() -> None:
    """Test reading valid CSV file."""
    csv_content = (
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;"
        "Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации\n"
        "3598919;EXECUTED;2020-12-06T23:00:58Z;29740;Peso;COP;"
        "Discover 3172601889670065;Discover 0720428384694643;Перевод с карты на карту"
    )

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        result = read_csv_file(tmp_path)
        assert len(result) == 2
        assert result[0]["id"] == 650703
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["amount"] == 16210
        assert result[0]["currency_code"] == "PEN"
    finally:
        os.unlink(tmp_path)


def test_read_csv_file_not_found() -> None:
    """Test reading non-existent CSV file."""
    result = read_csv_file("nonexistent.csv")
    assert result == []


def test_read_csv_file_empty() -> None:
    """Test reading empty CSV file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write("")
        tmp_path = tmp.name

    try:
        result = read_csv_file(tmp_path)
        assert result == []
    finally:
        os.unlink(tmp_path)


def test_read_csv_file_invalid() -> None:
    """Test reading invalid CSV file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write("invalid,csv,content\nwithout,proper,headers")
        tmp_path = tmp.name

    try:
        result = read_csv_file(tmp_path)
        assert isinstance(result, list)
    finally:
        os.unlink(tmp_path)


def test_read_excel_file_valid() -> None:
    """Test reading valid Excel file."""
    df = pd.DataFrame(
        {
            "id": [650703, 3598919],
            "state": ["EXECUTED", "EXECUTED"],
            "date": ["2023-09-05T11:30:32Z", "2020-12-06T23:00:58Z"],
            "amount": [16210, 29740],
            "currency_name": ["Sol", "Peso"],
            "currency_code": ["PEN", "COP"],
            "from": ["Счет 58803664561298323391", "Discover 3172601889670065"],
            "to": ["Счет 39745660563456619397", "Discover 0720428384694643"],
            "description": ["Перевод организации", "Перевод с карты на карту"],
        }
    )

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name
        df.to_excel(tmp_path, index=False, engine="openpyxl")

    try:
        result = read_excel_file(tmp_path)
        assert len(result) == 2
        assert result[0]["id"] == 650703
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["amount"] == 16210
        assert result[0]["currency_code"] == "PEN"
    finally:
        os.unlink(tmp_path)


def test_read_excel_file_not_found() -> None:
    """Test reading non-existent Excel file."""
    result = read_excel_file("nonexistent.xlsx")
    assert result == []


def test_read_excel_file_empty() -> None:
    """Test reading empty Excel file."""
    df = pd.DataFrame()

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".xlsx", delete=False) as tmp:
        tmp_path = tmp.name
        df.to_excel(tmp_path, index=False, engine="openpyxl")

    try:
        result = read_excel_file(tmp_path)
        assert result == []
    finally:
        os.unlink(tmp_path)


def test_read_excel_file_invalid() -> None:
    """Test reading invalid Excel file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".xlsx", delete=False) as tmp:
        tmp.write("not a valid excel file")
        tmp_path = tmp.name

    try:
        result = read_excel_file(tmp_path)
        assert result == []
    finally:
        os.unlink(tmp_path)


@patch("src.file_reader.pd.read_csv")
def test_read_csv_file_mock(mock_read_csv: MagicMock) -> None:
    """Test CSV reading with mock."""
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    mock_read_csv.return_value = mock_df

    result = read_csv_file("any_path.csv")
    assert result == [{"id": 1, "amount": 100}]
    mock_read_csv.assert_called_once_with("any_path.csv", sep=";", encoding="utf-8")


@patch("src.file_reader.pd.read_excel")
def test_read_excel_file_mock(mock_read_excel: MagicMock) -> None:
    """Test Excel reading with mock."""
    mock_df = MagicMock()
    mock_df.empty = False
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    mock_read_excel.return_value = mock_df

    result = read_excel_file("any_path.xlsx")
    assert result == [{"id": 1, "amount": 100}]
    mock_read_excel.assert_called_once_with("any_path.xlsx", engine="openpyxl")
