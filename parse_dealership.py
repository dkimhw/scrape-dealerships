
import parse_inventory as pi
import pandas as pd
from datetime import datetime


def get_stream_auto_outlet_inventory_data(soup, dealership_info, url):
  # Initialize empty data frame & dictionary
  cars = pd.DataFrame()
  cars_dict = {}

  # Parse title
  # Parse year, make, model_trim, vehicle_type, model, trim
  title = pi.clean_text_data(pi.parse_subsection_all(soup, 'h4', 'span', 'srp-vehicle-title'))
  valid_len_data = len(title)

  years = pi.get_valid_year(title)
  makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
  trim = [None] * valid_len_data
  models = [None] * valid_len_data

  # Prices
  car_prices = [int(float(i)) for i in pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-price')]

  # Misc car information
  results = pi.get_row_subsection_data(soup, ('div', 'medium-8 medium-pull-4 columns'), ('div', 'srp-vehicle-data'))
  vehicle_data = []
  for section in results:
      sub_data = []
      for el in section:
          el_data = [x.get_text() for x in el.findAll('div', 'column')]
          sub_data += el_data
      vehicle_data.append(sub_data)

  exterior_color = []
  interior_color = []
  transmission = []
  engine = []
  drivetrain = []
  vin = []
  miles = []

  for i in range(len(vehicle_data)):
    for col in vehicle_data[i]:
      if 'Ext. Color' in col:
          cleaned_str = col.replace('Ext. Color: ', '')
          exterior_color.append(cleaned_str)
      elif 'Int. Color' in col:
          cleaned_str = col.replace('Int. Color: ', '')
          interior_color.append(cleaned_str)
      elif 'Transmission' in col:
          cleaned_str = col.replace('Transmission: ', '')
          transmission.append(cleaned_str)
      elif 'Mileage' in col:
          cleaned_str = col.replace('Mileage: ', '').replace(',', '')
          miles.append(int(cleaned_str))
      elif 'Drivetrain' in col:
          cleaned_str = col.replace('Drivetrain: ', '')
          drivetrain.append(cleaned_str)
      elif 'Engine' in col:
          cleaned_str = col.replace('Engine: ', '')
          engine.append(cleaned_str)
      elif 'VIN' in col:
          cleaned_str = col.split(' ')[1].strip()
          vin.append(cleaned_str)


  # Append all parsed data to cars_list
  cars_dict['title'] = title
  cars_dict['year'] = years
  cars_dict['make'] = makes
  cars_dict['model_trim'] = model_trim
  cars_dict['vehicle_type'] = vehicle_type
  cars_dict['model'] = models
  cars_dict['trim'] = trim
  cars_dict['vehicle_mileage'] = miles
  cars_dict['price'] = car_prices
  cars_dict['exterior_color'] = exterior_color
  cars_dict['interior_color'] = interior_color
  cars_dict['transmission'] = transmission
  cars_dict['engine'] = engine
  cars_dict['drivetrain'] = drivetrain
  cars_dict['vin'] = vin

  # Check if data is valid
  is_valid = pi.data_length_validation(cars_dict, valid_len_data)

  if (is_valid):
    # If valid create cars dataframe to return
    for key in cars_dict:
      pi.add_column_df(cars, cars_dict[key], key)

    # Add dealership info
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    # Make other changes
    cars['model_trim'] = cars['model'] + ' ' + cars['trim']

    return cars
  else:
    error_df = pd.DataFrame()
    error_df.at[0, 'error'] = 'Data Validation'
    error_df.at[0, 'dealership'] = dealership_info['dealership_name']
    error_df.at[0, 'date'] = datetime.now(tz = None)
    error_df.at[0, 'url'] = url
    return error_df
