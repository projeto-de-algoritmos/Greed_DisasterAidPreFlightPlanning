UAV_CAN_LAND_PERSON_CAN_REACH = 1
UAV_CANNOT_LAND_PERSON_CAN_REACH = 0
UAV_CANNOT_LAND_PERSON_CANNOT_REACH = -1


def can_uav_land(label):
    """Checks if an UAV can reach a position labelled with "label".

    Parameters
    ----------
    label : int
        Label of a position in the image.

    Returns
    -------
    boolean
        Whether an UAV can reach a position labelled with "label".

    """
    return label == UAV_CAN_LAND_PERSON_CAN_REACH


def can_a_person_reach(label):
    """Checks if a person can reach a position labelled with "label".

    Parameters
    ----------
    label : int
        Label of a position in the image.

    Returns
    -------
    bool
        Whether a person can reach a position labelled with "label".

    """
    return label == UAV_CAN_LAND_PERSON_CAN_REACH or \
        label == UAV_CANNOT_LAND_PERSON_CAN_REACH
