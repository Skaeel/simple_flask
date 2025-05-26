from pydantic import BaseModel, Field


class ConversionRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма для конвертации")
    from_currency: str = Field(..., min_length=3, max_length=3, description="Исходная валюта")
    to_currency: str = Field(..., min_length=3, max_length=3, description="Целевая валюта")
    region: str = Field(..., description="Регион")


class ConversionResponse(BaseModel):
    converted_amount: float
    comission: float
    total: float
    exchange_rate: float