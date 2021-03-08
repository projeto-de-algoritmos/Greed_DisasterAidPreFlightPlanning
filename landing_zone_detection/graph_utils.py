import numpy as np
from landing_zone_detection.label_utils import can_a_person_reach, can_uav_land


def do_coord_exist(coord, matrix_shape):
    """Check if a 2D coordinate isn't out of bounds.

    Parameters
    ----------
    coord : ndarray
        Description of parameter `coord`.
    matrix_shape : ndarray
        Description of parameter `matrix_shape`.

    Returns
    -------
    bool
        Whether the coordinate exists.

    """
    return np.bitwise_and(coord < matrix_shape, coord >= 0).all()


def distance_between_3d_points(x1, y1, z1, x2, y2, z2):
    """Short summary.

    Parameters
    ----------
    x1 : type
        Description of parameter `x1`.
    y1 : type
        Description of parameter `y1`.
    z1 : type
        Description of parameter `z1`.
    x2 : type
        Description of parameter `x2`.
    y2 : type
        Description of parameter `y2`.
    z2 : type
        Description of parameter `z2`.

    Returns
    -------
    type
        Description of returned object.

    """
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)**(1/2)


def hashable_coord(coord):
    """Short summary.

    Parameters
    ----------
    coord : type
        Description of parameter `coord`.

    Returns
    -------
    type
        Description of returned object.

    """
    return str(coord)


def find_landing_zone(data):
    """Short summary.

    Parameters
    ----------
    data : type
        Description of parameter `data`.

    Returns
    -------
    type
        Description of returned object.

    """
    shortest_paths_dict = {}
    person_coord_hash = hashable_coord(data.person_coord)
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
    """Short summary.

    Parameters
    ----------
    current_coord : type
        Description of parameter `current_coord`.
    data : type
        Description of parameter `data`.
    shortest_paths_dict : type
        Description of parameter `shortest_paths_dict`.
    base_neighbours : type
        Description of parameter `base_neighbours`.

    Returns
    -------
    type
        Description of returned object.

    """
    current_coord_hash = hashable_coord(current_coord)
    current_height = data.height_map[current_coord[0]][current_coord[1]]
    current_item = shortest_paths_dict[current_coord_hash]
    neighbour_list = base_neighbours + np.asarray(current_coord)
    for nb_coord in neighbour_list:
        # ignore coords that do not exist i.e (-1, 99999999)
        if not do_coord_exist(nb_coord, data.adj_matrix.shape):
            continue
        nb_label = data.adj_matrix[nb_coord[0]][nb_coord[1]]
        # ignore unreachable coords
        if not can_a_person_reach(nb_label):
            continue

        nb_coord_hashable = hashable_coord(nb_coord)
        nb_height = data.height_map[nb_coord[0]][nb_coord[1]]
        nb_distance = current_item['distance'] + \
            distance_between_3d_points(
                current_coord[0], current_coord[1], abs(current_height),
                nb_coord[0], nb_coord[1], abs(nb_height)
            )

        if nb_coord_hashable not in shortest_paths_dict:
            shortest_paths_dict[nb_coord_hashable] = {}
        else:
            if nb_distance > shortest_paths_dict[nb_coord_hashable]['distance']:
                continue
        nb_coord_item = shortest_paths_dict[nb_coord_hashable]

        nb_coord_item['distance'] = nb_distance
        nb_coord_item['path'] = shortest_paths_dict[current_coord_hash]['path'][:]
        nb_coord_item['path'].append(nb_coord)
        if can_uav_land(nb_label):
            nb_coord_item['can_uav_land'] = True
        else:
            nb_coord_item['can_uav_land'] = False

        find_landing_zone_re(
            nb_coord, data, shortest_paths_dict, base_neighbours
        )
