from abc import ABC, abstractmethod
from pathlib import Path
import json

from .exceptions import InvalidCurrencyError


current_dir = Path(__file__).resolve().parent
rates_file_path = current_dir / 'exchange_rates.json'

with open(rates_file_path, "r") as f:
    EXCHANGE_RATES = json.load(f)

class CurrencyConverter(ABC):
    @abstractmethod
    def calculate(self, amount: float, from_currency: str, to_currency: str) -> dict:
        pass
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES[from_currency]:
            raise InvalidCurrencyError(from_currency if from_currency not in EXCHANGE_RATES else to_currency)
        return EXCHANGE_RATES[from_currency][to_currency]
        
class EuropeConverter(CurrencyConverter):
    def calculate(self, amount: float, from_currency: str, to_currency: str) -> dict:
        if amount < 0:
            raise ValueError("amount must be greater than 0")
        rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
        comission = converted_amount * 0.015
        total = converted_amount + comission
        
        return {
            "converted_amount": round(converted_amount, 2),
            "comission": round(comission, 2),
            "total": round(total, 2),
            "exchange_rate": rate
        }
    
class AsiaConverter(CurrencyConverter):
    def calculate(self, amount: float, from_currency: str, to_currency: str) -> dict:
        if amount < 0:
            raise ValueError("amount must be greater than 0")
        rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
        comission = converted_amount * 0.02 + 0.5
        total = converted_amount + comission
        
        return {
            "converted_amount": round(converted_amount, 2),
            "comission": round(comission, 2),
            "total": round(total, 2),
            "exchange_rate": rate
        }
    
class WorldwideConverter(CurrencyConverter):
    def calculate(self, amount: float, from_currency: str, to_currency: str) -> dict:
        if amount < 0:
            raise ValueError("amount must be greater than 0")
        rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate
        comission = converted_amount * 0.03
        total = converted_amount + comission
        
        return {
            "converted_amount": round(converted_amount, 2),
            "comission": round(comission, 2),
            "total": round(total, 2),
            "exchange_rate": rate
        }