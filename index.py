from flask import Flask, request
from copy import deepcopy
import datetime as dt
import pandas as pd
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config.config import load_config
from src.repos.GetDayAHeadData import getDayAHeadData
from src.repos.GetForecastRevision import getForecastRevision


pointIdPayload = {
    "label": "Point Id",
    "name": "point_id",
    "type": "select",
    "placeholder": "Select State",
    "reloadMetric": True,
    "options": [
        {"label": "CHATTISGARH", "value": "CHATTISGARH"},
        {"label": "GUJRAT", "value": "GUJRAT"},
        {"label": "GOA", "value": "GOA"},
        {"label": "MADHYA PRADESH", "value": "MADHYA PRADESH"},
        {"label": "MAHARASTRA", "value": "MAHARASTRA"},
        {"label": "WR-TOTAL", "value": "WR-TOTAL"}
    ]
}


historyMetric = {
    "label": "IntraDay Demand Forecast",
    "value": "IDF",
    "payloads": [pointIdPayload,]
}
realTimeMetric = {
    "label": "DayAHead Demand Forecast",
    "value": "DAF",
    "payloads": [pointIdPayload,]
}

metrics = [historyMetric, realTimeMetric]

app = Flask(__name__)

@app.route('/')
def index():
    return "hello"


@app.route("/api")
def healthCheck():
    return ""

@app.route("/api/metrics", methods=["POST"])
def getMetrics():
    return metrics

@app.route("/api/metric-payload-options", methods=["POST"])
def getMetricPayloadOptions():
    queryData = request.get_json()
    payloadOptions = []
    reqPayloadName = queryData.get("name", "")
    if reqPayloadName == 'point_id':
        payloadOptions = [
        {"label": "CHATTISGARH", "value": "CHATTISGARH"},
        {"label": "GUJRAT", "value": "GUJRAT"},
        {"label": "GOA", "value": "GOA"},
        {"label": "MADHYA PRADESH", "value": "MADHYA PRADESH"},
        {"label": "MAHARASTRA", "value": "MAHARASTRA"},
        {"label": "WR-TOTAL", "value": "WR-TOTAL"}
    ]
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
        print("\n\n\n---\n", targetPayload, "\n\n\n---\n")
        
        point_Id = targetPayload['point_id']    #this denotes the state name 
        value = t.get("target", "")    #this denotes the history or real value
        targetData = {
            "target": t["refId"],
            "datapoints": []
        }


        startTime = str(startTime)[:-3]
        endTime = str(endTime)[:-3]

        #DayAHeadForecast 
        if value == 'DAF':
            data = getDayAHeadData(startTime, endTime, point_Id)
            for i in data:
                i[1] = int((i[1].timestamp() + 19800)*1000) #add 5 hours and 30 mins to time to convert it to our time zone
                targetData["datapoints"].append(i)
            

        elif value == 'IDF':
            data = getForecastRevision(startTime, endTime, point_Id)
            for i in data:
                i[1] = int((i[1].timestamp() + 19800)*1000) #add 5 hours and 30 mins to time to convert it to our time zone
                targetData["datapoints"].append(i)
        
        response.append(targetData)

    return response

app.run(host="0.0.0.0", port=8080, debug=True)

