class ParseException(Exception):
    def __init__(self, message, token):
        super(ParseException, self).__init__(message)
        self.token = token


def parse_attached_resources(raw):
    attached_resources = {}
    for token in raw:
        chunks = token.split(':')
        if len(chunks) == 1:
            resource_name, path = token, ""
        elif len(chunks) == 2:
            resource_name, path = chunks
        else:
            raise ParseException("Invalid attached resource value", token)
        attached_resources[resource_name] = path
    return attached_resources


def parse_env_vars(raw):
    envvars = {}
    for envvar_str in raw:
        key_val_split = envvar_str.split('=')
        key = key_val_split[0]
        val = '='.join(key_val_split[1:])
        envvars[key] = val
    return envvars


def parse_repos(raw):
    repos = []
    for repo_str in raw:
        split_repo_spec = repo_str.split('=')
        if len(split_repo_spec) != 2:
            raise ParseException("Invalid repo specification", repo_str)
        name, repo_path = split_repo_spec
        split_path = repo_path.split(':')
        if len(split_path) == 1:
            path, commit_ref = repo_path, "HEAD"
        elif len(split_path) == 2:
            path, commit_ref = split_path
        else:
            raise ParseException("Invalid repo specification", repo_str)
        repos.append({'name': name, 'path': path, 'commit_ref': commit_ref})
    return repos
