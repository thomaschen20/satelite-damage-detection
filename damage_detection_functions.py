
#import cv2
import glob
import matplotlib.pyplot as plt

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

def show_building_crops_from_image_filename(dataset, image_filename):
  image = cv2.imread(image_filename)[:,:,::-1].astype("uint8")
  print(len(dataset[image_filename]['building_list']))
  for building in dataset[image_filename]['building_list']:
    x = building['bbox'][0]
    y = building['bbox'][1]
    width = building['bbox'][2]
    height = building['bbox'][3]
    
    crop = image[int(y):int(y+height), int(x):int(x+width), :]
    resized_crop = cv2.resize(crop, (100,100), cv2.INTER_LINEAR)
    plt.imshow(resized_crop)
    
    plt.show()

def show_bounding_boxes_from_image_filename(dataset, image_filename):
  color = (255,0,0)
  thickness = 2
  image = cv2.imread(image_filename)[:,:,::-1].astype("uint8")
  print(len(dataset[image_filename]['building_list']))
  for building in dataset[image_filename]['building_list']:
    x = building['bbox'][0]
    y = building['bbox'][1]
    width = building['bbox'][2]
    height = building['bbox'][3]
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
  for image in dataset:
      if "post_disaster" in image:
          if count < trains:
              train[image] = dataset[image]
          else:
              test[image] = dataset[image]
  return (train, test)