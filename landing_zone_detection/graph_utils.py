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


def hashable_coord(coord, mtx_shape):
    """Transforms a coord list into a hashable type.

    Parameters
    ----------
    coord : list or ndarray
        2D coordinate i.e (0,0).
    mtx_shape : list or ndarray
        Shape of the image i.e [1920, 1080, 3] or [1920, 1080].

    Returns
    -------
    int
        A representation of the coord that is hashable.

    """
    return coord[0] * mtx_shape[0] + coord[1]


class Node(object):
    """Short summary.

    Parameters
    ----------
    coord : list or ndarray
        2D coordinate i.e (0,0).
    mtx_shape : list or ndarray
        Shape of the adj_matrix i.e [7, 7].
    label : type
        Description of parameter `label`.
    height : type
        Description of parameter `height`.
    distance : type
        Description of parameter `distance`.
    path : type
        Description of parameter `path`.

    Attributes
    ----------
    hash : type
        Description of attribute `hash`.
    __hash__ : type
        Description of attribute `__hash__`.
    """

    def __init__(self, coord, mtx_shape,
                 label=None, height=None, distance=-1, path=[]):
        self.coord = coord
        self.mtx_shape = mtx_shape
        self.label = label
        self.height = height
        self.distance = distance
        self.path = path
        self.hash = self.__hash__(coord=self.coord, mtx_shape=self.mtx_shape)

    def __hash__(self, coord, mtx_shape):
        """Hash the node.

        Returns
        -------
        int
            A representation of the coord that is hashable.

        """
        return hashable_coord(coord=coord, mtx_shape=mtx_shape)


def find_landing_zone(person_coord, adj_matrix, height_map):
    """Find the landing zone closest to the person xy coordinates considering the z terrain elevation..

    Parameters
    ----------
    person_coord : list
        (x, y) coordinate in the adj_matrix of the person supposed to receive supplies or deliveries.
    adj_matrix : numpy.ndarray
        Adjacent matrix where the meaning of each value is specified in the label_utils.py module.
    height_map : numpy.ndarray
        Depth estimation of the frame. Same shape as the adj_matrix.

    Returns
    -------
    (list, int)
        Returns the shortest_path and the shortest_distance as a tuple.
    """
    # TODO: [performance] move code to C/C++ or to a recursive language
    base_neighbours = np.asarray([[1, 0], [0, 1], [1, 1],
                                  [-1, 0], [0, -1], [-1, -1],
                                  [-1, 1], [1, -1]])
    shortest_paths_dict = {}

    person_node = Node(
        coord=person_coord,
        mtx_shape=adj_matrix.shape,
        path=[person_coord],
        distance=0,
        height=height_map[person_coord[0]][person_coord[1]],
        label=adj_matrix[person_coord[0]][person_coord[1]],
    )
    shortest_paths_dict[person_node.hash] = person_node
    find_landing_zone_re(
        curr_node=person_node,
        adj_matrix=adj_matrix,
        height_map=height_map,
        shortest_paths_dict=shortest_paths_dict,
        base_neighbours=base_neighbours
    )

    del shortest_paths_dict[person_node.hash]

    shortest_path = []
    shortest_distance = -1

    for node in shortest_paths_dict.values():
        if not can_uav_land(node.label):
            continue
        if (shortest_distance > node.distance) or (shortest_distance == -1):
            shortest_path = node.path
            shortest_distance = node.distance

    return shortest_path, shortest_distance


def find_landing_zone_re(curr_node,
                         adj_matrix, height_map,
                         shortest_paths_dict,
                         base_neighbours):
    """Recursive part of find_landing_zone. It doesn't return anything, it just updates the shortest_paths_dict.

    Parameters
    ----------
    curr_node : Node
        Current node.


    shortest_paths_dict : dict
        Dict of the path to each node.
    base_neighbours : list of lists
        Neighbours of [0,0]: [1,0], [0,1], [1,1], [-1,0], [0,-1], [-1,-1], [-1,1], [1,-1]. Some of them may not exist in a 2D image.

    """
    neighbour_list = base_neighbours + np.asarray(curr_node.coord)
    for nb_node_coord in neighbour_list:
        # Ignore coords that do not exist i.e (-1, 99999999).
        if not do_coord_exist(nb_node_coord, curr_node.mtx_shape):
            continue
        # Ignore unreachable coords.
        nb_node_label = adj_matrix[nb_node_coord[0]][nb_node_coord[1]]
        if not can_a_person_reach(nb_node_label):
            continue
        # If neighbour's already in shortest_paths_dict, access it. Otherwise,
        # create but DON'T put it into the shortest_paths_dict.
        nb_node_hash = Node.__hash__(
            self=None,
            coord=nb_node_coord,
            mtx_shape=curr_node.mtx_shape
        )
        node_was_here_before = nb_node_hash in shortest_paths_dict
        if node_was_here_before:
            nb_node = shortest_paths_dict[nb_node_hash]
        else:
            nb_node = Node(
                coord=nb_node_coord,
                mtx_shape=curr_node.mtx_shape,
                height=height_map[nb_node_coord[0]][nb_node_coord[1]],
                label=nb_node_label,
            )
        # Calculate the distance from the person to the node.
        nb_node_distance = curr_node.distance + \
            distance_between_3d_points(
                curr_node.coord[0], curr_node.coord[1], abs(curr_node.height),
                nb_node.coord[0], nb_node.coord[1], abs(nb_node.height)
            )
        # Check if the calculated distance is shorter than the prev distance.
        # If so, update the values inside nb_node.
        if node_was_here_before:
            if (nb_node_distance > nb_node.distance)\
                    and (not nb_node.distance == -1):
                continue
        else:
            shortest_paths_dict[nb_node_hash] = nb_node
        nb_node.distance = nb_node_distance
        nb_node.path = curr_node.path + [nb_node.coord]
        shortest_paths_dict[nb_node.hash] = nb_node
        find_landing_zone_re(
            curr_node=nb_node,
            adj_matrix=adj_matrix,
            height_map=height_map,
            shortest_paths_dict=shortest_paths_dict,
            base_neighbours=base_neighbours
        )
        shortest_paths_dict[nb_node.hash] = nb_node
