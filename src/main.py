from flask import Flask, request, abort, jsonify
from ar_model import predict
from dtos import JsonRequestKeys


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/predict", methods=['POST'])
def make_predictions():
    json = request.get_json()

    if json is None:
        abort(400, "invalid json input")
    if JsonRequestKeys.TimeSeries.value not in json:
        abort(400, f"invalid json input: key '{JsonRequestKeys.TimeSeries.value}' is missing.")
    if JsonRequestKeys.PredictionSteps.value not in json:
        abort(400, f"invalid json input: key '{JsonRequestKeys.PredictionSteps.value }' is missing.")
    if JsonRequestKeys.NumberOfSamples.value not in json:
        abort(400, f"invalid json input: key '{JsonRequestKeys.NumberOfSamples.value}' is missing.")

    time_series = json[JsonRequestKeys.TimeSeries.value]
    if not isinstance(time_series, list):
        abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}' is not a list.")
    if not time_series:
        abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}' must contain at least one element.")
    for i in range(0, len(time_series)):
        if JsonRequestKeys.TimeSeriesID.value not in time_series[i]:
            abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}]' must have the key '{JsonRequestKeys.TimeSeriesID.value}'.")
        if JsonRequestKeys.TimeSeriesValues.value not in time_series[i]:
            abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}]' must have the key '{JsonRequestKeys.TimeSeriesValues.value}'.")

        id = time_series[i][JsonRequestKeys.TimeSeriesID.value]
        if not isinstance(id, str):
            abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}].{JsonRequestKeys.TimeSeriesID.value}' must be a string.")
        if not id:
            abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}].{JsonRequestKeys.TimeSeriesID.value}' must not be an empty string.")

        values = time_series[i][JsonRequestKeys.TimeSeriesValues.value]
        if not isinstance(values, list):
            abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}].{JsonRequestKeys.TimeSeriesValues.value}' must be a list.")
        if len(values) < 2:
            abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}].{JsonRequestKeys.TimeSeriesValues.value}' must contain at least two elements.")
        for j in range(len(values)):
            if not isinstance(values[j], (float, int)):
                abort(400, f"invalid json input: '{JsonRequestKeys.TimeSeries.value}[{i}].{JsonRequestKeys.TimeSeriesValues.value}[{j}]' must be an integer or a float.")

    pred_steps = json[JsonRequestKeys.PredictionSteps.value]
    if not isinstance(pred_steps, int):
        abort(400, f"invalid json input: '{JsonRequestKeys.PredictionSteps.value}' must be an integer.")
    if pred_steps <= 0 or pred_steps > 20:
        abort(400, f"invalid json input: '{JsonRequestKeys.PredictionSteps.value}' must be between 1 and 20.")

    num_samples = json[JsonRequestKeys.NumberOfSamples.value]
    if not isinstance(num_samples, int):
        abort(400, f"invalid json input: '{JsonRequestKeys.NumberOfSamples.value}' must be an integer.")
    if num_samples <= 0 or num_samples > 500:
        abort(400, f"invalid json input: '{JsonRequestKeys.NumberOfSamples.value}' must be between 1 and 500.")

    response = {}
    result = predict(time_series=time_series, pred_steps=pred_steps, num_samples=num_samples)
    response['timeSeries'] = result

    return jsonify(response)


@app.errorhandler(Exception)
def global_exception_handler(error):
    return f'An error occured: {error}', 500


if __name__ == "__main__":
    app.run(debug=True)
