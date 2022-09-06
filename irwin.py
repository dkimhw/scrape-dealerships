
import parse_inventory as pi
import pandas as pd
from datetime import datetime
import re

def get_irwin_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Parse title
    # For this dealership - we need to make the change later

    # Parse year, make, model_trim, vehicle_type, model, trim
    title = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-name')
    valid_len_data = len(title)

    years = pi.convert_to_numeric_type(pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-year'))
    makes = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-make')
    models = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-model')
    trim = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-trim')

    model_trim = [None] * valid_len_data
    vehicle_type = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-bodystyle')

    # Miles
    miles = pi.convert_to_numeric_type(
      pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-mileage')
    )

    # Prices
    car_prices = [int(float(i)) for i in pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-price')]

    # Misc car information
    exterior_color = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-extcolor')
    interior_color = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-intcolor')
    transmission = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-trans')
    engine = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-engine')
    drivetrain = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-drivetrain')
    vin = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-vin')

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
