import pytest
from app.service.entities import EuropeConverter, AsiaConverter, WorldwideConverter, InvalidCurrencyError, CurrencyConverter

# Пример курсов валют для тестирования
EXCHANGE_RATES = {
    "USD": {"EUR": 0.9, "JPY": 130.0},
    "EUR": {"USD": 1.1, "JPY": 145.0},
    "JPY": {"USD": 0.0077, "EUR": 0.0069}
}

@pytest.fixture
def europe_converter():
    return EuropeConverter()

@pytest.fixture
def asia_converter():
    return AsiaConverter()

@pytest.fixture
def worldwide_converter():
    return WorldwideConverter()

def test_currency_converter_abstract_methods():
    with pytest.raises(TypeError):
        converter = CurrencyConverter()

# Тесты для EuropeConverter
def test_europe_converter_valid_conversion(europe_converter):
    result = europe_converter.calculate(100, "USD", "EUR")
    assert result["converted_amount"] == 90.0
    assert result["comission"] == 1.35
    assert result["total"] == 91.35
    assert result["exchange_rate"] == 0.9

def test_europe_converter_invalid_currency(europe_converter):
    with pytest.raises(InvalidCurrencyError) as excinfo:
        europe_converter.calculate(100, "XYZ", "EUR")
    assert "Invalid currency: XYZ" in str(excinfo.value)

def test_europe_converter_min_amount(europe_converter):
    result = europe_converter.calculate(0.01, "USD", "EUR")
    assert result["converted_amount"] == 0.01
    assert result["comission"] == 0.0
    assert result["total"] == 0.01

def test_europe_converter_max_amount(europe_converter):
    result = europe_converter.calculate(999999999.99, "USD", "EUR")
    assert result["converted_amount"] == 899999999.99
    assert result["comission"] == 13499999.99
    assert result["total"] == 913499999.98

def test_europe_converter_negative_amount(europe_converter):
    with pytest.raises(ValueError) as excinfo:
        europe_converter.calculate(-100, "USD", "EUR")
    assert "amount must be greater than 0" in str(excinfo.value)

# Тесты для AsiaConverter
def test_asia_converter_valid_conversion(asia_converter):
    result = asia_converter.calculate(100, "USD", "JPY")
    assert result["converted_amount"] == 13000.0
    assert result["comission"] == 260.5
    assert result["total"] == 13260.5
    assert result["exchange_rate"] == 130.0

def test_asia_converter_invalid_currency(asia_converter):
    with pytest.raises(InvalidCurrencyError) as excinfo:
        asia_converter.calculate(100, "XYZ", "JPY")
    assert "Invalid currency: XYZ" in str(excinfo.value)

def test_asia_converter_min_amount(asia_converter):
    result = asia_converter.calculate(0.01, "USD", "JPY")
    assert result["converted_amount"] == 1.3
    assert result["comission"] == 0.5
    assert result["total"] == 1.8

def test_asia_converter_max_amount(asia_converter):
    result = asia_converter.calculate(999999999.99, "USD", "JPY")
    assert result["converted_amount"] == 129999999998.7
    assert result["comission"] == 2600000000.47
    assert result["total"] == 132599999999.17

def test_asia_converter_negative_amount(asia_converter):
    with pytest.raises(ValueError) as excinfo:
        asia_converter.calculate(-100, "USD", "JPY")
    assert "amount must be greater than 0" in str(excinfo.value)

# Тесты для WorldwideConverter
def test_worldwide_converter_valid_conversion(worldwide_converter):
    result = worldwide_converter.calculate(100, "EUR", "USD")
    assert result["converted_amount"] == 110.0
    assert result["comission"] == 3.3
    assert result["total"] == 113.3
    assert result["exchange_rate"] == 1.1

def test_worldwide_converter_invalid_currency(worldwide_converter):
    with pytest.raises(InvalidCurrencyError) as excinfo:
        worldwide_converter.calculate(100, "EUR", "XYZ")
    assert "Invalid currency: XYZ" in str(excinfo.value)

def test_worldwide_converter_min_amount(worldwide_converter):
    result = worldwide_converter.calculate(0.01, "EUR", "USD")
    assert result["converted_amount"] == 0.01
    assert result["comission"] == 0.0
    assert result["total"] == 0.01

def test_worldwide_converter_max_amount(worldwide_converter):
    result = worldwide_converter.calculate(999999999.99, "EUR", "USD")
    assert result["converted_amount"] == 1099999999.99
    assert result["comission"] == 32999999.99
    assert result["total"] == 1132999999.98

def test_worldwide_converter_negative_amount(worldwide_converter):
    with pytest.raises(ValueError) as excinfo:
        worldwide_converter.calculate(-100, "EUR", "USD")
    assert "amount must be greater than 0" in str(excinfo.value)