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


print(get_car_make_model(" 2010 Audi A4 Avant "))
