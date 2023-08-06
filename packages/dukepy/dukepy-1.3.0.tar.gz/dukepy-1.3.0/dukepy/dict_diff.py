def dict_diff(dict_target, dict_source,
			  udpate_modified_keys=False,
			  udpate_added_keys=False,
			  udpate_removed_keys=False,
			  path=""):
	"""
	:param dict_target: The dictionary to be modified
	:param dict_source: The dictionary to be compared with
	:param udpate_modified_keys:
	:param udpate_added_keys:
	:param udpate_removed_keys:
	:param path:
	:return: True if at least one difference.
	"""
	ret = False
	for k in list(dict_target.keys()):
		if not k in dict_source:
			ret = True
			print(path, ":")
			# print(k + " as key not in d2", "\n")
			print(" - ", k, " : ", dict_target[k])
			if udpate_removed_keys:
				dict_target.pop(k)
		else:
			if type(dict_target[k]) is dict:
				if path == "":
					local_path = k
				else:
					local_path = path + "->" + k

				res = dict_diff(dict_target[k], dict_source[k],
								udpate_modified_keys=udpate_modified_keys,
								udpate_added_keys=udpate_added_keys,
								udpate_removed_keys=udpate_removed_keys,
								path=local_path)
				if not ret:
					ret = res
			else:
				if dict_target[k] != dict_source[k]:
					# ret = True
					print(path, ":")
					print(" - ", k, " : ", dict_target[k])
					print(" + ", k, " : ", dict_source[k])
					if udpate_modified_keys:
						dict_target[k] = dict_source[k]
	for k in list(dict_source.keys()):
		if not k in dict_target:
			ret = True
			print(path, ":")
			print(" + ", k, " : ", dict_source[k])
			if udpate_added_keys:
				dict_target[k] = dict_source[k]

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
