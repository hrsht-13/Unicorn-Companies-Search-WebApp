import pandas as pd
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

def get_data():
  url="https://www.cbinsights.com/research-unicorn-companies"
  df=pd.read_html(url)[0]
  df["Date Joined"]=pd.to_datetime(df["Date Joined"],infer_datetime_format=True)
  df["Date Joined"]=df["Date Joined"].dt.strftime("%d-%m-%Y")
  df["Valuation ($B)"] = df["Valuation ($B)"].apply(lambda x : x.replace("$","")) 
  df["Valuation ($B)"] = df["Valuation ($B)"].astype("float")
  df.to_csv("unicorn.csv")
  

def findGeocode(city):
       
    # try and catch is used to overcome
    # the exception thrown by geolocator
    # using geocodertimedout  
    try:
          
        # Specify the user_agent as your
        # app name it should not be none
        geolocator = Nominatim(user_agent="your_app_name")
          
        return geolocator.geocode(city)
      
    except GeocoderTimedOut:
          
        return findGeocode(city) 
  
  
def location():
  #for cities
  lon = {}
  lat = {}
  for i in tqdm(df["City"].unique()):
      
    if findGeocode(i) != None:
           
        loc = findGeocode(i)
          
        # coordinates returned from 
        # function is stored into
        # two separate list
        lat[i]=loc.latitude
        lon[i]=loc.longitude
       
    # if coordinate for a city not
    # found, insert "NaN" indicating 
    # missing value 
    else:
        lat[i]=np.nan
        lon[i]=np.nan
        
  #for countries
  longitude = {}
  latitude = {}
  for i in tqdm(df["Country of origin"].unique()):
      
    if findGeocode(i) != None:
           
        loc = findGeocode(i)
          
        # coordinates returned from 
        # function is stored into
        # two separate list
        latitude[i]=loc.latitude
        longitude[i]=loc.longitude
       
    # if coordinate for a city not
    # found, insert "NaN" indicating 
    # missing value 
    else:
        latitude[i]=np.nan
        longitude[i]=np.nan
        
  return longitude, latitude , lat, lon
        
        
        
        
        
        
        
