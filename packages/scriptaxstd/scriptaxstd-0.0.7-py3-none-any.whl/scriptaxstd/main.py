from scriptaxstd.flow.Delegator import Delegator
from commandtax.models.Command import Command

delegator = Delegator(Command(command=["string", "substr", "--text", "this_is_some_text", "--start", 0, "--length", 5]))

print(delegator.delegate())

