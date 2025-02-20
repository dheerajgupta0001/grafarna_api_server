GRAFANA_API_SERVER --> main parent folder
    --src
        --config
            --config.py
                ==> load_config() 
                    input  --> None
                    return --> config.json data
        --repos
            --GetDayAHeadData.py
                ==> getDayAHeadData()
                    input   --> start time, end time, state name
                    return  -->  DayAHead Demand Forecast of that particular state
                    --> uses the DAYAHEAD_DEMAND_FORECAST table from database
            --GetForecastRevision.py
                ==> getForecastRevision()
                    input   --> start time, endtime and statename, revisionNo='R0A'
                    return  --> IntraDay Demand Forecast of that particular state
                    --> uses the FORECAST_REVISION_STORE table from database
            --GetStatePointId.py
                ==> getStatePointId()
                    input   --> statename 
                    return  --> point Id of that particular state
                    --> uses ENTITY_MAPPING_TABLE table from database

    --config.json
        ==> consists of database connection URI in JSON format
    --index.py
        ==> healthCheck()
            --> health checkup function
            --> route: "/api"
        ==> getMetrics()
            --> returns available Metrics
            --> route: "/api/metrics"
        ==> getMetricPayloadOptions()
            --> returns payload PayloadOptions
            --> route: "/api/metric-payload-options"
        ==> queryData()
            --> returns the payload data for provided options in request
            --> route: "/api/query"






