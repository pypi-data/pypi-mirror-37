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

                ret = dict_diff(d1[k], d2[k],
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


if __name__ == "__main__":
    dictionary_1 = {"abc": "value_abc",
                    "prs": "value_prs"}
    dictionary_2 = {"abc": "value_abc",
                    "xyz": "value_xyz"}
    dict_diff(dictionary_1, dictionary_2)
    print(dictionary_1)
    print(dictionary_2)

    dict_diff(dictionary_1, dictionary_2,
              udpate_added_keys=True)

    print(dictionary_1)
    print(dictionary_2)
