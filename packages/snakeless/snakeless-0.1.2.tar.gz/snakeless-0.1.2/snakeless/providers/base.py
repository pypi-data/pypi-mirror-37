import fs


class BaseProvider(object):
    def __init__(self, config):
        raise NotImplemented

    def get_func_data(self, func_name, func_data_key, default=None):
        return self.config["functions"][func_name].get(func_data_key, default)

    def get_project_data(self, data_key):
        return self.config["project"][data_key]

    def get_func_or_project_data(self, func_name, func_data_key, default=None):
        return self.get_func_data(
            func_name, func_data_key, default
        ) or self.get_project_data(func_data_key)

    def get_env_variables(self, func_name):
        should_merge_env = self.get_func_data(func_name, "merge_env", False)

        project_env_file = self.get_project_data("env_file_path")
        if project_env_file:
            project_env = self.parse_env_file(project_env_file)
        else:
            project_env = {}

        func_env_file = self.get_func_data(func_name, "env_file_path")
        if func_env_file:
            func_env = self.parse_env_file(func_env_file)
        else:
            func_env = {}

        resulting_env = {}

        if func_env and should_merge_env:
            resulting_env.update({**project_env, **func_env})
        elif func_env:
            resulting_env = func_env
        else:
            resulting_env = project_env

        return resulting_env

    def parse_env_file(self, env_file_path):
        env_variables = {}
        with fs.open_fs(".") as root_fs:
            with root_fs.open(env_file_path) as env_file:
                env_variables = {
                    key: value
                    for key, value in (
                        line.strip().split("=", maxsplit=2)
                        for line in env_file
                    )
                }
                return env_variables

    def deploy_function(self, func_name, spinner):
        raise NotImplemented
