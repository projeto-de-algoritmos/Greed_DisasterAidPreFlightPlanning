import numpy as np
from landing_zone_detection.label_utils import can_a_person_reach, can_uav_land


def do_coord_exist(coord, matrix_shape):
    """Check if a 2D coordinate isn't out of bounds.

    Parameters
    ----------
    coord : numpy.ndarray
        2D coordinate i.e (0,0).
    matrix_shape : numpy.ndarray
        Shape of the matrix to where the coordinate should point.

    Returns
    -------
    bool
        Whether the coordinate exists.

    """
    return np.bitwise_and(coord < matrix_shape, coord >= 0).all()


def distance_between_3d_points(x1, y1, z1, x2, y2, z2):
    """Computes the euclidean distance between two 3D points.

    Parameters
    ----------
    x1 : int or float
        x coordinate of point 1.
    y1 : int or float
        y coordinate of point 1`.
    z1 : int or float
        z coordinate of point 1`.
    x2 : int or float
        x coordinate of point 2`.
    y2 : int or float
        y coordinate of point 2`.
    z2 : int or float
        z coordinate of point 2`.

    Returns
    -------
    int or float
        Euclidean distance between two 3D points..

    """
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**(1/2)


def hashable_coord(coord, img_shape):
    """Transforms a coord list into a hashable type.

    Parameters
    ----------
    coord : list or ndarray
        2D coordinate i.e (0,0).
    img_shape : list or ndarray
        Shape of the image i.e [1920, 1080, 3] or [1920, 1080].

    Returns
    -------
    int
        A representation of the coord that is hashable.

    """
    return coord[0] * img_shape[0] + coord[1]


def find_landing_zone(data):
    """Find the landing zone closest to the person xy coordinates considering the z terrain elevation..

    Parameters
    ----------
    data : AerialImageData
        Aerial image and its surrounding data (frame, adj_matrix, height_map and person_coord).

    Returns
    -------
    (list, int)
        Returns the shortest_path and the shortest_distance as a tuple.

    """
    shortest_paths_dict = {}
    person_coord_hash = hashable_coord(
        data.person_coord, data.adj_matrix.shape
    )
    shortest_paths_dict[person_coord_hash] = {}
    shortest_paths_dict[person_coord_hash]['path'] = [data.person_coord]
    shortest_paths_dict[person_coord_hash]['distance'] = 0

    base_neighbours = np.asarray([[1, 0], [0, 1], [1, 1],
                                  [-1, 0], [0, -1], [-1, -1],
                                  [-1, 1], [1, -1]])
    find_landing_zone_re(
        data.person_coord,
        data,
        shortest_paths_dict,
        base_neighbours
    )

    del shortest_paths_dict[person_coord_hash]

    for value in shortest_paths_dict.values():
        if not value['can_uav_land']:
            continue
        if 'shortest_distance' not in locals():
            shortest_path = value['path']
            shortest_distance = value['distance']
            continue
        if shortest_distance > value['distance']:
            shortest_path = value['path']
            shortest_distance = value['distance']

    if 'shortest_distance' in locals():
        return shortest_path, shortest_distance
    else:
        return [], -1


def find_landing_zone_re(current_coord, data, shortest_paths_dict,
                         base_neighbours):
    """Recursive part of find_landing_zone. It doesn't return anything, it just updates the shortest_paths_dict.

    Parameters
    ----------
    current_coord : list
        2D coordinate i.e (0,0).
    data : AerialImageData
        Aerial image and its surrounding data (frame, adj_matrix, height_map and person_coord).
    shortest_paths_dict : dict
        Dict of the path to each node.
    base_neighbours : list of lists
        Neighbours of [0,0]: [1,0], [0,1], [1,1], [-1,0], [0,-1], [-1,-1], [-1,1], [1,-1]. Some of them may not exist in a 2D image.

    """
    current_coord_hash = hashable_coord(current_coord, data.adj_matrix.shape)
    current_height = data.height_map[current_coord[0]][current_coord[1]]
    current_item = shortest_paths_dict[current_coord_hash]
    neighbour_list = base_neighbours + np.asarray(current_coord)
    for nb_coord in neighbour_list:
        # Ignore coords that do not exist i.e (-1, 99999999).
        if not do_coord_exist(nb_coord, data.adj_matrix.shape):
            continue
        nb_label = data.adj_matrix[nb_coord[0]][nb_coord[1]]
        # Ignore unreachable coords.
        if not can_a_person_reach(nb_label):
            continue

        nb_coord_hashable = hashable_coord(nb_coord, data.adj_matrix.shape)
        # Calculate the distance from the person to the node.
        nb_height = data.height_map[nb_coord[0]][nb_coord[1]]
        nb_distance = current_item['distance'] + \
            distance_between_3d_points(
                current_coord[0], current_coord[1], abs(current_height),
                nb_coord[0], nb_coord[1], abs(nb_height)
            )
        # If neighbour's already in shortest_paths_dict, access it. Otherwise,
        # create and put it into the shortest_paths_dict.
        if nb_coord_hashable not in shortest_paths_dict:
            shortest_paths_dict[nb_coord_hashable] = {}
        else:
            # Check if the calculated distance is shorter than the prev distance.
            # If so, update the values inside nb_coord_item.
            if nb_distance > shortest_paths_dict[nb_coord_hashable]['distance']:
                continue
        nb_coord_item = shortest_paths_dict[nb_coord_hashable]
        nb_coord_item['distance'] = nb_distance
        nb_coord_item['path'] = shortest_paths_dict[current_coord_hash]['path']\
            + [nb_coord]
        if can_uav_land(nb_label):
            nb_coord_item['can_uav_land'] = True
        else:
            nb_coord_item['can_uav_land'] = False

        find_landing_zone_re(
            nb_coord, data, shortest_paths_dict, base_neighbours
        )
