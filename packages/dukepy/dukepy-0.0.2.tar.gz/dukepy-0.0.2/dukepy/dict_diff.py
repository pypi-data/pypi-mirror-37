def dict_diff(d1, d2,
              udpate_modified_keys=False,
              udpate_added_keys=False,
              udpate_removed_keys=False,
              path=""):
    """

    :param d1:
    :param d2:
    :param udpate_modified_keys:
    :param udpate_added_keys:
    :param udpate_removed_keys:
    :param path:
    :return: True if at least one difference.
    """
    ret = False
    for k in list(d1.keys()):
        if not k in d2:
            ret = True
            print(path, ":")
            # print(k + " as key not in d2", "\n")
            print(" - ", k, " : ", d1[k])
            if udpate_removed_keys:
                d1.pop(k)
        else:
            if type(d1[k]) is dict:
                if path == "":
                    local_path = k
                else:
                    local_path = path + "->" + k

                dict_diff(d1[k], d2[k],
                          udpate_modified_keys=udpate_modified_keys,
                          udpate_added_keys=udpate_added_keys,
                          udpate_removed_keys=udpate_removed_keys,
                          path=local_path)
            else:
                if d1[k] != d2[k]:
                    # ret = True
                    print(path, ":")
                    print(" - ", k, " : ", d1[k])
                    print(" + ", k, " : ", d2[k])
                    if udpate_modified_keys:
                        d1[k] = d2[k]
    for k in list(d2.keys()):
        if not k in d1:
            ret = True
            print(path, ":")
            print(" + ", k, " : ", d2[k])
            if udpate_added_keys:
                d1[k] = d2[k]

    return ret
