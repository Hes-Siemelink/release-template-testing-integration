from digitalai.release.integration import BaseTask
from digitalai.release.v1.api.release_api import ReleaseApi, Release
from digitalai.release.v1.api.phase_api import PhaseApi
from digitalai.release.v1.api.task_api import TaskApi


class TestTemplate(BaseTask):

    def execute(self) -> None:

        # Get input properties
        template_name = self.input_properties['templateName']
        if not template_name:
            raise ValueError("The 'template' field cannot be empty")
        release_id = self.input_properties['releaseId']
        mock_type = self.input_properties['mockType']

        # Create the REST clients
        release_api = ReleaseApi(self.get_default_api_client())
        phase_api = PhaseApi(self.get_default_api_client())
        task_api = TaskApi(self.get_default_api_client())

        # Get base template
        base_template = release_api.search_releases_by_title(release_title=template_name)[0]
        print(f"Testing template ID: {base_template.id}")

        # Get reference release
        # XXX Deserialization of the returned release fails on attachments.
        #     Workaround is to set _check_return_type=False
        reference_release = release_api.get_release(release_id, _check_return_type=False)

        # allTasks = find_all_tasks(reference_release)

        # Copy template into this release and replace certain tasks with mocks
        for phase in base_template.phases:
            phase = convert_floats_to_ints(phase)
            print("Adding phase:")
            print(f"{phase}")
            added_phase = phase_api.add_phase(self.get_release_id(), phase=phase)

            for task in phase.tasks:
                task_api.add_task_task(added_phase.id, task=task)

              # if task.type.toString() == mockType:
              #   mockTask = taskApi.newTask('xlrelease.ScriptTask')
              #   mockTask.title = "MOCK " + task.title
              #   original, taskIndex = find_task_by_type(allTasks, mockType, taskIndex)
              #   mockTask.script = create_mock_script(original)
              #   taskApi.addTask(addedPhase.id, mockTask)
              # else:
              #   taskApi.addTask(addedPhase.id, task)


def convert_floats_to_ints(obj):
    """
    Recursively traverses an object's attributes and converts all float values to integers.

    Args:
        obj: The object to process.

    Returns:
        The modified object (modifies in place).  If the input is not an object
        with a __dict__ attribute (or a list/dict itself), it returns the original
        input unchanged.
    """

    if hasattr(obj, '__dict__'):  # Check if it's an object with attributes
        for attr_name, attr_value in obj.__dict__.items():
            if isinstance(attr_value, dict):
                convert_floats_to_ints(attr_value)  # Recurse for dicts
            elif isinstance(attr_value, list):
                convert_floats_to_ints(attr_value)  # Recurse for lists
            elif isinstance(attr_value, float):
                setattr(obj, attr_name, int(attr_value))  # Modify attribute in place
            elif hasattr(attr_value, '__dict__'):  # Recurse for other objects
                # XXX HACK to prevent infinite recursion on circular attributes.
                # Looks like only attributes injected by the API framework that start with underscore cause this
                if attr_name[0] != "_": continue
                convert_floats_to_ints(attr_value)
        return obj
    elif isinstance(obj, dict):  # Handle dictionaries
        for key, value in obj.items():
            if isinstance(value, dict):
                print(f"Recursive dict call for key: {key}")
                convert_floats_to_ints(value)  # Recurse for dicts
            elif isinstance(value, list):
                convert_floats_to_ints(value)  # Recurse for lists
            elif isinstance(value, float):
                obj[key] = int(value)  # Modify attribute in place
            elif hasattr(value, '__dict__'):  # Recurse for other objects
                convert_floats_to_ints(value)
        return obj
    elif isinstance(obj, list):  # Handle lists
        for i, item in enumerate(obj):
            if isinstance(item, dict):
                convert_floats_to_ints(item)  # Recurse for dicts
            elif isinstance(item, list):
                convert_floats_to_ints(item)  # Recurse for lists
            elif isinstance(item, float):
                obj[i] = int(item)  # Modify attribute in place
            elif hasattr(item, '__dict__'):  # Recurse for other objects
                convert_floats_to_ints(item)
        return obj
    elif isinstance(obj, float):
        return int(obj)
    else:
        return obj


def find_all_tasks(release: Release):
    tasks = []
    for phase in release.phases:
        for task in phase.tasks:
            tasks.append(task)
    return tasks

    # from com.xebialabs.xlrelease.api.v1.forms import Variable
    #
    #
    # # baseTemplate = templateApi.getTemplate(releaseVariables['templateId'])
    # baseTemplate = releaseApi.searchReleasesByTitle(releaseVariables['templateId'])[0]
    # referenceRelease = releaseApi.getRelease(releaseVariables['releaseId'])
    # mockType = releaseVariables['mockType']
    #
    # def find_all_tasks(refRel):
    #   tasks = []
    #   for phase in refRel.phases:
    #     for task in phase.tasks:
    #       tasks.append(task)
    #   return tasks
    #
    # def find_task_by_type(all, type, startIndex):
    #   for i in range(startIndex, len(all)):
    #     if all[i].type.toString() == type:
    #       return all[i], i + 1
    #
    #   raise Exception("Task not found after index %s" % startIndex)
    #
    # def create_mock_script(original):
    #
    #   # mock = original.pythonScript.getOuputProperties().toString()
    #
    #   # XXX Getting the output variable is hardcoded now, should be a proper lookup
    #   return "releaseVariables['taskId'] = '%s'" %original.getProperty('xlDeployTaskId')
    #
    # # Reference list of previously run tasks, as a flat list for simpler lookup
    # allTasks = find_all_tasks(referenceRelease)
    # taskIndex = 0
    #
    # # Copy variables.
    # # XXX Make this work
    # for variable in releaseApi.getVariables(referenceRelease.id):
    #   # print "type: %s; contents: %s" % (type(variable), variable)
    #   formVar = Variable(variable.type.toString(), variable.key, variable.getValue(), variable.requiresValue)
    #   releaseApi.createVariable(release.id, formVar)
    #
    # # Copy template into this release and replace certain tasks with mocks
    # for phase in baseTemplate.phases:
    #   print "PHASE" + phase.title
    #   addedPhase = phaseApi.addPhase(release.id, phase)
    #   for task in phase.tasks:
    #
    #     if task.type.toString() == mockType:
    #       mockTask = taskApi.newTask('xlrelease.ScriptTask')
    #       mockTask.title = "MOCK " + task.title
    #       original, taskIndex = find_task_by_type(allTasks, mockType, taskIndex)
    #       mockTask.script = create_mock_script(original)
    #       taskApi.addTask(addedPhase.id, mockTask)
    #     else:
    #       taskApi.addTask(addedPhase.id, task)
