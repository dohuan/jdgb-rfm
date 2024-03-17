import logging
from flask import Flask, request
import os
import json

from src.invoker import invoke

LOGGER = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/invoke", methods=["GET"])
def run_app():
    run_date = str(request.args.get('run_date'))
    try:
        out = invoke(dbt_run_date=run_date)
    except Exception as e:
        out = e
    return str(out)


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    logging.info(f"Healthcheck hit")
    print("Healthy")
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
