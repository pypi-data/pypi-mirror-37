from enum import Enum


class UserChoice(Enum):
    DO_NOT_REPLACE = 1
    SET_NAME = 2
    REUSE_NAME = 3


class ChoiceBuilder:

    def __init__(self):
        self.available_choices = []

    def add_choice(self, message: str) -> 'ChoiceBuilder':
        self.available_choices.append(message)
        return self

    def add_conditional_choice(self, condition: bool, message: str) -> 'ChoiceBuilder':
        if condition:
            return self.add_choice(message)
        return self

    def ask_user(self, prefix_message: str = None, suffix_message: str = None):
        if prefix_message:
            print(prefix_message)

        print('Choices')
        for idx, choice in enumerate(self.available_choices):
            print(f'\t{idx + 1}. {choice}')
        print()
        possible_choices = [str(nb) for nb in range(1, len(self.available_choices) + 1)]
        ask_message = 'Please enter your choice number: '
        choice = input(ask_message)
        while choice not in possible_choices:
            print(f'Choice must be in {possible_choices}.')
            choice = input(ask_message)

        if suffix_message:
            print(suffix_message)
        return choice


def ask_user(cmd, variables, arg_value, arg_name) -> UserChoice:
    choice_builder = ChoiceBuilder() \
        .add_choice('Do not replace') \
        .add_choice('Set variable name') \
        .add_conditional_choice(arg_value in variables, 'Re-use variable {variables.get(arg_value)}')

    user_choice = choice_builder.ask_user(prefix_message=f'\nCMD: {cmd}\nVariable: {arg_name} = {arg_value}\n')
    return UserChoice(int(user_choice))


def apply_user_choice(user_choice: UserChoice, cmd: str, arg_value: str, suggested_name: str = None):
    if user_choice == UserChoice.DO_NOT_REPLACE:
        return cmd, None
    if user_choice == UserChoice.REUSE_NAME and suggested_name:
        return cmd.replace(arg_value, suggested_name), None
    if user_choice == UserChoice.SET_NAME:
        var_name = input('variable name:')
        sanitized_var_name = to_bash_variable(var_name)
        cmd = cmd.replace(arg_value, sanitized_var_name)
        if sanitized_var_name != var_name:
            print(f'Command line is updated with sanitized var_name {cmd}')
        return cmd, sanitized_var_name
