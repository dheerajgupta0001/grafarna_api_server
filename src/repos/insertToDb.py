from flask import Flask, request
from copy import deepcopy
import datetime as dt
import pandas as pd
import random

pointIdPayload = {
    "label": "Point Id",
    "name": "point_id",
    "type": "input"
}
samplingTypePayload = {
    "label": "Sampling Type",
    "name": "sampling_type",
    "type": "select",
    "placeholder": "Select Sampling Type",
    "reloadMetric": True,
    "options": [
        {"label": "Snap", "value": "snap"},
        {"label": "Average", "value": "avg"},
        {"label": "Maximum", "value": "max"},
        {"label": "Minimum", "value": "min"},
        {"label": "Raw", "value": "raw"}
    ]
}
samplingFreqPayload = {
    "label": "Sampling Frequency (secs)",
    "name": "sampling_freq",
    "type": "input"
}
avoidFuturePayload = {
    "label": "Avoid Future",
    "name": "avoid_future",
    "type": "select",
    "options": [
        {"label": "Yes", "value": "yes"},
        {"label": "No", "value": "no"}
    ]
}

historyMetric = {
    "label": "HISTORY",
    "value": "history",
    "payloads": [pointIdPayload, samplingTypePayload, samplingFreqPayload, avoidFuturePayload]
}
realTimeMetric = {
    "label": "REALTIME",
    "value": "real",
    "payloads": [pointIdPayload, avoidFuturePayload]
}

metrics = [historyMetric, realTimeMetric]

app = Flask(__name__)

@app.route("/api")
def healthCheck():
    return ""

@app.route("/api/metrics", methods=["POST"])
def getMetrics():
    metricsFinal = deepcopy(metrics)
    queryData = request.get_json()
    metricName = queryData.get("metric", "")
    samplingType = queryData.get("payload", {}).get("sampling_type", "")
    if metricName == "history" and samplingType == "raw":
        metricsFinal[0]["payloads"] = [pointIdPayload,
                                       samplingTypePayload, avoidFuturePayload]
    return metricsFinal

@app.route("/api/metric-payload-options", methods=["POST"])
def getMetricPayloadOptions():
    queryData = request.get_json()
    # metricName = queryData.get("metric", "")
    # currentPayload = queryData.get("payload", {})
    payloadOptions = []
    reqPayloadName = queryData.get("name", "")
    if reqPayloadName == "avoid_future":
        payloadOptions = [{"label": "Yes", "value": "yes"},
                          {"label": "No", "value": "no"}]
    return payloadOptions

@app.route("/api/query", methods=["POST"])
def queryData():
    queryData = request.get_json()
    print(queryData)
    startTime = dt.datetime.strptime(
        queryData["range"]["from"], "%Y-%m-%dT%H:%M:%S.%fZ")
    endTime = dt.datetime.strptime(
        queryData["range"]["to"], "%Y-%m-%dT%H:%M:%S.%fZ")
    targets = queryData["targets"]
    response = []
    for t in targets:
        targetPayload = t.get("payload", {})
        targetData = {
            "target": t["refId"],
            "datapoints": []
        }
        samplFreq = int(targetPayload.get("sampling_freq", "60"))
        for sampleTime in pd.date_range(startTime, endTime, freq=dt.timedelta(seconds=samplFreq)):
            targetData["datapoints"].append(
                [random.randint(100, 300), int(sampleTime.timestamp()*1000)])
        response.append(targetData)
    # print(response)
    return response

app.run(host="0.0.0.0", port=8080, debug=True)