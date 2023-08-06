class RunnerAction:
    def __init__(self, short_name, name):
        self.short_name = short_name
        self.name = name


class RunnerActions:

    def __init__(self):
        pass

    get_new_round_description = RunnerAction("new", "get_new_round_description")
    deploy_to_production = RunnerAction("deploy", "deploy_to_production")

    all = [
        get_new_round_description,
        deploy_to_production,
    ]
