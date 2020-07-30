
import cv2
import glob
import matplotlib.pyplot as plt
import random
def get_expanded_bounding_box(bbox, img, perc_exp=0.1):
    """Returns the expanded bounding box.
    Args:
        perc_exp: percent expansion
    """
    h, w = img.shape[:2]
    bbox = [int(round(b)) for b in bbox]  # [x, y, width, height]
    bbox[0] = max(int(round(bbox[0] - bbox[2] * perc_exp)), 0)
    bbox[1] = max(int(round(bbox[1] - bbox[3] * perc_exp)), 0)
    bbox[2] = min(int(round(bbox[2] + bbox[2] * perc_exp * 2)), w - bbox[0])
    bbox[3] = min(int(round(bbox[3] + bbox[3] * perc_exp * 2)), h - bbox[1])
    return bbox

def convert_format_to_tuple_of_coords(polygon_string):
  temp = []
  space_inds = []
  comma_inds = []
  for i in range(10, len(polygon_string)):
    if polygon_string[i] == ",":
      comma_inds.append(i)
    elif polygon_string[i] == " " and polygon_string[i-1] != ",":
      space_inds.append(i)
  comma_inds.append(len(polygon_string) - 2)
  ind = 10
  for i in range(len(space_inds)):
    x = float(polygon_string[ind:space_inds[i]])
    y = float(polygon_string[space_inds[i]+1:comma_inds[i]])
    temp.append((x,y))
    ind = comma_inds[i]+2
  return tuple(temp)

def show_damage_level_frequency_in_dataset(dataset):
  counter = {}
  all_damage = []
  for image in dataset:
    for building in dataset[image]['building_list']:
      if 'damage_level' in building.keys():
        all_damage.append(building['damage_level'])
        if building['damage_level'] in counter:
          counter[building['damage_level']] += 1
        else:
          counter[building['damage_level']] = 1
  all_damage = sorted(all_damage)
  plt.hist(all_damage, 9)
  plt.xlabel('Damage Level')
  plt.ylabel('Building Count')
  plt.title('How damaged were the buildings in the dataset?')
  
  plt.show()
  print(counter)

def show_building_size_histogram_for_dataset(dataset):
  all_sizes = []
  max_size = 0
  for image in dataset:
    for building in dataset[image]['building_list']:
        size = building['bbox'][2] * building['bbox'][3]
        if size < 8000:
          all_sizes.append(size)
          max_size = max(max_size, size)
  all_sizes = sorted(all_sizes)
  plt.hist(all_sizes, bins = 100)
  plt.xlabel('Size')
  plt.ylabel('Building Count')
  plt.title('Building Crop Pixel Area')
  
  plt.show()
  print(max_size)
  
def show_damage_type_frequency_in_dataset(dataset):
  counter = {}
  types = []
  for image in dataset:
    for building in dataset[image]['building_list']:
      types.append(dataset[image]['damage_type'])
      if dataset[image]['damage_type'] in counter:
        counter[dataset[image]['damage_type']] += 1
      else:
        counter[dataset[image]['damage_type']] = 1
  types = sorted(types)
  plt.hist(types, 11)
  plt.xlabel('Damage Type')
  plt.ylabel('Building Count')
  plt.title('What type of disaster caused the damage?')

  plt.show()
  
  print(counter)

def show_building_crops_from_image_filename(dataset, image_filename, expanded = False):
  image = cv2.imread(image_filename)[:,:,::-1].astype("uint8")
  for building in dataset[image_filename]['building_list']:
    if not expanded:
      bbox = building['bbox']
    else:
      bbox = get_expanded_bounding_box(building['bbox'], image)
    x = bbox[0]
    y = bbox[1]
    width = bbox[2]
    height = bbox[3]
    
    crop = image[int(y):int(y+height), int(x):int(x+width), :]
    resized_crop = cv2.resize(crop, (100,100), cv2.INTER_LINEAR)
    print(width * height)
    plt.imshow(resized_crop)
    
    plt.show()

def show_bounding_boxes_from_image_filename(dataset, image_filename, expanded = False):
  color = (255,0,0)
  thickness = 2
  image = cv2.imread(image_filename)[:,:,::-1].astype("uint8")
  for building in dataset[image_filename]['building_list']:
    if not expanded:
      bbox = building['bbox']
    else:
      bbox = get_expanded_bounding_box(building['bbox'], image)
    x = bbox[0]
    y = bbox[1]
    width = bbox[2]
    height = bbox[3]
    image = cv2.rectangle(image, (int(x),int(y)), (int(x+width), int(y+height)), color, thickness)
  plt.imshow(image)
  plt.show()

def split_dataset_post_disaster(dataset, percent_train=0.8):
  """
  TODO: decide on equal distribution of damage type? or ? 
  depending on what the other graphs show
  """
  if percent_train > 1:
      return ()
  train = {}
  test = {}
  trains = int(percent_train * len(dataset))
  count = 0
  key_list = list(dataset.keys())
  random.shuffle(key_list)          #randomizes order of images
  for image in key_list:
    if "post_disaster" in image:
        if count < trains:
            train[image] = dataset[image]
        else:
            test[image] = dataset[image]
    count += 1
  return (train, test)

def split_dataset_pre_and_post_disaster(dataset, percent_train=0.8):
  """
  returns train set and test set, each of which contains pairs of pre and post images
  """
  if percent_train > 1:
      return ()
  train = {}
  test = {}
  trains = int(percent_train * len(dataset)/2)
  count = 0
  key_list = sorted(list(dataset.keys()))
  pair_list = []
  for i in range(1, len(key_list), 2):
    pair_list.append((key_list[i - 1], key_list[i])) #append pair of pre and post
  random.shuffle(pair_list)          #randomizes order of pairs
  for (post_image, pre_image) in pair_list:
    if count < trains:
        train[post_image] = dataset[post_image]
        train[pre_image] = dataset[pre_image]
    else:
        test[post_image] = dataset[post_image]
        test[pre_image] = dataset[pre_image]
    count += 1
  return (train, test)