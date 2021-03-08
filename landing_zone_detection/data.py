import numpy as np
import cv2
from landing_zone_detection import label_utils
import os


class AerialImageData(object):
    """Aerial image and its surrounding data.

    Parameters
    ----------
    frame : numpy.ndarray
        Frame (image) taken by the flying UAV.
    adj_matrix : numpy.ndarray
        Adjacent matrix where the meaning of each value is specified in the label_utils.py module.
    height_map : numpy.ndarray
        Depth estimation of the frame. Same shape as the adj_matrix.
    person_coord : list
        (x, y) coordinate of a person in the adj_matrix. This is the person who's supposed to receive the UAV.

    """

    def __init__(self, frame=None, adj_matrix=None, height_map=None,
                 person_coord=None):
        self.frame = frame
        self.adj_matrix = adj_matrix
        self.height_map = height_map
        self.person_coord = person_coord


# UTILITIES TO GENERATE RANDOM DATA
MOCK_DATA_PATH = 'mock_data'
TERRAIN_OPTIONS_IMAGES = [
    os.path.join(MOCK_DATA_PATH, 'grass.png'),
    os.path.join(MOCK_DATA_PATH, 'grass_barrel.png'),
    os.path.join(MOCK_DATA_PATH, 'grass_pincushion.png'),
    os.path.join(MOCK_DATA_PATH, 'tall_grass.png'),
    os.path.join(MOCK_DATA_PATH, 'tall_grass_barrel.png'),
    os.path.join(MOCK_DATA_PATH, 'tall_grass_pincushion.png'),
    os.path.join(MOCK_DATA_PATH, 'tree.png'),
    os.path.join(MOCK_DATA_PATH, 'tree_barrel.png'),
    os.path.join(MOCK_DATA_PATH, 'tree_pincushion.png'),
]
PERSON_OPTIONS_IMAGES = [
    os.path.join(MOCK_DATA_PATH, 'person_in_tall_grass.png'),
    os.path.join(MOCK_DATA_PATH, 'person_in_tall_grass_barrel.png'),
    os.path.join(MOCK_DATA_PATH, 'person_in_tall_grass_pincushion.png'),
    os.path.join(MOCK_DATA_PATH, 'person_on_grass.png'),
    os.path.join(MOCK_DATA_PATH, 'person_on_grass_barrel.png'),
    os.path.join(MOCK_DATA_PATH, 'person_on_grass_pincushion.png'),
]

TERRAIN_OPTIONS_LABELS = [
    label_utils.UAV_CAN_LAND_PERSON_CAN_REACH,  # grass
    label_utils.UAV_CAN_LAND_PERSON_CAN_REACH,  # grass_barrel
    label_utils.UAV_CAN_LAND_PERSON_CAN_REACH,  # grass_pincushion
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # tall_grass
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # tall_grass_barrel
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # tall_grass_pincushion
    label_utils.UAV_CANNOT_LAND_PERSON_CANNOT_REACH,  # tree
    label_utils.UAV_CANNOT_LAND_PERSON_CANNOT_REACH,  # tree_barrel
    label_utils.UAV_CANNOT_LAND_PERSON_CANNOT_REACH,  # tree_pincushion
]
PERSON_OPTIONS_LABELS = [
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # person_in_tall_grass
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # person_in_tall_grass_barrel
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # person_in_tall_grass_pincushion
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # person_on_grass
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # person_on_grass_barrel
    label_utils.UAV_CANNOT_LAND_PERSON_CAN_REACH,  # person_on_grass_pincushion
]

TERRAIN_OPTIONS_HEIGHTS = [
    0,  # grass
    0.8,  # grass_barrel
    -1.2,  # grass_pincushion
    0,  # tall_grass
    0.8,  # tall_grass_barrel
    -1.2,  # tall_grass_pincushion
    0,  # tree
    0.8,  # tree_barrel
    -1.2,  # tree_pincushion
]
PERSON_OPTIONS_HEIGHTS = [
    0,  # person_in_tall_grass
    0.8,  # person_in_tall_grass_barrel
    -1.2,  # person_in_tall_grass_pincushion
    0,  # person_on_grass
    0.8,  # person_on_grass_barrel
    -1.2,  # person_on_grass_pincushion
]


class RandomAerialImageDataGenerator(object):
    """Class to generate random AerialImageData object using the given terrain and person options.

    Parameters
    ----------
    width : int
        Image width.
    height : int
        Image  height.
    channels : int
        Number of channels in the image.
    dtype : np.uint8
        Data type of the frame.
    col_size : int
        Width of each adj_matrix (or height_map) item.
    row_size : int
        Height of each adj_matrix (or height_map) item.
    terrain_options_images : list
        Each item of the image can randomly assume one of this images.
    terrain_options_labels : list
        Labels of each option in terrain_options_images.
    terrain_options_heights : list
        Estimated depth (height from the drone to the ground) of each option in terrain_options_images.
    person_options_images : list
        Until now, only one random item of the image can assume one of this images. In other words: only one person per image.
    person_options_labels : list
        Labels of each person_options in person_options_images.
    person_options_heights : list
        Estimated depth (height from the drone to the ground) of each option in person_options_images.

    Attributes
    ----------
    num_cols : type
        Number of columns in each adj_matrix (or height_map) item.
    num_rows : type
        Number of rows in each adj_matrix (or height_map) item.

    """

    def __init__(self, width=224, height=224, channels=3, dtype=np.uint8,
                 col_size=32, row_size=32,
                 terrain_options_images=TERRAIN_OPTIONS_IMAGES,
                 terrain_options_labels=TERRAIN_OPTIONS_LABELS,
                 terrain_options_heights=TERRAIN_OPTIONS_HEIGHTS,
                 person_options_images=PERSON_OPTIONS_IMAGES,
                 person_options_labels=PERSON_OPTIONS_LABELS,
                 person_options_heights=PERSON_OPTIONS_HEIGHTS):
        self.width = width
        self.height = height
        self.channels = channels
        self.dtype = dtype
        self.col_size = col_size
        self.row_size = row_size
        self.terrain_options_images = terrain_options_images
        self.terrain_options_labels = terrain_options_labels
        self.terrain_options_heights = terrain_options_heights
        self.person_options_images = person_options_images
        self.person_options_labels = person_options_labels
        self.person_options_heights = person_options_heights

        self.num_cols = self.width // self.col_size
        self.num_rows = self.height // self.row_size

        self.terrain_options_images = self.load_img_items(
            self.terrain_options_images
        )
        self.person_options_images = self.load_img_items(
            self.person_options_images
        )

    def __read_img_item(self, filename, **kwargs):
        """Read an image item from filename.

        Parameters
        ----------
        filename : str
            File path.
        **kwargs : dict
            **kwargs.

        Returns
        -------
        numpy.ndarray
            2D matrix representing an image.

        """
        return cv2.imread(
            filename,
            **kwargs
        )

    def __resize_img_item(self, img_item,
                          resize_method=cv2.INTER_LINEAR, **kwargs):
        """Resize an image item.

        Parameters
        ----------
        img_item : numpy.ndarray
            2D matrix representing an image.
        resize_method : int
            Type of the resize method i.e cv2.INTER_LINEAR.
        **kwargs : dict
            **kwargs

        Returns
        -------
        numpy.ndarray
            Resized image.

        """
        return cv2.resize(
            src=img_item,
            dsize=(self.col_size, self.row_size),
            interpolation=resize_method,
            **kwargs
        )

    def load_img_items(self, img_items):
        """Read and transform a list of image items.

        Parameters
        ----------
        img_items : list
            List of paths, or list of numpy.ndarrays.

        Returns
        -------
        list
            List of the transformed images.

        """
        for i, img in enumerate(img_items):
            # read images
            if type(img) == str:
                img = self.__read_img_item(img)
            # transform images
            img = self.__resize_img_item(img)
            img_items[i] = img
        return img_items

    def generate(self):
        """Generates a random AerialImageData object using the given terrain and person options.

        Returns
        -------
        AerialImageData
            Aerial image and its surrounding data.

        """
        data = AerialImageData(
            frame=np.empty(
                (
                    self.num_cols*self.col_size,
                    self.num_rows*self.row_size,
                    self.channels,
                ),
                dtype=self.dtype,
            ),
            adj_matrix=np.empty(
                (self.num_cols, self.num_rows),
                dtype=np.int8,
            ),
            height_map=np.empty(
                (self.num_cols, self.num_rows),
                dtype=np.int8,
            )
        )
        # populate with the terrain options
        for i in range(self.num_cols):
            x1 = self.col_size*i
            x2 = self.col_size*(i+1)
            for j in range(self.num_rows):
                y1 = self.row_size*j
                y2 = self.row_size*(j+1)
                chosen_item_idx = np.random.choice(
                    len(self.terrain_options_images)
                )
                data.height_map[i][j] = self.terrain_options_heights[
                    chosen_item_idx
                ]
                data.adj_matrix[i][j] = \
                    self.terrain_options_labels[chosen_item_idx]
                data.frame[x1:x2, y1:y2, :] = \
                    self.terrain_options_images[chosen_item_idx]
        # choose a single terrain item randomly and subtitute it with a person
        i = np.random.choice(self.num_cols)
        x1 = self.col_size*i
        x2 = self.col_size*(i+1)
        j = np.random.choice(self.num_rows)
        y1 = self.row_size*j
        y2 = self.row_size*(j+1)
        chosen_item_idx = np.random.choice(len(self.person_options_images))
        data.height_map[i][j] = self.person_options_heights[chosen_item_idx]
        data.adj_matrix[i][j] = self.person_options_labels[chosen_item_idx]
        data.frame[x1:x2, y1:y2, :] = self.person_options_images[
            chosen_item_idx
        ]
        # store the coordinate of the person
        data.person_coord = [i, j]
        return data
