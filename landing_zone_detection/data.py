import numpy as np
import cv2
from landing_zone_detection import labels
import os


class AerialImageData(object):
    """Short summary.

    Parameters
    ----------
    frame : type
        Description of parameter `frame`.
    adj_matrix : type
        Description of parameter `adj_matrix`.
    height_map : type
        Description of parameter `height_map`.

    Attributes
    ----------
    frame
    adj_matrix
    height_map

    """

    def __init__(self, frame=None, adj_matrix=None, height_map=None):
        self.frame = frame
        self.adj_matrix = adj_matrix
        self.height_map = height_map


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
    labels.UAV_CAN_LAND_HUMAN_CAN_REACH,  # grass
    labels.UAV_CAN_LAND_HUMAN_CAN_REACH,  # grass_barrel
    labels.UAV_CAN_LAND_HUMAN_CAN_REACH,  # grass_pincushion
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # tall_grass
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # tall_grass_barrel
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # tall_grass_pincushion
    labels.UAV_CANNOT_LAND_HUMAN_CANNOT_REACH,  # tree
    labels.UAV_CANNOT_LAND_HUMAN_CANNOT_REACH,  # tree_barrel
    labels.UAV_CANNOT_LAND_HUMAN_CANNOT_REACH,  # tree_pincushion
]
PERSON_OPTIONS_LABELS = [
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # person_in_tall_grass
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # person_in_tall_grass_barrel
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # person_in_tall_grass_pincushion
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # person_on_grass
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # person_on_grass_barrel
    labels.UAV_CANNOT_LAND_HUMAN_CAN_REACH,  # person_on_grass_pincushion
]

TERRAIN_OPTIONS_HEIGHTS = [
    0,  # grass
    1,  # grass_barrel
    -1,  # grass_pincushion
    0,  # tall_grass
    1,  # tall_grass_barrel
    -1,  # tall_grass_pincushion
    0,  # tree
    1,  # tree_barrel
    -1,  # tree_pincushion
]
PERSON_OPTIONS_HEIGHTS = [
    0,  # person_in_tall_grass
    1,  # person_in_tall_grass_barrel
    -1,  # person_in_tall_grass_pincushion
    0,  # person_on_grass
    1,  # person_on_grass_barrel
    -1,  # person_on_grass_pincushion
]


class RandomAerialImageDataGenerator(object):
    """Short summary.

    Parameters
    ----------
    width : type
        Description of parameter `width`.
    height : type
        Description of parameter `height`.
    channels : type
        Description of parameter `channels`.
    dtype : type
        Description of parameter `dtype`.
    col_size : type
        Description of parameter `col_size`.
    row_size : type
        Description of parameter `row_size`.
    terrain_options_images : type
        Description of parameter `terrain_options_images`.
    terrain_options_labels : type
        Description of parameter `terrain_options_labels`.
    terrain_options_heights : type
        Description of parameter `terrain_options_heights`.
    person_options_images : type
        Description of parameter `person_options_images`.
    person_options_labels : type
        Description of parameter `person_options_labels`.
    person_options_heights : type
        Description of parameter `person_options_heights`.

    Attributes
    ----------
    num_cols : type
        Description of attribute `num_cols`.
    num_rows : type
        Description of attribute `num_rows`.
    load_img_items : type
        Description of attribute `load_img_items`.
    width
    height
    channels
    dtype
    col_size
    row_size
    terrain_options_images
    terrain_options_labels
    terrain_options_heights
    person_options_images
    person_options_labels
    person_options_heights

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
        """Short summary.

        Parameters
        ----------
        filename : type
            Description of parameter `filename`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        return cv2.imread(
            filename,
            **kwargs
        )

    def __resize_img_item(self, img_item,
                          resize_method=cv2.INTER_LINEAR, **kwargs):
        """Short summary.

        Parameters
        ----------
        img_item : type
            Description of parameter `img_item`.
        resize_method : type
            Description of parameter `resize_method`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        return cv2.resize(
            img_item,
            (self.col_size, self.row_size),
            resize_method,
            **kwargs
        )

    def load_img_items(self, img_items):
        """Short summary.

        Parameters
        ----------
        img_items : type
            Description of parameter `img_items`.

        Returns
        -------
        type
            Description of returned object.

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
        """Short summary.

        Returns
        -------
        type
            Description of returned object.

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
        return data
