from flask import Flask, request
from copy import deepcopy
import datetime as dt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.repos.GetDayAHeadData import getDayAHeadData
from src.repos.GetForecastRevision import getForecastRevision

#state options: 
pointIdPayload_options = [
        {"label": "CHATTISGARH", "value": "CHATTISGARH"},
        {"label": "GUJRAT", "value": "GUJRAT"},
        {"label": "GOA", "value": "GOA"},
        {"label": "MADHYA PRADESH", "value": "MADHYA PRADESH"},
        {"label": "MAHARASTRA", "value": "MAHARASTRA"},
        {"label": "WR-TOTAL", "value": "WR-TOTAL"}
    ]

#point Id payload
pointIdPayload = {
    "label": "Point Id",
    "name": "point_id",
    "type": "select",
    "placeholder": "Select State",
    "reloadMetric": True,
    "options": pointIdPayload_options
}


#IDF payload
IDFMetric = {
    "label": "IntraDay Demand Forecast",
    "value": "IDF",
    "payloads": [pointIdPayload,]
}

#DAF payload
DAFMetric = {
    "label": "DayAHead Demand Forecast",
    "value": "DAF",
    "payloads": [pointIdPayload,]
}


#metrics
metrics = [IDFMetric, DAFMetric]

app = Flask(__name__)


#healthCheck function
@app.route("/api")
def healthCheck():
    return ""



#metrics function: this function returns metrics
@app.route("/api/metrics", methods=["POST"])
def getMetrics():
    return metrics


#/api/metric-payload-options function: this function reutrns payload metic options
@app.route("/api/metric-payload-options", methods=["POST"])
def getMetricPayloadOptions():
    queryData = request.get_json()
    payloadOptions = []
    reqPayloadName = queryData.get("name", "")
    if reqPayloadName == 'point_id':
        payloadOptions = pointIdPayload_options
    return payloadOptions



#query function: this function returns query data
@app.route("/api/query", methods=["POST"])
def queryData():
    queryData = request.get_json()
   
    #start Time in the format YYYY-MM-DD hh:mm:ss.mmm
    startTime = str(dt.datetime.strptime(
        queryData["range"]["from"], "%Y-%m-%dT%H:%M:%S.%fZ"))[:-3]
    #end Time in the format YYYY-MM-DD hh:mm:ss.mmm
    endTime = str(dt.datetime.strptime(
        queryData["range"]["to"], "%Y-%m-%dT%H:%M:%S.%fZ"))[:-3]
    
    #get targets from request
    targets = queryData["targets"]

    response = []

    #for each target query the database and return data
    for t in targets:
        targetPayload = t.get("payload", {})
        #target data        
        targetData = {
            "target": t["refId"],
            "datapoints": []
        }

        #return if no point_id in request
        if 'point_id' not in targetPayload.keys():
            response.append(targetData)
            return response

        point_Id = targetPayload['point_id']    #this denotes the state name 
        value = t.get("target", "")    #this denotes the DAF or IDF value

        #DayAHead Demand Forecast 
        if value == 'DAF':
            data = getDayAHeadData(startTime, endTime, point_Id)
            for i in data:
                i[1] = int((i[1].timestamp() + 19800)*1000) #add 5 hours and 30 mins to time to convert it to our time zone
                targetData["datapoints"].append(i)
        #IntraDay Demand forecast
        elif value == 'IDF':
            data = getForecastRevision(startTime, endTime, point_Id)
            for i in data:
                i[1] = int((i[1].timestamp() + 19800)*1000) #add 5 hours and 30 mins to time to convert it to our time zone
                targetData["datapoints"].append(i)
        
        response.append(targetData)

    return response

app.run(host="0.0.0.0", port=8080, debug=True)

