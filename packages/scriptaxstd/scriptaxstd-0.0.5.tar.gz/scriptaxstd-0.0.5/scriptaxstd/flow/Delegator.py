from commandtax.models.Command import Command
import traceback


class Delegator:
    def __init__(self, command: Command):
        self.command = command

    def delegate(self):
        command = self.command.command
        lib = command[0]
        method = command[1]
        command = command[2:]
        parameters = {}

        i = 0

        while len(command) > i:
            parameter = command[i]

            peek = command[1 + i]
            if parameter[0] == '-' and parameter[1] != '-':
                parameters[self.removeDashes(parameter)] = True
            else:
                parameters[self.removeDashes(parameter)] = peek
                i += 1
            i += 1

        instance = None

        if lib == 'string':
            from scriptaxstd.flow.String import String
            instance = String()
        elif lib == 'math':
            from scriptaxstd.flow.Math import Math
            instance = Math()
        elif lib == 'path':
            from scriptaxstd.flow.Path import Path
            instance = Path()
        elif lib == 'file':
            from scriptaxstd.flow.File import File
            instance = File()
        elif lib == 'time':
            from scriptaxstd.flow.Time import Time
            instance = Time()
        elif lib == 'binary':
            from scriptaxstd.flow.Binary import Binary
            instance = Binary()

        if not instance:
            print('INVALID LIBRARY')
        else:
            try:
                return getattr(instance, method)(**parameters)
            except:
                print(traceback.print_exc())
                print('LIBRARY: ' + lib + ' DOES NOT CONTAIN METHOD: ' + method)
                return None

    def removeDashes(self, passage):
        while passage[0] == '-':
            passage = passage[1:]
        return passage
