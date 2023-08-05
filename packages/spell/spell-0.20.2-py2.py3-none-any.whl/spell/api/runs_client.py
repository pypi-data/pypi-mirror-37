import json
from datetime import datetime
from six.moves import urllib

from requests.exceptions import ChunkedEncodingError

from spell.api import base_client
from spell.api.exceptions import ClientException, JsonDecodeError, WaitError
from spell.api.utils import url_path_join, to_RFC3339_string


RUNS_RESOURCE_URL = "runs"

LOGS_RESOURCE_URL = "logs"
LS_RESOURCE_URL = "ls"
KILL_RESOURCE_URL = "kill"
STOP_RESOURCE_URL = "stop"
COPY_RESOURCE_URL = "cp"
STATS_RESOURCE_URL = "stats"
WAIT_STATUS_RESOURCE_URL = "wait_status"
WAIT_METRIC_RESOURCE_URL = "wait_metric"
METRICS_RESOURCE_URL = "user-metrics"


class RunRequest:
    """
    A class used to encapsulate all of the specifications of a Run

    Keyword arguments:
    machine_type -- which machine_type to use for the actual run
    command -- the command to run on this workspaces
    workspace_id -- the id of the workspace for this repo
    commit_hash -- the current commit hash on the repo to run
    commit_label -- the commit label for the workspace/commit hash, if the run is associated with a workflow
    cwd -- the current working directory that the user ran this cmd in
    root_directory -- the name of the top level directory for the git repository
    pip_packages -- list of pip dependencies to install
    apt_packages -- list of apt dependencies to install
    docker_image -- name of docker image to use as base
    framework -- Spell framework to use for the run, must be specified if docker_image not given
    framework_version -- Version of Spell framework to use for the run
    python2 -- a boolean indicating whether python version should be set to python 2
    attached_resources -- ids and mount points of runs to attach
    description -- a human readable description of this run
    envvars -- environment variables to set
    conda_file -- contents of conda environment.yml
    conda_name -- name of conda environment to activate in run
    local_caching -- turn on local caching of attached resources
    run_type -- type of run
    idempotent -- should we use an existing identical run
    local_root -- Used for jupyter runs
    workflow_id -- ID of the workflow to associate this run to
    """
    def __init__(self, machine_type="CPU", command=None, workspace_id=None, commit_hash=None, commit_label=None,
                 cwd=None, root_directory=None, pip_packages=None, apt_packages=None, docker_image=None, framework=None,
                 framework_version=None, python2=None, attached_resources=None, description=None,
                 envvars=None, conda_file=None, conda_name=None, local_caching=False, run_type="user",
                 idempotent=False, local_root=None, workflow_id=None):
        self.machine_type = machine_type
        self.command = command
        self.workspace_id = workspace_id
        self.commit_hash = commit_hash
        self.commit_label = commit_label
        self.cwd = cwd
        self.root_directory = root_directory
        self.pip_packages = pip_packages
        self.apt_packages = apt_packages
        self.docker_image = docker_image
        self.framework = framework
        self.framework_version = framework_version
        self.python2 = python2
        self.description = description
        self.envvars = envvars
        self.attached_resources = {name: {"mount_point": attached_resources[name]}
                                   for name in attached_resources} if attached_resources else None
        self.conda_file = conda_file
        self.conda_name = conda_name
        self.local_caching = local_caching
        self.run_type = run_type
        self.idempotent = idempotent
        self.local_root = local_root
        self.workflow_id = workflow_id

    def to_payload(self):
        return {
            "command": self.command,
            "workspace_id": self.workspace_id,
            "gpu": self.machine_type,
            "pip_packages": self.pip_packages if self.pip_packages is not None else [],
            "apt_packages": self.apt_packages if self.apt_packages is not None else [],
            "docker_image": self.docker_image,
            "framework": self.framework,
            "framework_version": self.framework_version,
            "python2": self.python2,
            "git_commit_hash": self.commit_hash,
            "description": self.description,
            "environment_vars": self.envvars,
            "attached_resources": self.attached_resources,
            "conda_file": self.conda_file,
            "conda_name": self.conda_name,
            "run_type": self.run_type,
            "local_caching": self.local_caching,
            "cwd": self.cwd,
            "root_directory": self.root_directory,
            "idempotent": self.idempotent,
            "workflow_id": self.workflow_id,
            "commit_label": self.commit_label,
        }


class RunsClient(base_client.BaseClient):

    def run(self, run_req):
        r = self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner), payload=run_req.to_payload())
        self.check_and_raise(r)
        resp = self.get_json(r)
        run = resp["run"]
        if "already_existed" in resp and resp["already_existed"]:
            run.already_existed = True
        return run

    def list_runs(self, workspace_ids=None):
        """Get a list of runs.

        Keyword arguments:
        workspace_ids -- the ids of the workspaces to filter the runs by [OPTIONAL]

        Returns:
        a list of Run objects for this user

        """
        url = url_path_join(RUNS_RESOURCE_URL, self.owner)
        if workspace_ids is not None:
            url += "?" + urllib.parse.urlencode([('workspace_id', workspace_id) for workspace_id in workspace_ids])
        r = self.request("get", url)
        self.check_and_raise(r)
        return self.get_json(r)["runs"]

    def get_run(self, run_id):
        """Get a run.

        Keyword arguments:
        run_id -- the id of the run

        Returns:
        a Run object
        """
        r = self.request("get", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id))
        self.check_and_raise(r)
        return self.get_json(r)["run"]

    def get_run_log_entries(self, run_id, follow, offset):
        """Get log entries for a run.

        Keyword arguments:
        run_id -- the id of the run
        follow -- true if the logs should be followed
        offset -- which log line to start from

        Returns:
        a generator for entries of run logs
        """
        finished = False
        while not finished:
            if offset is None:
                raise ClientException("Missing log stream offset")
            payload = {"follow": follow, "offset": offset}
            with self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, LOGS_RESOURCE_URL),
                              payload=payload, stream=True) as log_stream:
                self.check_and_raise(log_stream)
                try:
                    if log_stream.encoding is None:
                        log_stream.encoding = 'utf-8'
                    for chunk in log_stream.iter_lines(decode_unicode=True):
                        try:
                            chunk = json.loads(chunk, cls=base_client.SpellDecoder)
                        except ValueError as e:
                            message = "Error decoding the log response chunk: {}".format(e)
                            raise JsonDecodeError(msg=message, response=log_stream, exception=e)
                        offset = chunk.get("next_offset", offset)
                        logEntry = chunk.get("log_entry")
                        finished = chunk.get("finished")
                        if logEntry:
                            yield logEntry
                        elif finished:
                            break
                except ChunkedEncodingError:
                    continue  # Try reconnecting

    def remove_run(self, run_id):
        """Soft delete a run, don't show in ps or ls.

        Keyword arguments:
        run_id -- the id of the run to remove

        Returns:
        nothing if successful
        """
        r = self.request("delete", url_path_join(RUNS_RESOURCE_URL, self.owner, str(run_id)))
        self.check_and_raise(r)

    def kill_run(self, run_id):
        """Kill a currently running run.

        Keyword arguments:
        run_id -- the id of the run
        """
        r = self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, KILL_RESOURCE_URL))
        self.check_and_raise(r)

    def stop_run(self, run_id):
        """Stop a currently running run.

        Keyword arguments:
        run_id -- the id of the run to stop
        """
        r = self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, STOP_RESOURCE_URL))
        self.check_and_raise(r)

    def get_stats(self, run_id, follow=False):
        """Get statistics for a run.

        Keyword arguments:
        run_id -- the id of the run

        Returns:
        a generator of (cpu_stats, gpu_stats) tuples for the run
        """
        finished = False
        while not finished:
            payload = {"follow": follow}
            with self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, STATS_RESOURCE_URL),
                              payload=payload, stream=True) as stats_stream:
                self.check_and_raise(stats_stream)
                try:
                    if stats_stream.encoding is None:
                        stats_stream.encoding = 'utf-8'
                    for chunk in stats_stream.iter_lines(decode_unicode=True):
                        try:
                            chunk = json.loads(chunk, cls=base_client.SpellDecoder)
                        except ValueError as e:
                            message = "Error decoding the stats response chunk: {}".format(e)
                            raise JsonDecodeError(msg=message, response=stats_stream, exception=e)
                        cpu_stats, gpu_stats = chunk.get("cpu_stats"), chunk.get("gpu_stats")
                        finished = chunk.get("finished")
                        if cpu_stats:
                            yield (cpu_stats, gpu_stats)
                        elif finished:
                            break
                except ChunkedEncodingError:
                    continue  # Try reconnecting

    def get_run_metrics(self, run_id, metric_name, follow=False, offset=None):
        """Get user metrics for a run

        Keyword arguments:
        run_id -- the id of the run
        metric_name -- the metric name
        follow -- true if metrics should be followed until the run is complete
        offset -- a datetime.datetime object specifying a time offset to start from.
            offset is exclusive (i.e., returned metrics will be > offset)

        Returns:
        a generator of metrics for the run
        """
        finished = False
        if offset:
            offset = to_RFC3339_string(offset)
        while not finished:
            payload = {"metrics": [{"name": metric_name, "offset": offset}], "follow": follow}
            with self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, METRICS_RESOURCE_URL),
                              payload=payload, stream=True) as metric_stream:
                self.check_and_raise(metric_stream)
                if metric_stream.encoding is None:
                    metric_stream.encoding = 'utf-8'
                try:
                    for chunk in metric_stream.iter_lines(decode_unicode=True):
                        chunk = json.loads(chunk)
                        if chunk.get("connected"):
                            # initial connection chunk of long-lived response
                            continue
                        metrics = chunk.get("metrics_by_name")
                        if metrics:
                            for metric in metrics[metric_name]["data"]:
                                offset = metric[0]
                                timestamp = datetime.strptime(metric[0], "%Y-%m-%dT%H:%M:%S.%fZ")
                                index = metric[1]
                                value = metric[2]
                                yield (timestamp, index, value)
                        finished = chunk.get("finished") or not metric_stream.headers.get("stream")
                        if finished:
                            break
                except ChunkedEncodingError:
                    continue  # Try reconnecting
                except ValueError as e:
                    message = "Error decoding the metric response chunk: {}".format(e)
                    raise JsonDecodeError(msg=message, response=metric_stream, exception=e)

    def wait_status(self, run_id, *statuses):
        """Wait for a run to reach a given status.

        Keyword arguments:
        run_id -- the id of the run to wait on
        statuses -- variable length list of status to wait for. Allowed values: "building", "running", "saving",
            "pushing", "complete", "failed", "killed", "stopped"
        """
        payload = {"statuses": statuses}
        finished = False
        while not finished:
            with self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, WAIT_STATUS_RESOURCE_URL),
                              payload=payload, stream=True) as status_stream:
                self.check_and_raise(status_stream)
                try:
                    if status_stream.encoding is None:
                        status_stream.encoding = 'utf-8'
                    for chunk in status_stream.iter_lines(decode_unicode=True):
                        try:
                            chunk = json.loads(chunk)
                        except ValueError as e:
                            message = "Error decoding the wait status response: {}".format(e)
                            raise JsonDecodeError(msg=message, response=status_stream, exception=e)
                        if chunk.get("success") is None:
                            # this is initial connection message
                            continue
                        finished = True
                        if chunk.get("success"):
                            return
                        else:
                            raise WaitError(msg=chunk.get("error"), response=status_stream)
                except ChunkedEncodingError:
                    continue  # Try reconnecting

    def wait_metric(self, run_id, metric_name, condition, value):
        """Wait for a run metric to reach a given condition.

        Keyword arguments:
        run_id -- the id of the run to wait on
        metric_name -- the name of the metric to wait on
        condition -- condition to wait for. Allowed values: "eq", "gt", "gte", "lt", "lte"
        value -- the value to evaluate the condition against
        """
        payload = {"metric_name": metric_name, "condition": condition, "value": value}
        finished = False
        while not finished:
            with self.request("post", url_path_join(RUNS_RESOURCE_URL, self.owner, run_id, WAIT_METRIC_RESOURCE_URL),
                              payload=payload, stream=True) as metric_stream:
                self.check_and_raise(metric_stream)
                try:
                    if metric_stream.encoding is None:
                        metric_stream.encoding = 'utf-8'
                    for chunk in metric_stream.iter_lines(decode_unicode=True):
                        try:
                            chunk = json.loads(chunk)
                        except ValueError as e:
                            message = "Error decoding the wait metric response: {}".format(e)
                            raise JsonDecodeError(msg=message, response=metric_stream, exception=e)
                        if chunk.get("success") is None:
                            # this is initial connection message
                            continue
                        finished = True
                        if chunk.get("success"):
                            return
                        else:
                            raise WaitError(msg=chunk.get("error"), response=metric_stream)
                except ChunkedEncodingError:
                    continue  # Try reconnecting
