"""
The eoworkflow module, together with eotask and eodata, provides core building blocks for specifying and executing
workflows.

A workflow is a directed (acyclic) graph composed of instances of EOTask objects. Each task may take as input the
results of other tasks and external arguments. The external arguments are passed anew each time the workflow is
executed. The workflow builds the computational graph, performs dependency resolution, and executes the tasks.
If the input graph is cyclic, the workflow raises a `CyclicDependencyError`.

The result of a workflow execution is an immutable mapping from tasks to results. The result contains tasks with
zero out-degree (i.e. terminal tasks).

The workflow can be exported to a DOT description language and visualized.
"""

import collections
import logging
import warnings
import uuid

# the next are needed for DAG visualization only
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

from copy import deepcopy

from .eotask import EOTask
from .graph import DirectedGraph


LOGGER = logging.getLogger(__file__)


class CyclicDependencyError(ValueError):
    pass


class EOWorkflow:
    """The constructor to instantiate a workflow from a list of dependencies.

    :param dependencies: A list of dependencies between tasks, specifying the computational graph.
    :type dependencies: list(tuple or Dependency)
    :param task_names: A dictionary providing human-readable names to EOTask's, defaults to ``None``
    :type task_names: dict(EOTask: str) or None
    """
    def __init__(self, dependencies, task_names=None):
        self.id_gen = _UniqueIdGenerator()

        self.dependencies = self._parse_dependencies(dependencies, task_names)
        self.uuid_dict = self._set_task_uuid(self.dependencies)
        self.dag = self.create_dag(self.dependencies)
        self.ordered_dependencies = self._schedule_dependencies(self.dag)

    @staticmethod
    def _parse_dependencies(dependencies, task_names):
        """Parses dependencies and adds names of task_names.

        :param dependencies: Input of dependency parameter
        :type dependencies: list(tuple or Dependency)
        :param task_names: Human-readable names of tasks
        :type task_names: dict(EOTask: str) or None
        :return: List of dependencies
        :rtype: list(Dependency)
        """
        parsed_dependencies = [dep if isinstance(dep, Dependency) else Dependency(*dep) for dep in dependencies]
        for dep in dependencies:
            if task_names and dep.task in task_names:
                dep.set_name(task_names[dep.task])
        return parsed_dependencies

    def _set_task_uuid(self, dependencies):
        """Adds universally unique user ids (UUID) to each task of the workflow.

        :param dependencies: The list of dependencies between tasks defining the computational graph
        :type dependencies: list(Dependency)
        :return: A dictionary mapping UUID to dependencies
        :rtype: dict(str: Dependency)
        """
        uuid_dict = {}
        for dep in dependencies:
            task = dep.task
            if task.uuid in uuid_dict:
                raise ValueError('EOWorkflow cannot execute the same instance of EOTask multiple times')

            task.uuid = self.id_gen.next()
            uuid_dict[task.uuid] = dep

        return uuid_dict

    def create_dag(self, dependencies):
        """Creates a directed graph from dependencies.

        :param dependencies: A list of Dependency objects
        :type dependencies: list(Dependency)
        :return: A directed graph of the workflow
        :rtype: DirectedGraph
        """
        dag = DirectedGraph()

        for dep in dependencies:
            for vertex in dep.inputs:
                dag.add_edge(self.uuid_dict[vertex.uuid], dep)
            if not dep.inputs:
                dag.add_vertex(dep)
        return dag

    @staticmethod
    def _schedule_dependencies(dag):
        """
        Computes an ordering < of tasks so that for any two tasks t and t' we have that if t depends on t' then
        t' < t. In words, all dependencies of a task precede the task in this ordering.

        :param dag: A directed acyclic graph representing dependencies between tasks.
        :type dag: DirectedGraph
        :return: A list of topologically ordered dependecies
        :rtype: list(Dependency)
        """
        in_degrees = dict(dag.get_indegrees())

        independent_vertices = collections.deque([vertex for vertex in dag if dag.get_indegree(vertex) == 0])
        topological_order = []
        while independent_vertices:
            v_vertex = independent_vertices.popleft()
            topological_order.append(v_vertex)

            for u_vertex in dag[v_vertex]:
                in_degrees[u_vertex] -= 1
                if in_degrees[u_vertex] == 0:
                    independent_vertices.append(u_vertex)

        if len(topological_order) != len(dag):
            raise CyclicDependencyError('Tasks do not form an acyclic graph')

        return topological_order

    @staticmethod
    def make_linear_workflow(*tasks, **kwargs):
        """Factory method for creating linear workflows.

        :param tasks: EOTask's t1,t2,...,tk with dependencies t1->t2->...->tk
        :param kwargs: Optional keyword arguments (such as workflow name) forwarded to the constructor
        :return: A new EO workflow instance
        :rtype: EOWorkflow
        """
        warnings.warn('This method will soon be removed. Use LinearWorkflow class instead', DeprecationWarning)

        return LinearWorkflow(*tasks, **kwargs)

    def execute(self, input_args=None, monitor=False):
        """Executes the workflow.

        :param input_args: External input arguments to the workflow.
        :type input_args: dict(EOTask: dict(str: object))
        :param monitor: If True workflow execution will be monitored
        :type monitor: bool
        :return: An immutable mapping containing results of terminal tasks
        :rtype: WorkflowResults
        """
        out_degs = dict(self.dag.get_outdegrees())

        input_args = input_args if input_args else {}
        for task in input_args:
            if not isinstance(task, EOTask):
                raise ValueError('Invalid input argument {}, should be an instance of EOTask'.format(task))

        _, intermediate_results = self._execute_tasks(input_args=input_args, out_degs=out_degs, monitor=monitor)

        return WorkflowResults(intermediate_results)

    def _execute_tasks(self, *, input_args, out_degs, monitor):
        """Executes tasks comprising the workflow in the predetermined order.

        :param input_args: External input arguments to the workflow.
        :type input_args: Dict
        :param out_degs: Dictionary mapping vertices (task IDs) to their out-degrees. (The out-degree equals the number
        of tasks that depend on this task.)
        :type out_degs: Dict
        :return: An immutable mapping containing results of terminal tasks
        :rtype: WorkflowResults
        """
        done_tasks = set()

        intermediate_results = {}

        for dep in self.ordered_dependencies:
            result = self._execute_task(dependency=dep,
                                        input_args=input_args,
                                        intermediate_results=intermediate_results,
                                        monitor=monitor)

            intermediate_results[dep] = result

            self._relax_dependencies(dependency=dep,
                                     out_degrees=out_degs,
                                     intermediate_results=intermediate_results)

        return done_tasks, intermediate_results

    def _execute_task(self, *, dependency, input_args, intermediate_results, monitor):
        """Executes a task of the workflow.

        :param dependency: A workflow dependecy
        :type dependency: Dependency
        :param input_args: External task parameters.
        :type input_args: dict
        :param intermediate_results: The dictionary containing intermediate results, including the results of all
        tasks that the current task depends on.
        :type intermediate_results: dict
        :return: The result of the task in dependency
        :rtype: object
        """
        task = dependency.task
        kw_inputs = input_args.get(task, {})
        inputs = tuple(intermediate_results[self.uuid_dict[input_task.uuid]] for input_task in dependency.inputs)
        LOGGER.debug("Computing %s(*%s, **%s)", str(task), str(inputs), str(kw_inputs))
        return task(*inputs, **kw_inputs, monitor=monitor)

    def _relax_dependencies(self, *, dependency, out_degrees, intermediate_results):
        """
        Relaxes dependencies incurred by ``task_id``. After the task with ID ``task_id`` has been successfully
        executed, all the tasks it depended on are upadted. If ``task_id`` was the last remaining dependency of a task
        ``t`` then ``t``'s result is removed from memory and, depending on ``remove_intermediate``, from disk.

        :param dependency: A workflow dependecy
        :type dependency: Dependency
        :param out_degrees: Out-degrees of tasks
        :type out_degrees: dict
        :param intermediate_results: The dictionary containing the intermediate results (needed by tasks that have yet
        to be executed) of the already-executed tasks
        :type intermediate_results: dict
        """
        current_task = dependency.task
        for input_task in dependency.inputs:
            dep = self.uuid_dict[input_task.uuid]
            out_degrees[dep] -= 1

            if out_degrees[dep] == 0:
                LOGGER.debug("Removing intermediate result for %s", str(current_task))
                del intermediate_results[dep]

    def get_dot(self):
        """Generates the DOT description of the underlying computational graph.

        :return: The DOT representation of the computational graph
        :rtype: Digraph
        """
        dot = Digraph()
        dep_to_dot_name = self._get_dep_to_dot_name_mapping(self.ordered_dependencies)

        for dep in self.ordered_dependencies:
            for input_task in dep.inputs:
                dot.edge(dep_to_dot_name[self.uuid_dict[input_task.uuid]],
                         dep_to_dot_name[dep])
        return dot

    @staticmethod
    def _get_dep_to_dot_name_mapping(dependencies):
        dot_name_to_deps = {}
        for dep in dependencies:
            dot_name = EOWorkflow._get_dot_name(dep)

            if dot_name not in dot_name_to_deps:
                dot_name_to_deps[dot_name] = [dep]
            else:
                dot_name_to_deps[dot_name].append(dep)

        dep_to_dot_name = {}
        for dot_name, deps in dot_name_to_deps.items():
            if len(deps) == 1:
                dep_to_dot_name[deps[0]] = dot_name
                continue

            for idx, dep in enumerate(deps):
                dep_to_dot_name[dep] = dot_name + str(idx)

        return dep_to_dot_name

    @staticmethod
    def _get_dot_name(dependency):
        """Generates names of tasks used in dot graph."""
        return dependency.get_task_name()

    def dependency_graph(self, outfile, view=False):
        """Visualize the computational graph.

        :param outfile: The name of the output image of the graph.
        :type outfile: str
        :param view: A flag indicating whether to view the image of the graph
        :type view: bool
        """
        dot = self.get_dot()

        with open(outfile, 'w') as fout:
            fout.write(dot.source)

        if view:
            graph = nx.drawing.nx_pydot.read_dot(outfile)
            nx.draw(graph, with_labels=True)
            plt.show()


class LinearWorkflow(EOWorkflow):
    """A linear version of EOWorkflow where each tasks only gets results of the previous task.

    :param tasks: Tasks in the order of execution
    :type tasks: *EOTask
    :param task_names: A dictionary providing human-readable names to EOTask's (optional); defaults to ``None``
    :type task_names: Dict
    """
    def __init__(self, *tasks, **kwargs):
        tasks = self._make_tasks_unique(tasks)
        dependencies = [(task, [tasks[idx - 1]] if idx > 0 else []) for idx, task in enumerate(tasks)]

        super().__init__(dependencies, **kwargs)

    @staticmethod
    def _make_tasks_unique(tasks):
        """If some tasks of the workflow are the same they are deep copied."""
        unique_tasks = []
        prev_tasks = set()

        for task in tasks:
            if task in prev_tasks:
                task = deepcopy(task)
            unique_tasks.append(task)

        return unique_tasks


class Dependency:
    """Class representing a node in EOWorkflow graph."""
    def __init__(self, task=None, inputs=None, name=None, transform=None):
        if transform is not None:
            warnings.warn("Parameter 'transform' has been renamed to 'task' and will soon be removed",
                          DeprecationWarning)
            if task is None:
                task = transform

        if not isinstance(task, EOTask):
            raise ValueError('Value {} should be an instance of {}'.format(task, EOTask.__name__))
        self.task = task

        if inputs is None:
            inputs = []
        if isinstance(inputs, EOTask):
            inputs = [inputs]
        if not isinstance(inputs, (list, tuple)):
            raise ValueError('Value {} should be a list'.format(inputs))
        for input_task in inputs:
            if not isinstance(input_task, EOTask):
                raise ValueError('Value {} should be an instance of {}'.format(input_task, EOTask.__name__))
        self.inputs = inputs

        self.name = name

    def set_name(self, name):
        """Sets a new name."""
        self.name = name

    def get_task_name(self):
        """Returns a name of the task in dependency."""
        if self.name:
            return self.name
        return type(self.task).__name__

    def __repr__(self):
        return self.get_task_name()


class WorkflowResults(collections.Mapping):
    """The result of a workflow is an (immutable) dictionary mapping [1] from EOTasks to results of the workflow.

    When an EOTask is passed as an index, its UUID, assigned during workflow execution, is used as the key (as opposed
    to the result of invoking __repr__ on the EO task). This ensures that indexing by task works even after pickling,
    and makes dealing with checkpoints more convenient.

    [1] https://docs.python.org/3.6/library/collections.abc.html#collections-abstract-base-classes
    """
    def __init__(self, results):
        self._result = dict(results)
        self._uuid_dict = {dep.task.uuid: dep for dep in results}

    def __getitem__(self, item):
        if isinstance(item, EOTask):
            item = self._uuid_dict[item.uuid]
        return self._result[item]

    def __len__(self):
        return len(self._result)

    def __iter__(self):
        return iter(self._result)

    def __contains__(self, item):
        if isinstance(item, EOTask):
            item = self._uuid_dict[item.uuid]
        return item in self._result

    def __eq__(self, other):
        return self._result == other

    def __ne__(self, other):
        return self._result != other

    def keys(self):
        return {dep.task: None for dep in self._result}.keys()

    def values(self):
        return self._result.values()

    def items(self):
        return {dep.task: value for dep, value in self._result.items()}.items()

    def get(self, key, default=None):
        if isinstance(key, EOTask):
            key = self._uuid_dict[key.uuid]
        return self._result.get(key, default)

    def __repr__(self):
        repr_list = ['{}('.format(self.__class__.__name__)]

        for _, dep in self._uuid_dict.items():
            repr_list.append('{}({}): {}'.format(Dependency.__name__, dep.get_task_name(),
                                                 repr(self._result[dep])))

        return '\n  '.join(repr_list) + '\n)'


class _UniqueIdGenerator:
    """Generator of unique IDs, which is used in workflows only."""

    MAX_UUIDS = 2 ** 20

    def __init__(self):
        self.uuids = set()

    def _next(self):
        if len(self.uuids) + 1 > _UniqueIdGenerator.MAX_UUIDS:
            raise MemoryError('Limit of max UUIDs reached')

        while True:
            uid = uuid.uuid4()
            if uid not in self.uuids:
                self.uuids.add(uid)
                return uid

    def next(self):
        """Generates an ID."""
        return self._next().hex
