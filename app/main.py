from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from app.service.entities import EuropeConverter, AsiaConverter, WorldwideConverter
from app.service.exceptions import RegionNotFoundError, InvalidCurrencyError, ConversionError
from app.service.schemas import ConversionRequest, ConversionResponse


app = Flask(__name__)

def get_converter(region: str):
    converters = {
        "europe": EuropeConverter(),
        "asia": AsiaConverter(),
        "worldwide": WorldwideConverter()
    }
    
    if region not in converters:
        raise RegionNotFoundError(region)
    
    return converters[region]

@app.route("/", methods=['get'])
def index():
    return render_template("index.html")

@app.route("/convert", methods=['post'])
def convert():
    try:
        data = request.json
        conversion_request = ConversionRequest(**data)
        
        converter = get_converter(conversion_request.region)
        
        result = converter.calculate(
            conversion_request.amount,
            conversion_request.from_currency,
            conversion_request.to_currency
        )
        
        response = ConversionResponse(**result)
        return jsonify(response.model_dump()), 200
    
    except InvalidCurrencyError as e:
        return jsonify({"error": str(e)}), 400
    except RegionNotFoundError as e:
        return jsonify({"error": str(e)}), 400
    except ConversionError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"{e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)


