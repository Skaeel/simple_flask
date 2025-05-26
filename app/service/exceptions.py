class ConversionError(Exception):
    pass


class InvalidCurrencyError(ConversionError):
    def __init__(self, currency: str):
        super().__init__(f"Invalid currency: {currency}")


class RegionNotFoundError(ConversionError):
    def __init__(self, region: str):
        super().__init__(f"Region not found: {region}")