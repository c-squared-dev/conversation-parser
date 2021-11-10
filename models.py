from constants import excel_to_json_type_map
from utils import generate_uuid, find_node


class RapidProNodeAction:

    def __init__(self, attachments, text, type, quick_replies):
        self.attachments = attachments
        self.text = text
        self.type = type
        self.quick_replies = quick_replies
        self.uuid = generate_uuid()

    def render(self):
        return {
            "attachments": [f'image:{attachment}' for attachment in self.attachments],
            "text": self.text,
            "type": excel_to_json_type_map[self.type],
            "quick_replies": self.quick_replies,
            "uuid": self.uuid
        }


class RapidProExit:
    def __init__(self, destination_uuid):
        self.uuid = generate_uuid()
        self.destination_uuid = destination_uuid

    def render(self):
        return {
            "uuid": self.uuid,
            "destination_uuid": self.destination_uuid
        }


class RapidProCase:
    def __init__(self, argument, category_uuid):
        self.arguments = [argument]
        self.category_uuid = category_uuid
        self.type = 'has_only_phrase'
        self.uuid = generate_uuid()

    def render(self):
        return {
            "arguments": self.arguments,
            "category_uuid": self.category_uuid,
            "type": self.type,
            "uuid": self.uuid
        }


class RapidProCategory:
    def __init__(self, exit_uuid, name):
        self.exit_uuid = exit_uuid
        self.name = name
        self.uuid = generate_uuid()

    @classmethod
    def default_category(cls, exit_uuid):
        return cls(exit_uuid=exit_uuid, name='All Responses')

    def render(self):
        return {
            "exit_uuid": self.exit_uuid,
            "name": self.name,
            "uuid": self.uuid
        }


class RapidProRouter:
    def __init__(self, operand, default_category_uuid):
        self.type = 'switch'
        self.cases = []
        self.categories = []
        self.operand = operand
        self.default_category_uuid = default_category_uuid
        self.wait = {'type': 'msg'}

    def render(self):
        return {
            'type': self.type,
            'cases': [case.render() for case in self.cases],
            'categories': [category.render() for category in self.categories],
            'operand': self.operand,
            'default_category_uuid': self.default_category_uuid,
            'wait': self.wait
        }


class RapidProNode:
    def __init__(self, row_id, type, _from, condition, message_text, media, choice_1, choice_2):

        # Excel Sheet
        self.uuid = generate_uuid()
        self.row_id = row_id
        self.type = type
        self._from = _from
        self.condition = condition
        self.message_text = message_text
        self.media = media
        self.choice_1 = choice_1
        self.choice_2 = choice_2

        # Use for RapidPro
        self.actions = []
        self.exits = []

    def _get_quick_replies(self):
        return [choice for choice in [self.choice_1, self.choice_2] if choice]

    def populate_actions(self):
        self.actions.append(
            RapidProNodeAction(
                attachments=[self.media] if self.media else [],
                text=self.message_text,
                type=self.type,
                quick_replies=self._get_quick_replies()
            )
        )

    def _get_destination_nodes(self, nodes_map):
        return [node for _, node in nodes_map.items() if node._from == self.row_id]

    def add_exit(self, rapidpro_exit):
        self.exits.append(rapidpro_exit)

    def populate_exits(self, nodes_map):
        if self.choice_1 or self.choice_2:
            # populate later with patch
            return

        destination_nodes = self._get_destination_nodes(nodes_map=nodes_map)
        if destination_nodes:
            self.exits = [RapidProExit(destination_uuid=node.uuid) for node in destination_nodes]
        else:
            self.exits = [RapidProExit(destination_uuid=None)]

    def parse(self, **kwargs):
        nodes_map = kwargs.get('nodes_map')
        self.populate_actions()
        self.populate_exits(nodes_map=nodes_map)

    def render(self):
        return_dict = {
            "uuid": self.uuid,
        }

        if self.actions:
            return_dict.update({"actions": [action.render() for action in self.actions]})

        if self.exits:
            return_dict.update({"exits": [exit.render() for exit in self.exits]})
        return return_dict


class ConditionalRapidProNode(RapidProNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        default_category = RapidProCategory.default_category(exit_uuid=None)
        self.router = RapidProRouter('@input.text', default_category_uuid=None)

        self.router.categories.append(default_category)
        self.router.default_category_uuid = default_category.uuid

        self.used_conditions = set([node.condition for _, node in nodes_map.items() if node.condition])
        # Update default category UUID here

    def _populate_cases(self):
        for choice in [self.choice_1, self.choice_2]:
            if choice and choice in self.used_conditions:
                # category_uuid will be populated from _populate_categories
                self.router.cases.append(RapidProCase(argument=choice, category_uuid=None))

    def _populate_categories(self):
        for choice in [self.choice_1, self.choice_2]:
            if choice and choice in self.used_conditions:
                # Populate exit_uuid
                category = RapidProCategory(exit_uuid=None, name=choice)

                matching_case = self._find_case_with_argument_text(category.name)
                matching_case.category_uuid = category.uuid

                self.router.categories.append(category)

    def _find_case_with_argument_text(self, argument_text):
        """
        Find a case whose argument matches the text we provide. This is used to match
        the category with a case.
        :param argument_text:
        :return:
        """
        for router_case in self.router.cases:
            if router_case.arguments[0] == argument_text:
                return router_case

    def populate_actions(self):
        self.actions = []

    def populate_exits(self, nodes_map):
        for category in self.router.categories:
            if category.name == 'All Responses':
                destination_uuid = None
            else:
                next_node = find_node(nodes_map, self.row_id, condition=category.name)

                if next_node.type == 'go_to':
                    destination_uuid = next_node.get_destination_node().uuid
                else:
                    destination_uuid = next_node.uuid

            exit = RapidProExit(destination_uuid=destination_uuid)
            category.exit_uuid = exit.uuid

            self.exits.append(exit)

    def parse(self):
        self._populate_cases()
        self._populate_categories()
        super().parse()

    def render(self):
        return {
            'uuid': self.uuid,
            'actions': [action.render() for action in self.actions],
            'router': self.router.render(),
            'exits': [exit.render() for exit in self.exits]
        }


class RapidProGotoNode(RapidProNode):
    def get_destination_node(self, nodes_map):
        return nodes_map[self.message_text]
