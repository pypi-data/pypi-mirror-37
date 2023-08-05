from enum import Enum


def ask_user(cmd, variables, arg_value, arg_name) -> UserChoice:
    possible_choices = (1, 2) if arg_value in variables else (1, 2, 3)
    print(cmd)
    print(f'\nVariable: {arg_name} = {arg_value}')
    print('Choices:')
    print('\t1. Do not replace.')
    print('\t2. Set variable name.')
    if len(possible_choices) == 3:
        print(f'\t3. Re-use variable {variables[arg_value]}')

    choice = input()
    while choice not in possible_choices:
        print(f'Reply must be in {possible_choices}')
        choice = input()
    return UserChoice(choice)



class UserChoice(Enum):
    DO_NOT_REPLACE = 1
    SET_NAME = 2
    REUSE_NAME = 3




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
