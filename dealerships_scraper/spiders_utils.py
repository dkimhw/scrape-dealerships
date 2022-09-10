import re


def get_item_data_from_xpath(response, xpath, item, item_key, item_type):
    item_data = None
    try:
      item_data = response.xpath(xpath).get().strip()
      if item_type == 'int':
        item_data = re.sub('\D', '', item_data)
        item_data = int(item_data)
      elif item_type == 'float':
        item_data = re.sub('\D', '', item_data)
        item_data = float(item_data)
    except:
      pass

    item[item_key] = item_data
