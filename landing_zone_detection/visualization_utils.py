import cv2
import numpy as np
import matplotlib.pyplot as plt


def item_from_color(color, col_size=32, row_size=32):
    """Short summary.

    Parameters
    ----------
    color : type
        Description of parameter `color`.
    col_size : type
        Description of parameter `col_size`.
    row_size : type
        Description of parameter `row_size`.

    Returns
    -------
    type
        Description of returned object.

    """
    return np.repeat(
        [np.repeat([color], col_size, axis=0)],
        row_size,
        axis=0
    )


def adj_matrix_to_image(adj_matrix,
                        value_to_color={1: [80, 30, 50],
                                        0: [168, 50, 125],
                                        -1: [0, 0, 255]},
                        num_channels=3,
                        num_cols=7, num_rows=7,
                        col_size=32, row_size=32,
                        img_dtype=np.uint8):
    """Short summary.

    Parameters
    ----------
    adj_matrix : type
        Description of parameter `adj_matrix`.
    value_to_color : type
        Description of parameter `value_to_color`.
    num_cols : type
        Description of parameter `num_cols`.
    num_rows : type
        Description of parameter `num_rows`.
    col_size : type
        Description of parameter `col_size`.
    row_size : type
        Description of parameter `row_size`.
    img_dtype : type
        Description of parameter `img_dtype`.

    Returns
    -------
    type
        Description of returned object.

    """
    img = np.zeros(
        (num_cols*col_size, num_rows*row_size, num_channels),
        dtype=img_dtype
    )
    value_to_item = {
        1: item_from_color(value_to_color[1]),
        0: item_from_color(value_to_color[0]),
        -1: item_from_color(value_to_color[-1]),
    }
    for i, col in enumerate(adj_matrix):
        x1 = col_size*i
        x2 = col_size*(i+1)
        for j, value in enumerate(col):
            y1 = row_size*j
            y2 = row_size*(j+1)
            img[x1:x2, y1:y2, :] = value_to_item[value].copy()
    return img


def node_list_to_image(node_list,
                       item_color=[255, 0, 0],
                       num_channels=3,
                       num_cols=7, num_rows=7,
                       col_size=32, row_size=32,
                       img_dtype=np.uint8):
    """Short summary.

    Parameters
    ----------
    node_list : type
        Description of parameter `node_list`.
    item_color : type
        Description of parameter `item_color`.
    num_cols : type
        Description of parameter `num_cols`.
    num_rows : type
        Description of parameter `num_rows`.
    col_size : type
        Description of parameter `col_size`.
    row_size : type
        Description of parameter `row_size`.
    img_dtype : type
        Description of parameter `img_dtype`.

    Returns
    -------
    type
        Description of returned object.

    """
    img = np.zeros(
        (num_cols*col_size, num_rows*row_size, num_channels),
        dtype=img_dtype
    )
    item = item_from_color(item_color)
    for node in node_list:
        x1 = col_size*node[0]
        x2 = col_size*(node[0]+1)
        y1 = row_size*node[1]
        y2 = row_size*(node[1]+1)
        img[x1:x2, y1:y2, :] = item.copy()
    return img


def plot_frame(frame, width=224, height=224, images_to_overlay=[]):
    """Short summary.

    Parameters
    ----------
    frame : type
        Description of parameter `frame`.
    width : type
        Description of parameter `width`.
    height : type
        Description of parameter `height`.
    images_to_overlay : type
        Description of parameter `images_to_overlay`.

    Returns
    -------
    type
        Description of returned object.

    """
    # overlay images on the frame
    if images_to_overlay:
        img_to_overlay = images_to_overlay[0]
    for img in images_to_overlay[1:]:
        img_to_overlay += img
    if images_to_overlay:
        frame = cv2.addWeighted(img_to_overlay, 1.0, frame, 1.0, 0.0)
    # resize to desired size with bilinear interpolation
    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)
    # convert from BGR to RGB for plotting purposes
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # plot the resulting frame
    plt.imshow(frame)
    plt.show()
