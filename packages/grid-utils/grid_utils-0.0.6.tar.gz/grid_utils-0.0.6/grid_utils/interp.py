# -*- coding:utf-8 -*-

import numpy as np


__all__ = ['calc_bilinear_para']


def calc_bilinear_para(float_i, float_j, nx=None, ny=None):
    """
    Calculate bilinear interpolate parameter (i, j, weight) for a given position.
    :param float_i: x position (float number)
    :param float_j: y position (float number)
    :param nx: X grid num (for limitation)
    :param ny: Y grid num (for limitation)
    :return: {"i": i_arr, "j": j_arr, "weight": weight_arr}

    The result can be used like this:
    >>> v_interp = np.sum(v_arr[para["j"], para["i"]] * para["weight"])
    """
    ai = float_i % 1
    aj = float_j % 1

    i1 = int(np.floor(float_i))
    i2 = i1 + 1
    j1 = int(np.floor(float_j))
    j2 = j1 + 1

    has_i1 = i1 >= 0
    has_j1 = j1 >= 0
    has_i2 = nx is None or i2 <= nx-1
    has_j2 = ny is None or j2 <= ny-1

    if has_i1 and has_j1:
        if has_i2 and has_j2:
            # has 4 points: (i1, j1), (i2, j1), (i1, j2), (i2, j2)
            i_list = [i1, i2, i1, i2]
            j_list = [j1, j1, j2, j2]
            weight_list = [(1.0-ai)*(1.0-aj), ai*(1.0-aj), (1.0-ai)*aj, ai*aj]
        elif has_i2 and not has_j2:
            # has 2 points: (i1, j1), (i2, j1)
            i_list = [i1, i2]
            j_list = [j1, j1]
            weight_list = [1.0-ai, ai]
        elif not has_i2 and has_j2:
            # has 2 points: (i1, j1), (i1, j2)
            i_list = [i1, i1]
            j_list = [j1, j2]
            weight_list = [1.0-aj, aj]
        else:
            # only 1 point: (i1, j1)
            i_list = [i1]
            j_list = [j1]
            weight_list = [1.0]
    elif has_i1 and not has_j1:
        if has_i2:
            # has 2 points: (i1, j2), (i2, j2)
            i_list = [i1, i2]
            j_list = [j2, j2]
            weight_list = [1.0-ai, ai]
        else:
            # only 1 point: (i1, j2)
            i_list = [i1]
            j_list = [j2]
            weight_list = [1.0]
    elif not has_i1 and has_j1:
        if has_j2:
            # has 2 points: (i2, j1), (i2, j2)
            i_list = [i2, i2]
            j_list = [j1, j2]
            weight_list = [1.0-aj, aj]
        else:
            # only 1 point: (i2, j1)
            i_list = [i2]
            j_list = [j1]
            weight_list = [1.0]
    else:
        # only 1 point: (i2, j2)
        i_list = [i2]
        j_list = [j2]
        weight_list = [1.0]

    return {"i": np.array(i_list), "j": np.array(j_list), "weight": np.array(weight_list)}
