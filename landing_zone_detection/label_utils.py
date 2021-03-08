UAV_CAN_LAND_PERSON_CAN_REACH = 1
UAV_CANNOT_LAND_PERSON_CAN_REACH = 0
UAV_CANNOT_LAND_PERSON_CANNOT_REACH = -1


def can_uav_land(label):
    """Short summary.

    Parameters
    ----------
    label : type
        Description of parameter `label`.

    Returns
    -------
    type
        Description of returned object.

    """
    return label == UAV_CAN_LAND_PERSON_CAN_REACH


def can_a_person_reach(label):
    """Short summary.

    Parameters
    ----------
    label : type
        Description of parameter `label`.

    Returns
    -------
    type
        Description of returned object.

    """
    return label == UAV_CAN_LAND_PERSON_CAN_REACH or \
        label == UAV_CANNOT_LAND_PERSON_CAN_REACH
