import numpy as np

from landing_zone_detection import labels


def do_coord_exist(coord, matrix_shape):
    """Short summary.

    Parameters
    ----------
    coord : type
        Description of parameter `coord`.
    matrix_shape : type
        Description of parameter `matrix_shape`.

    Returns
    -------
    type
        Description of returned object.

    """
    return np.bitwise_and(coord < matrix_shape, coord >= 0).all()


def can_a_person_reach(coord, adj_matrix):
    """Short summary.

    Parameters
    ----------
    coord : list or ndarray
        2D coordinate i.e (0, 0).
    adj_matrix : type
        Description of parameter `adj_matrix`.

    Returns
    -------
    type
        Description of returned object.

    """
    value = adj_matrix[coord[0]][coord[1]]
    return value == labels.UAV_CAN_LAND_PERSON_CAN_REACH or \
        value == labels.UAV_CANNOT_LAND_PERSON_CAN_REACH


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


def hash_coord(coord):
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


def search(data):
    shortest_paths_dict = {}
    person_coord_hash = hash_coord(data.person_coord)
    shortest_paths_dict[person_coord_hash] = {}
    shortest_paths_dict[person_coord_hash]['path'] = [data.person_coord]
    shortest_paths_dict[person_coord_hash]['distance'] = 0

    search_visit(data.person_coord, data, shortest_paths_dict)

    del shortest_paths_dict[person_coord_hash]

    for value in shortest_paths_dict.values():
        if 'shortest_distance' not in locals():
            shortest_path = value['path']
            shortest_distance = value['distance']
            continue
        if shortest_distance > value['distance']:
            shortest_path = value['path']
            shortest_distance = value['distance']

    return shortest_path, shortest_distance


base_neighbours = np.asarray([[1, 0], [0, 1], [1, 1],
                              [-1, 0], [0, -1], [-1, -1],
                              [-1, 1], [1, -1]])


def search_visit(current_coord, data, shortest_paths_dict):
    current_coord_hash = hash_coord(current_coord)
    current_height = data.height_map[current_coord[0]][current_coord[1]]
    neighbour_list = base_neighbours + np.asarray(current_coord)
    # remove unreachable coords or coords that don't exist
    neighbour_list = [
        neighbour for neighbour in neighbour_list
        if (do_coord_exist(neighbour, data.adj_matrix.shape)
            and can_a_person_reach(neighbour, data.adj_matrix))
    ]
    for neighbour_coord in neighbour_list:
        neighbour_coord_hash = hash_coord(neighbour_coord)
        neighbour_height = data\
            .height_map[neighbour_coord[0]][neighbour_coord[1]]
        distance = shortest_paths_dict[current_coord_hash]['distance'] + \
            distance_between_3d_points(
                *current_coord, abs(current_height),
                *neighbour_coord, abs(neighbour_height)
            )

        if neighbour_coord_hash not in shortest_paths_dict:
            shortest_paths_dict[neighbour_coord_hash] = {}
        else:
            if distance > shortest_paths_dict[neighbour_coord_hash]['distance']:
                continue

        path = [
            *shortest_paths_dict[current_coord_hash]['path'],
            neighbour_coord
        ]

        shortest_paths_dict[neighbour_coord_hash]['path'] = path
        shortest_paths_dict[neighbour_coord_hash]['distance'] = distance

        search_visit(neighbour_coord, data, shortest_paths_dict)
