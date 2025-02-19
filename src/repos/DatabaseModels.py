




#Entity mapping table class
class entityMapping(db.Model):
     __tablename__ = 'ENTITY_MAPPING_TABLE'
     ID = db.column(db.Integer)
     ENTITY_TAG = db.Column(db.String)
     ENTITY_NAME = db.Column(db.String)
     ENTITY_FULL_NAME = db.Column(db.String)
    

#DayAHead demand forecast table class
class dayAHeadForecast(db.Model):
     __tablename__ = 'DAYAHEAD_DEMAND_FORECAST'
     ID = db.column(db.Integer)
     ENTITY_TAG = db.Column(db.String)
     TIME_STAMP = db.Column(db.DateTime) ################################################ CHECK THIS
     FORECASTED_DEMAND_VALUE = db.Column(db.Float)


#Forecast revision table class
class forecastRevison(db.Model):
     __tablename__ = 'FORECAST_REVISION_STORE'
     ID = db.column(db.Integer)
     ENTITY_TAG = db.Column(db.String)
     TIME_STAMP = db.Column(db.DateTime) ################################################ CHECK THIS
     FORECASTED_DEMAND_VALUE = db.Column(db.Float)
     REVISION_NO = db.Column(db.String)




