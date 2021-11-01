import json
import string

import openpyxl

sheet = None

# type_column_index = None
text_column_index = None
choices_column_indexes = []


def get_maximum_rows():
    global sheet
    return sheet.max_row


def get_maximum_columns():
    global sheet
    return sheet.max_column


def read_sheet_detail():
    global sheet
    compatible_file = openpyxl.load_workbook('C:\\Users\\Usman Ali\\Downloads\\compatible_example_chat_flows.xlsx')
    sheet = compatible_file['example_story2']


def get_sheet_cell_detail(row, column):
    global sheet
    return sheet.cell(row=row, column=column).value


def get_choice_node_detail(row):
    global choices_column_indexes

    choice_type_node = {
        'uuid': 'a117eea3-8f9e-4023-aacb-404360b88c25',
        'actions': [], 'router': {'type': 'switch', 'cases': [],
        'categories': [{'exit_uuid': 'e59fda75-21e1-4d77-83a7-7733cc721eff',
        'name': 'All Responses', 'uuid': '5348fd6e-ffd3-4f11-ad59-3aa6f985a51a'}], 'operand': '@input.text',
        'default_category_uuid': '5348fd6e-ffd3-4f11-ad59-3aa6f985a51a',
        'wait': {'type': 'msg'}}, 'exits': [{'uuid': 'e59fda75-21e1-4d77-83a7-7733cc721eff', 'destination_uuid': None}],
    }

    for choice_index in choices_column_indexes:
        if get_sheet_cell_detail(row, choice_index):
            current_categories_detail = {
                'exit_uuid': 'e59fda75-21e1-4d77-83a7-7733cc721eff',
                'name': '', 'uuid': '5348fd6e-ffd3-4f11-ad59-3aa6f985a51a'
            }
            current_exist_detail = {
                'uuid': 'e59fda75-21e1-4d77-83a7-7733cc721eff', 'destination_uuid': None
            }
            current_choice_detail = {
                'arguments': [], 'category_uuid': 'd44a1630-8d47-4dda-8aa4-8bd63e3f88e5',
                'type': 'has_only_phrase', 'uuid': '2b0705fb-de25-4de6-ab96-ab098480c9ca',
            }

            choice_name = get_sheet_cell_detail(row, choice_index)

            current_categories_detail['name'] = choice_name
            current_exist_detail['destination_uuid'] = 'f79d8ec3-cc2a-4278-a1f2-9d4cd0163c48'
            current_choice_detail['arguments'].append(choice_name)

            choice_type_node['router']['categories'].append(current_categories_detail)
            choice_type_node['exits'].append(current_exist_detail)
            choice_type_node['router']['cases'].append(current_choice_detail)

    return choice_type_node


def get_last_node_detail():
    last_node_detail = {
                        'uuid': 'bf14925f-11e4-4c8d-ab4f-f8c05737d600',
                        'actions': [], 'exits': []
    }

    last_action_detail = {
                        'uuid': 'c65213c0-6c0f-409a-9993-264ef5625f38',
                        'type': 'set_contact_field', 'field': {'key': 'example_story2__completed',
                         'name': 'example_story2__completed'}, 'value': 'true'
    }

    last_exit_detail = {
                        'uuid': '0367ab86-a4a3-4116-88dd-10d36a17f829', 'destination_uuid': None
                        }

    last_node_detail['actions'].append(last_action_detail)
    last_node_detail['exits'].append(last_exit_detail)

    return last_node_detail


def get_required_column_indexes():
    # type_column_index
    global text_column_index, choices_column_indexes

    read_sheet_detail()

    for column in range(1, get_maximum_columns()):
        first_row = get_sheet_cell_detail(1, column)

        # if first_row == 'type':
        #     type_column_index = column
        if first_row == 'message_text':
            text_column_index = column
        elif first_row == 'choice_1' or first_row == 'choice_2':
            choices_column_indexes.append(column)
        elif not first_row:
            break


def get_all_nodes_detail(flows_detail):
    # type_column_index
    global text_column_index, choices_column_indexes
    global sheet

    get_required_column_indexes()

    for row in range(2, get_maximum_rows()):
        if not get_sheet_cell_detail(row, 2):
            break

        if get_sheet_cell_detail(row, text_column_index) == 2:
            continue

        choices = []

        text_type_node = {
            'uuid': '0500fc07-6f4e-4f04-8cb4-c39985d8a971',
            'actions': [], 'exits': [],
        }
        text_action_detail = {
            'attachments': [], 'text': get_sheet_cell_detail(row, text_column_index),
            'type': 'send_msg', 'quick_replies': [],
            'uuid': '0500fc07-6f4e-4f04-8cb4-c39985d8a971'
        }
        text_exist_detail = {
            'uuid': '8874dfdb-31da-4880-83cc-a6b6a7ff6f04',
            'destination_uuid': 'a117eea3-8f9e-4023-aacb-404360b88c25'
        }

        for choice in choices_column_indexes:
            choice_text = get_sheet_cell_detail(row, choice)

            if choice_text:
                choices.append(choice_text)

        for choice in choices:
            text_action_detail['quick_replies'].append(choice)

        text_type_node['actions'].append(text_action_detail)
        text_type_node['exits'].append(text_exist_detail)

        flows_detail['nodes'].append(text_type_node)

        if choices:
            flows_detail['nodes'].append(get_choice_node_detail(row))


def get_detail_in_flows():
    flows_detail = {
        'name': 'example_story2', 'uuid': 'd299b770-3cf9-4dcd-81da-4c0f04da2872',
        'spec_version': '13.1.0', 'language': 'base', 'type': 'messaging',
        'nodes': [], '_ui': None, 'revision': 0, 'expire_after_minutes': 60,
        'metadata': {'revision': 0}, 'localization': {}
    }

    flows_detail['nodes'].append(get_all_nodes_detail(flows_detail))
    flows_detail['nodes'].append(get_last_node_detail())

    return flows_detail


if __name__ == '__main__':
    complete_sheet_detail = {
        'campaigns': [], 'fields': [], 'flows': [], 'groups': [],
        'site': 'https://rapidpro.idems.international',
        'triggers': [], 'version': '13',
    }

    complete_sheet_detail['flows'].append(get_detail_in_flows())

    with open('file_detail.json', 'w') as sheet_detail:
        json.dump(complete_sheet_detail, sheet_detail)
