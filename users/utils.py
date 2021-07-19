import numpy as np
import cv2 as cv




def get_shoulder_width(image_path, shoulder_pixels:int, actual_dimensions=1.98, points=8) -> float:
    """Returns the shoulder width in centimeters in real life"""
    def most_common(lst) -> int:
        """Returns most common occurrence"""
        return max(set(lst), key=lst.count)
    image = cv.imread(image_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, points, 0.01, 8)
    corners = np.int0(corners)
    list_x = []
    list_y = []
    for i in corners:
        x, y = i.ravel()

        list_x.append(x)
        list_y.append(y)

        list_x.sort()
        list_y.sort()

    diff_x = [t - s for s, t in zip(list_x, list_x[1:])]

    diff_y = [t - s for s, t in zip(list_y, list_y[1:])]

    diff_x_limited = [i for i in diff_x if 8 < i < 25]
    diff_y_limited = [i for i in diff_y if 8 < i < 25]
    final_set = set(diff_x_limited + diff_y_limited)

    pixel_candidates_2 = diff_x_limited + diff_y_limited
    pixel_candidates = list(final_set)
    pixel_candidates.sort()

    pixels = pixel_candidates[-1]
    pixels_2 = sum(pixel_candidates_2) / len(pixel_candidates_2)

    pixel_avg = sum(pixel_candidates) / len(pixel_candidates)

    pixels_new = most_common(pixel_candidates_2)

    shoulder_width = (shoulder_pixels * actual_dimensions) / pixels

    shoulder_width_avg = (shoulder_pixels * actual_dimensions) / pixel_avg

    shoulder_width_2 = (shoulder_pixels * actual_dimensions) / pixels_2
    diff_x_indices = [diff_x.index(i) for i in diff_x if 0 < i < 4]
    diff_y_indices = [diff_y.index(i) for i in diff_y if 0 < i < 4]
    final_y_candidates = [diff_y[i] for i in diff_x_indices]
    final_x_candidates = [diff_x[i] for i in diff_y_indices]

    final_final = [i for i in final_y_candidates + final_x_candidates if 8 < i < 25]
    final_final.sort()
    try:
        omega_pixels = most_common(final_final)
    except:
        omega_pixels = pixel_avg
    omega_shoulder_width = (shoulder_pixels * actual_dimensions) / omega_pixels
    shoulder_width_new = (shoulder_pixels * actual_dimensions) / pixels_new

    final_size =  (omega_shoulder_width + (2 * shoulder_width_new) + shoulder_width + shoulder_width_2 + shoulder_width_avg) / 6

    # ik this looks bad , I could use switch but don't want to add another bug in production
  
    if 40<final_size<=44:
        return "small"
    elif 44<final_size <=48:
        return "medium"
    elif 48<final_size<52:
        return "large"
    elif 52<final_size<=54:
        return "xlarge"
    elif 54<final_size<=58:
        return "xxlarge"
    else:
        return final_size
    