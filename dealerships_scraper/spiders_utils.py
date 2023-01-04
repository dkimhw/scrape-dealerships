import re


def get_item_data_from_xpath(response, xpath, item, item_key, item_type, extract_key = 0):
    item_data = None
    try:
      item_data = response.xpath(xpath).extract()[extract_key].strip()
      if item_type == 'int':
        item_data = re.sub('\D', '', item_data)
        if item_data == '':
          item_data = 0
        else:
          item_data = int(item_data)
      elif item_type == 'float':
        item_data = re.sub('\D', '', item_data)
        if item_data == '':
          item_data = 0.0
        else:
          item_data = float(item_data)
    except:
      pass

    item[item_key] = item_data


def get_car_make_model(title):
  full_title = title.strip()
  valid_makes = ['BMW', 'Audi', 'Toyota', 'Lexus', 'Ford', 'Honda'
    , 'Hyundai', 'Kia', 'Chevrolet', 'Jeep', 'Nissan', 'Volkswagen'
    , 'Mitsubishi', 'Mazda', 'GMC', 'Cadillac', 'Land Rover', 'Dodge'
    , 'Jaguar', 'Volvo', 'Alfa Romeo', 'MINI Cooper', 'Buick'
    , 'Fiat', 'Tesla', 'Lincoln', 'Maserati', 'smart', 'Aston Martin'
    , 'Porsche', 'Pontiac', 'Lamborghini', 'Rolls-Royce', 'Bentley'
    , 'HUMMER', 'Mercury'
    , 'Subaru', 'Ram', 'Chrysler', 'Acura', 'Mercedes-Benz', 'Infiniti']
  valid_vehicle_type = ['Sedan', 'SUV', 'Coupe', 'Wagon', 'Hatchback', 'Truck', 'Cargo Van', 'Van']

  year = full_title[0:5].strip()

  # Remove year
  full_title = full_title[5:]

  # Remove make and moel
  clean_model = ''
  clean_make = ''
  for make in valid_makes:
    make = make.strip()
    if make.lower() in full_title.lower():
      clean_make = make
      clean_model = full_title.replace(make, '')

  for vt in valid_vehicle_type:
    if vt.lower() in clean_model.lower():
      clean_model = clean_model.replace(vt, '')

  clean_model = clean_model.strip()
  print(clean_make)
  return year, clean_make, clean_model


def get_vehicle_type(string):
  valid_vehicle_type = ['Sedan', 'SUV', 'Coupe', 'Wagon', 'Hatchback', 'Convertible', 'Truck', 'Cargo Van', 'Van']
  for vt in valid_vehicle_type:
    if vt.lower() in string.lower():
      return vt
  return None
