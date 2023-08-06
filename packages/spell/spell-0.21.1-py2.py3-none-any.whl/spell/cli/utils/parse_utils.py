class ParseException(Exception):
    def __init__(self, message, token):
        super(ParseException, self).__init__(message)
        self.token = token


def parse_attached_resources(raw):
    attached_resources = {}
    for token in raw:
        schema_chunks = token.split("://")
        if len(schema_chunks) == 2:
            schema = schema_chunks[0] + "://"
            contents = schema_chunks[1]
        elif len(schema_chunks) == 1:
            schema = ""
            contents = token
        else:
            raise ParseException("Invalid attached public bucket resource value", token)
        chunks = contents.split(':')
        if len(chunks) == 1:
            resource_name, path = token, ""
        elif len(chunks) == 2:
            resource_name, path = chunks
        else:
            raise ParseException("Invalid attached resource value", token)
        attached_resources[schema + resource_name] = path
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


def parse_grid_params(raw):
    params = {}
    for param_str in raw:
        split_param_str = param_str.split('=')
        if len(split_param_str) != 2:
            raise ParseException("Invalid param specification", param_str)
        name, values = split_param_str
        split_values = values.split(',')
        if any([len(val) == 0 for val in split_values]):
            raise ParseException("Invalid param specification", param_str)
        params[name] = list(map(convert_value, split_values))
    return params


def convert_value(raw):
    """convert_value attempts to convert the input string to int and then float
    in that priority and return the result. If both conversions fails, the input string
    is returned unchanged.
    """
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw
