import numpy as np


class Params(object):
    def __init__(self,
                 speed,
                 landing_time,
                 takeoff_time,
                 maximum_flight_time,
#                 reload_time,
#                 battery_switching_time,
#                 total_number_of_batteries,
#                 num_mav,
                 num_people,
                 num_packets):
        self.speed = speed
        self.landing_time = landing_time
        self.takeoff_time = takeoff_time
        self.maximum_flight_time = maximum_flight_time
#        self.reload_time = reload_time  # TODO
#        self.battery_switching_time = battery_switching_time  # TODO
#        self.total_number_of_batteries = total_number_of_batteries  # TODO
#        self.num_mav = num_mav
        self.num_people = num_people
        self.num_packets = num_packets


def find_routes(person_coord_list,
                adj_matrix_shape,  # used just for simulation purposes
                home_coord,
                params):
    person_coord_list = person_coord_list[:]
    distances_to_home = np.linalg.norm(
        np.array(home_coord) - np.array(person_coord_list),
        axis=1
    )
    elapsed_time_list = [0]
    # all routes start at the home coordinate
    routes = [[home_coord]]
    route_idx = 0
    next_coord, time_to_next, time_to_home = find_routes_visit(
        curr_coord=home_coord,
        nb_coord_list=person_coord_list,
        distances_to_home=distances_to_home,
        adj_matrix_shape=adj_matrix_shape,
        params=params
    )
    loop_idx = -1
    while len(person_coord_list) != 0:
        loop_idx += 1
        next_coord, time_to_next, time_to_home = find_routes_visit(
            curr_coord=next_coord,
            nb_coord_list=person_coord_list,
            distances_to_home=distances_to_home,
            adj_matrix_shape=adj_matrix_shape,
            params=params
        )
        if (((params.maximum_flight_time*60-time_to_home) > 0)
                and ((params.maximum_flight_time*60-time_to_next) > 0)):
            # Remember the home coord is in routes when measuring its len.
            if params.num_packets < len(routes[route_idx]):
                route_idx += 1
                routes.append([home_coord])
                elapsed_time_list.append(0)
            routes[route_idx].append(next_coord)
            elapsed_time_list[route_idx] += time_to_next
            idx = person_coord_list.index(next_coord)
            del person_coord_list[idx]
            distances_to_home = np.delete(distances_to_home, idx)
    routes_clean = []
    elapsed_time_list_clean = []
    for i in range(len(routes)):
        if len(routes[i]) <= 1:
            continue
        routes_clean.append(routes[i] + [home_coord])
        elapsed_time_list_clean.append(elapsed_time_list[i])
    return routes_clean, elapsed_time_list_clean


def find_routes_visit(curr_coord, nb_coord_list,
                   distances_to_home,
                   adj_matrix_shape, params):
    distances = np.linalg.norm(
        np.array(curr_coord) - np.array(nb_coord_list),
        axis=1
    )
    distances += distances_to_home
    closest_dist, closest_coord = min(zip(distances, nb_coord_list))
    # takeoff once to exit curr_coord
    elapsed_time = params.takeoff_time
    # go to the closest nb_coord (and come back to the home)
    elapsed_time += params.speed / closest_dist
    # land at the coord
    elapsed_time += params.landing_time
    # takeoff again
    elapsed_time += params.takeoff_time
    # time to go to the next coord
    time_to_next = elapsed_time - (
        params.speed / distances_to_home[nb_coord_list.index(closest_coord)]
    )
    # bat_next = params.maximum_flight_time - elapsed_time
    # land again
    elapsed_time += params.landing_time
    # time to go to the next coord, then to go back home
    time_to_home = elapsed_time
    # bat_home = params.maximum_flight_time - elapsed_time
    return closest_coord, time_to_next, time_to_home
