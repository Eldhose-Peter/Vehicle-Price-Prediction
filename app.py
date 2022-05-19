from crypt import methods
import pickle
from flask import Flask, request
import requests
import json
import pandas as pd
from datetime import date

app = Flask(name)

def get_data(url,token):
    response = requests.get(url,headers={'Authorization': token})
    data = response.json()
    return data

@app.route('/',methods=['GET'])
def index():
    car_id=request.args.get('carID')
    token = request.headers.get('Authorization')

    api_url = "http://localhost:4000/channels/mychannel/chaincodes/fabcar?args=[{0}]&fcn=queryCar".format(car_id)
    data = get_data(api_url,token)
    df = convert_json_to_df(data["result"])
    model = pickle.load(open("model.pkl",'rb'))
    result = model.predict(df)
    return str(result[0]);
    
    

#convert json data to dataframe
def convert_json_to_df(data):

    todays_date = date.today();
    vehicle_age = todays_date.year - data.get("year");
    print(vehicle_age)

    km_driven = data.get("kmDriven");
    mileage = data.get("mileage");
    #engine = data.get("engine"); # engine CC
    engine = 1500; # engine CC
    #max_power = data.get("maxPower"); # max power in bhp
    max_power = 100; # max power in bhp
    seats = data.get("seats");
    #avg_cost_price = data.get("lastPrice"); # avg price of the new models
    avg_cost_price = 11.0; # avg price of the new models
    fuel_type = data.get("fuelType");
    transmission_type = data.get("transmissionType");
    sellerType = data.get("ownerLevel"); # 0 , is manufacturer
    brand = data.get("make");
    #model = data.get("model");
    model = "Ecosport";

    my_dict = {
        'vehicle_age':vehicle_age, 
        'km_driven':km_driven, 
        'mileage':mileage, 
        'engine':engine, 
        'max_power':max_power, 
        'seats':seats, 
        'avg_cost_price':avg_cost_price, 

        'fuel_type_Diesel':0,
        'fuel_type_LPG':0, 
        'fuel_type_Petrol':0,
        

        'transmission_type_Manual':0,

        'seller_type_Individual':0,
        'seller_type_Trustmark Dealer':0, 

        'brand_Ford':0,
        'brand_Honda':0,
        'brand_Hyundai':0,
        'brand_Isuzu':0,
        'brand_Jeep':0,
        'brand_Kia':0,
        'brand_MG':0,
        'brand_Mahindra':0,
        'brand_Maruti':0,
        'brand_Nissan':0,
        'brand_Renault':0,
        'brand_Skoda':0,
        'brand_Tata':0,
        'brand_Toyota':0,
        'brand_Volkswagen':0,        
        
        'model_Altroz':0,
        'model_Amaze':0,
        'model_Aspire':0,
        'model_Baleno':0,
        'model_Bolero':0,
        'model_Celerio':0,
        'model_Ciaz':0,
        'model_City':0,
        'model_Civic':0,
        'model_Compass':0,
        'model_Creta':0,
        'model_D-Max':0,
        'model_Duster':0, 
        'model_Dzire LXI':0,
        'model_Dzire VXI':0,
        'model_Dzire ZXI':0,
        'model_Ecosport':0,
        'model_Eeco':0,
        'model_Elantra':0, 
        'model_Ertiga':0,  
        'model_Figo':0,
        'model_Freestyle':0,
        'model_GO':0,  
        'model_Glanza':0,  
        'model_Grand':0,
        'model_Harrier':0, 
        'model_Hector':0,  
        'model_Ignis':0,
        'model_Innova':0,  
        'model_Jazz':0,
        'model_KUV':0, 
        'model_KUV100':0,  
        'model_KWID':0,
        'model_Kicks':0,
        'model_Marazzo':0, 
        'model_Nexon':0,
        'model_Polo':0,
        'model_Rapid':0,
        'model_RediGO':0,  
        'model_S-Presso':0,         
        'model_Safari':0,                            
        'model_Santro':0,                            
        'model_Scorpio':0,                           
        'model_Seltos':0,                            
        'model_Swift':0,                         
        'model_Swift Dzire':0,                           
        'model_Thar':0,                          
        'model_Tiago':0,                         
        'model_Tigor':0,                         
        'model_Triber':0,                            
        'model_Tucson':0,
        'model_Vento':0,                         
        'model_Venue':0,                         
        'model_Verna':0,                         
        'model_Vitara':0,                            
        'model_WR-V':0,                          
        'model_Wagon R':0,                           
        'model_XL6':0,                           
        'model_XUV300':0,                            
        'model_XUV500':0,                            
        'model_Yaris':0,                         
        'model_i10':0,                           
        'model_i20':0,                           
        'model_redi-GO':0
        
    }

    #set fuel type
    if fuel_type == "Diesel":
        my_dict['fuel_type_Diesel'] = 1
    elif fuel_type == "Petrol":
        my_dict['fuel_type_Petrol'] = 1


    #set transmission type
    if transmission_type == "Manual":
        my_dict['transmission_type_Manual'] = 1

    #set seller type
    if sellerType == 0:
        my_dict['seller_type_Trustmark Dealer'] = 1
    else:
        my_dict['seller_type_Individual'] = 1

    #set brand
    brand = "brand_"+brand;
    my_dict[brand] = 1

    #set model
    model = "model_"+model;
    my_dict[model] = 1


    df = pd.DataFrame(my_dict,index=[0])
    return df