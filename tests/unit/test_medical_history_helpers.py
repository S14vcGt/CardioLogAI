import pytest
from datetime import datetime, date
from unittest.mock import patch, MagicMock
from app.Scripts.medical_history_helpers import calcular_edad, calcular_bsa_mosteller


class TestMedicalHistoryHelpers:

    @patch("app.Scripts.medical_history_helpers.get_vzla_datetime")
    def test_calcular_edad_simple(self, mock_vzla_datetime):
        # Mock today as 2023-01-01
        mock_now = datetime(2023, 1, 1)
        mock_vzla_datetime.return_value = mock_now

        # Born exactly 20 years ago (2003-01-01)
        assert calcular_edad("2003-01-01") == 20

    @patch("app.Scripts.medical_history_helpers.get_vzla_datetime")
    def test_calcular_edad_not_birthday_yet(self, mock_vzla_datetime):
        # Mock today as 2023-01-01
        mock_now = datetime(2023, 1, 1)
        mock_vzla_datetime.return_value = mock_now

        # Born 2003-12-31 (19 years old, turning 20 end of year)
        assert calcular_edad("2003-12-31") == 19

    @patch("app.Scripts.medical_history_helpers.get_vzla_datetime")
    def test_calcular_edad_birthday_tomorrow(self, mock_vzla_datetime):
        # Mock today as 2023-01-01
        mock_now = datetime(2023, 1, 1)
        mock_vzla_datetime.return_value = mock_now

        # Born 2003-01-02 (19 years old, turning 20 tomorrow)
        assert calcular_edad("2003-01-02") == 19

    @patch("app.Scripts.medical_history_helpers.get_vzla_datetime")
    def test_calcular_edad_leap_year(self, mock_vzla_datetime):
        # Mock today as 2024-02-29 (Leap year)
        mock_now = datetime(2024, 2, 29)
        mock_vzla_datetime.return_value = mock_now

        # Born 2000-02-29 (24 years old)
        assert calcular_edad("2000-02-29") == 24

        # Born 2000-03-01 (Not birthday yet)
        assert calcular_edad("2000-03-01") == 23

    def test_calcular_edad_invalid_format(self):
        with pytest.raises(Exception) as excinfo:
            calcular_edad("01-01-2000")
        assert "Formato de fecha incorrecto" in str(excinfo.value)

    def test_calcular_bsa_mosteller_standard(self):
        # Weight 70kg, Height 170cm
        # BSA = sqrt((70 * 170) / 3600) = sqrt(11900 / 3600) = sqrt(3.3055) = 1.818
        # Round to 2 decimals -> 1.82
        assert calcular_bsa_mosteller(70, 170) == 1.82

    def test_calcular_bsa_mosteller_zero_negative(self):
        assert calcular_bsa_mosteller(0, 170) == 0.0
        assert calcular_bsa_mosteller(70, 0) == 0.0
        assert calcular_bsa_mosteller(-70, 170) == 0.0
