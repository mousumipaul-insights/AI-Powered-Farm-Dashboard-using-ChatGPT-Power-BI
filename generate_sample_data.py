"""
generate_sample_data.py — Author: Mousumi Paul
Generates all raw CSV datasets for the AI Farm Dashboard
"""
import pandas as pd, numpy as np, os
from datetime import datetime, timedelta
np.random.seed(42)

CROPS=["Rice","Wheat","Tomato","Potato","Onion","Maize","Soybean","Cotton","Sugarcane","Groundnut"]
REGIONS=["Punjab","Maharashtra","UP","Karnataka","West Bengal","Gujarat","MP","Andhra Pradesh","Bihar","Rajasthan"]
SEASONS=["Kharif","Rabi","Zaid"]
SEASON_MONTHS={"Kharif":[6,7,8,9,10],"Rabi":[11,12,1,2,3],"Zaid":[4,5]}
VARIETIES={"Rice":["Basmati","IR-64","Sona Masoori"],"Wheat":["HD-2967","PBW-343","Lok-1"],"Tomato":["Roma","Hybrid F1","Cherry"],"Potato":["Kufri Jyoti","Kufri Pukhraj"],"Onion":["Nashik Red","Bhima Dark Red"],"Maize":["DHM-117","HQPM-1"],"Soybean":["JS-335","NRC-37"],"Cotton":["Bt-Cotton","MCU-5"],"Sugarcane":["Co-86032","Co-0238"],"Groundnut":["TAG-24","GG-20"]}

def gen_yield(n=400):
    rows=[]
    for i in range(n):
        crop=np.random.choice(CROPS); region=np.random.choice(REGIONS); year=np.random.randint(2020,2025)
        season=np.random.choice(SEASONS); month=np.random.choice(SEASON_MONTHS[season])
        area=round(np.random.uniform(1,50),2)
        yield_pa=round(max(5.0, np.random.uniform(10,40)+(year-2020)*np.random.uniform(0.1,0.5)+np.random.normal(0,2)),2)
        total_yield=round(yield_pa*area,2)
        cost_pa=round(np.random.uniform(8000,35000),2)
        price_qtl=round(np.random.uniform(800,6000),2)
        revenue=round((total_yield*price_qtl)/100,2)
        profit=round(revenue-cost_pa*area,2)
        rows.append({"Record_ID":f"YLD{str(i+1).zfill(5)}","Year":year,"Month":month,"Season":season,"Crop":crop,"Variety":np.random.choice(VARIETIES[crop]),"Region":region,"Area_Acres":area,"Yield_Per_Acre_Qtl":yield_pa,"Total_Yield_Qtl":total_yield,"Cost_Per_Acre_INR":cost_pa,"Market_Price_Per_Qtl":price_qtl,"Total_Revenue_INR":revenue,"Net_Profit_INR":profit,"Irrigation_Type":np.random.choice(["Canal","Drip","Sprinkler","Rainfed"]),"Fertilizer_Used_Kg":round(np.random.uniform(20,120),1),"Soil_Type":np.random.choice(["Alluvial","Black","Red","Laterite","Sandy"])})
    return pd.DataFrame(rows)

def gen_weather(n=360):
    rows=[]
    for i in range(n):
        year=np.random.randint(2020,2025); month=np.random.randint(1,13); region=np.random.choice(REGIONS)
        monsoon=month in [6,7,8,9]
        rain=round(np.random.uniform(150,350) if monsoon else np.random.uniform(5,80),2)
        max_t=round(np.random.uniform(25,42) if month in [4,5,6] else np.random.uniform(15,30),1)
        min_t=round(max_t-np.random.uniform(8,15),1)
        hum=round(np.random.uniform(40,95),1)
        rows.append({"Weather_ID":f"WTH{str(i+1).zfill(5)}","Year":year,"Month":month,"Region":region,"Rainfall_MM":rain,"Max_Temp_C":max_t,"Min_Temp_C":min_t,"Avg_Temp_C":round((max_t+min_t)/2,1),"Humidity_Pct":hum,"Sunshine_Hrs":round(np.random.uniform(4,10),1),"Wind_Speed_KMH":round(np.random.uniform(5,35),1),"Is_Monsoon_Month":int(monsoon),"Drought_Flag":int(rain<20 and not monsoon),"Flood_Risk_Flag":int(rain>300),"Weather_Score":round(0.4*(rain/200)+0.3*(1-abs(max_t-28)/20)+0.3*(hum/100),3)})
    return pd.DataFrame(rows)

def gen_prices(n=300):
    base={"Rice":1800,"Wheat":2000,"Tomato":1200,"Potato":800,"Onion":1100,"Maize":1400,"Soybean":4000,"Cotton":6000,"Sugarcane":350,"Groundnut":4500}
    rows=[]
    for i in range(n):
        crop=np.random.choice(CROPS); year=np.random.randint(2020,2025); month=np.random.randint(1,13)
        b=base[crop]; price=round(b*np.random.uniform(0.75,1.40),2)
        rows.append({"Price_ID":f"PRC{str(i+1).zfill(5)}","Year":year,"Month":month,"Crop":crop,"Mandi_Price_Per_Qtl":price,"MSP_Per_Qtl":round(b*0.90,2),"Export_Price_USD":round(price*0.012,4),"Region":np.random.choice(REGIONS),"Price_Vs_MSP_Pct":round((price/(b*0.90)-1)*100,2)})
    return pd.DataFrame(rows)

def gen_farmers(n=100):
    rows=[]
    for i in range(n):
        crop=np.random.choice(CROPS)
        rows.append({"Farmer_ID":f"FRM{str(i+1).zfill(4)}","Region":np.random.choice(REGIONS),"Primary_Crop":crop,"Secondary_Crop":np.random.choice([c for c in CROPS if c!=crop]),"Land_Acres":round(np.random.uniform(1,30),2),"Experience_Yrs":np.random.randint(1,35),"Education":np.random.choice(["Primary","Secondary","Graduate","None"]),"Uses_Technology":np.random.choice([1,0],p=[0.45,0.55]),"Has_Irrigation":np.random.choice([1,0],p=[0.60,0.40]),"Annual_Income_INR":round(np.random.uniform(80000,800000),-3)})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    dfs = {"crop_yield_records":gen_yield(400),"weather_data":gen_weather(360),"market_prices":gen_prices(300),"farmer_profiles":gen_farmers(100)}
    for name, df in dfs.items():
        df.to_csv(f"data/raw/{name}.csv", index=False)
        print(f"  {name}.csv  -> {len(df)} records")
    print("Done")
