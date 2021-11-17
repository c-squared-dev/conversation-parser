import uuid


class RapidProAction:
    def render(self, text, type):
        return {
            'uuid': uuid.uuid4(),
            'text': text,
            'type': type,
        }


class Exit:
    def render(self, uuid):
        return {
            'destination_uuid': None,   # get_destination_uuid,
            'uuid': uuid,
        }


class RapidProNode:
    def __init(self, uuid, text, type):
        self.uuid = uuid
        self.text = text
        self.type = type

        self.actions = []
        self.exits = []

    def get_rapid_pro_action(self):
        rapid_pro_node_action = RapidProAction()
        self.actions.append(rapid_pro_node_action.render(self.text, self.type))

    def get_rapid_pro_exit(self):
        rapid_pro_exit = Exit(
            # get_destination_uuid(),
            uuid.uuid4(),
        )

        self.exits.append(rapid_pro_exit.render())

    def render(self):
        return {
            'uuid': self.uuid,
            'actions': self.actions,
            'exits': self.actions,
        }


class RouterCategory:
    def render(self, choice):
        return {
            'uuid': uuid.uuid4(),
            'name': choice if choice else 'All Responses',
            'exit_uuid': uuid.uuid4(),
        }


class RouterCases:
    def render(self, choice, category_uuid):
        return {
            'uuid': uuid.uuid4(),
            'name': choice,
            'exit_uuid': category_uuid,
        }


class AbstractRouter:
    def __init__(self, choices=None):
        self.choices = choices
        self.categories = []
        self.cases = []
        self.default_category_uuid = None
        self.exits = []

    def get_router_detail(self):
        router_category = RouterCategory()
        router_exit = Exit()
        router_case = RouterCases()

        current_category = router_category.render(None)

        self.categories.append(current_category)
        self.exits.append(router_exit.render(current_category['exit_uuid']))
        self.default_category_uuid = current_category['uuid']

        for choice in self.choices:
            current_category = router_category.render(None)

            self.categories.append(current_category)
            self.exits.append(router_exit.render(current_category['exit_uuid']))
            self.cases.append(router_case.render(choice, current_category['uuid']))

    def render(self):
        return {
            'type': 'switch',
            'categories': self.categories,
            'operand': '@input',
            'cases': self.cases,
            'default_category_uuid': self.default_category_uuid,

        }


class SwitchRouter(AbstractRouter):
    def __init__(self, choices):
        self.choices = choices

        self.router = {}

    def render(self):
        abstract_router = AbstractRouter(self.choices)

        current_router = abstract_router.render()

        self.router.update(current_router)

        return {
            'uuid': uuid.uuid4(),
            'router': self.router,
            'exits': current_router['exits']
        }


class RandomRouter:
    def __init__(self):
        self.choices = None
        self.router = {}

    def render(self):
        abstract_router = AbstractRouter(self.choices)

        current_router = abstract_router.render()

        self.router.update(current_router)

        return {
            'uuid': uuid.uuid4(),
            'router': self.router,
            'exits': current_router['exits']
        }
