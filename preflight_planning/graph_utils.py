import numpy as np


class Params(object):
    def __init__(self,
                 speed,
                 landing_time,
                 takeoff_time,
                 maximum_flight_time,
                 reload_time,
                 battery_switching_time,
                 total_number_of_batteries,
                 num_mav,
                 num_people,
                 num_packets):
        self.speed = speed
        self.landing_time = landing_time
        self.takeoff_time = takeoff_time
        self.maximum_flight_time = maximum_flight_time
        self.reload_time = reload_time  # TODO
        self.battery_switching_time = battery_switching_time  # TODO
        self.total_number_of_batteries = total_number_of_batteries  # TODO
        self.num_mav = num_mav
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
    # while drone aguentar (num_packets, maximum_flight_time)
    # qnd o drone num aguentar mais, vai pro outro q eh pra n decolar a toa
    uav_elapsed_times = np.zeros(params.num_mav)
    # all MAVs start at the home coordinate
    uav_routes = np.repeat([[home_coord]], params.num_mav, axis=0).tolist()
    uav_idx = 0
    next_coord, time_to_next, time_to_home = find_routes_re(
        curr_coord=home_coord,
        nb_coord_list=person_coord_list,
        distances_to_home=distances_to_home,
        adj_matrix_shape=adj_matrix_shape,
        params=params
    )
    loop_idx = -1
    while True:
        loop_idx += 1
        if len(person_coord_list) == 0:
            break
        next_coord, time_to_next, time_to_home = find_routes_re(
            curr_coord=next_coord,
            nb_coord_list=person_coord_list,
            distances_to_home=distances_to_home,
            adj_matrix_shape=adj_matrix_shape,
            params=params
        )
        if (((params.maximum_flight_time*60-time_to_home) > 0)
                and ((params.maximum_flight_time*60-time_to_next) > 0)):
            # Remember the home coord is in uav_routes when measuring its len.
            if params.num_packets < len(uav_routes[uav_idx]):
                uav_idx += 1
                if uav_idx > params.num_mav:
                    break
            uav_routes[uav_idx].append(next_coord)
            uav_elapsed_times[uav_idx] += time_to_next
            idx = person_coord_list.index(next_coord)
            del person_coord_list[idx]
            distances_to_home = np.delete(distances_to_home, idx)
            continue
        else:
            uav_idx += 1
            if uav_idx > params.num_mav:
                break
            continue
    uav_routes, uav_elapsed_times = list(zip(*[
        (route, time) for (route, time)
        in zip(uav_routes, uav_elapsed_times)
        if len(route) > 1
    ]))
    return uav_routes, uav_elapsed_times


def find_routes_re(curr_coord, nb_coord_list,
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
    # battery remaining to go to the next coord, then to go back home
    time_to_home = elapsed_time
    # bat_home = params.maximum_flight_time - elapsed_time
    # If the MAV has enough battery to come back, try to reach another node.
    # Else, use the previously calculated path.
    return closest_coord, time_to_next, time_to_home
