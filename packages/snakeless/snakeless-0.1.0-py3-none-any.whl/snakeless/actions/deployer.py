from ..helpers import snakeless_spinner, get_provider


class DeployerMixin(object):
    def deploy_functions(self, config, functions_to_deploy):
        with snakeless_spinner(
            text="Deploying functions...", spinner="dots"
        ) as spinner:
            provider_name = config["project"]["provider"]
            provider = get_provider(provider_name, config)
            for function_to_deploy in functions_to_deploy:
                spinner.text = (
                    f"Deploying the { function_to_deploy } function..."
                )
                provider.deploy_function(function_to_deploy)
            spinner.succeed("All functions were deployed!")
