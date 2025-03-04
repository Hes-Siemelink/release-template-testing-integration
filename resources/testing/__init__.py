from __future__ import print_function

def find_all_tasks(refRel):
  tasks = []
  for phase in refRel.phases:
    for task in phase.tasks:
      tasks.append(task)
  return tasks

def find_task_by_type(all, type, startIndex):
  for i in range(startIndex, len(all)):
    if all[i].type.toString() == type:
      return all[i], i + 1

  raise Exception("Task not found after index %s" % startIndex)

def create_mock_script(template_task, executed_task):

  print("### Task: {0}".format(template_task.title))
  script = ""
  for output_property in get_output_properties(template_task):
    print("Output property: {0}".format(output_property))

    variable = template_task.variableMapping[output_property]
    print("Variable: {0}".format(variable))

    if not variable: continue
    variable_name = remove_prefix_suffix(variable)
    script +=  "releaseVariables['{0}'] = '{1}'".format(variable_name, executed_task.getProperty(output_property))
    script += "\n"

  return script

def get_output_properties(task):
  vars = []
  type = task.getType()
  for prop in type.getDescriptor().getPropertyDescriptors():
    if prop.category == 'output':
      vars.append(prop.getName())

  return vars

#
# Util
#

def print_code(title, code):
  print("### {0}".format(title))
  print("```")
  print("{0}".format(code))
  print("```")
  print("")

def remove_prefix_suffix(s, prefix="${", suffix="}"):
  """Removes a given prefix and suffix from a string.

  Args:
    s: The input string.
    prefix: The prefix to remove.
    suffix: The suffix to remove.

  Returns:
    The string with the prefix and suffix removed, or the original string
    if the prefix or suffix is not found.
  """

  if s.startswith(prefix) and s.endswith(suffix):
    return s[len(prefix):-len(suffix)]
  else:
    return s
