import numpy as np
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import Model

from pelops.datasets.featuredataset import FeatureDataset

def load_image(img_path, resizex=224, resizey=224):
    data = image.load_img(img_path, target_size=(resizex, resizey))
    x = image.img_to_array(data)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

# load the imagenet networks
def get_models():
    # include_top needs to be True for this to work
    base_model = ResNet50(weights='imagenet', include_top=True)
    model = Model(input=base_model.input,
                  output=base_model.get_layer('flatten_1').output)
    return (model, base_model)

# return feature vector for a given img, and model
def image_features(img, model):
    features = model.predict(img)
    return features

def extract_feats_from_chips(chipdataset, output_fname):
    model, base_model = get_models()

    features = np.zeros((len(chipdataset), 2048), dtype=np.float16)
    chips = []
    chip_keys = []
    for index, (chip_key, chip) in enumerate(chipdataset.chips.items()):
        chip_keys.append(chip_key)
        chips.append(chip)
        img_path = chip.filepath
        img_data = load_image(img_path)
        features[index] = image_features(img_data, model)
    
    FeatureDataset.save(output_fname, chip_keys, chips, features)
    return True
