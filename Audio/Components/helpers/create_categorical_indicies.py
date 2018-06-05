def create_category_indicies(category):
    category_index = dict((c, i) for i, c in enumerate(category))
    index_category = dict((i, c) for i, c in enumerate(category))

    return category_index, index_category


def create_lookup_indicies(categorized_variables):
    note_index, index_note = create_category_indicies(categorized_variables['note_categories'])
    length_index, index_length = create_category_indicies(categorized_variables['length_categories'])
    interval_index, index_interval = create_category_indicies(categorized_variables['interval_categories'])
    note_name_index, index_note_name = create_category_indicies(categorized_variables['note_name_categories'])

    lookup_indicies = {
        'note_index': note_index,
        'index_note': index_note,
        'length_index': length_index,
        'index_length': index_length,
        'interval_index': interval_index,
        'index_interval': index_interval,
        'note_name_index': note_name_index,
        'index_note_name': index_note_name
    }

    return lookup_indicies

