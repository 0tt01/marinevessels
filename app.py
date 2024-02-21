import streamlit as st
import requests

import json
import pandas as pd


st.title("Marine vessel app")



vesselname = st.text_input("enter vessel name")


url = 'https://meri.digitraffic.fi/api/ais/v1/vessels'
location_url = 'https://meri.digitraffic.fi/api/ais/v1/locations'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()    
    target_ship_found = False
    target_mmsi = None
    for vessel in data:
        
        if "name" in vessel and vessel["name"] == vesselname:
            target_mmsi = vessel.get("mmsi")
            st.warning(f"Vessel found: {vesselname}")
            result = (json.dumps(vessel, indent=2))
            target_ship_found = True
            break  
    if target_mmsi is not None:
        location_response = requests.get(location_url)
        if location_response.status_code == 200:
            location_data = location_response.json()
            if "features" in location_data:
                for feature in location_data["features"]:
                    if "mmsi" in feature and feature["mmsi"] == target_mmsi:
                        coordinates = feature["geometry"]["coordinates"]
                        sog = feature["properties"]["sog"]
                        cog = feature["properties"]["cog"]
                        heading = feature["properties"]["heading"]
                        timestamp = feature["properties"]["timestamp"]
    if not target_ship_found:
        st.warning(f"Vessel not found: {vesselname}")
else:
    st.warning(f"Error: {response.status_code}")




st.json(vessel)
st.json(coordinates)
longitude = coordinates[0]
latitude = coordinates[1]
df = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})

st.map(df)
