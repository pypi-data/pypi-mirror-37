

class Config(object):
    """User-facing Interface for the Kubernetes Configuration system.
    """
    def __init__(self, kubeconf):
        self.kubeconf = kubeconf

    def current_context(self):
        """Set the current kube context.
        """
        return self.kubeconf.get_current_context()

    def use_context(self, name):
        """Switch contexts.
        """
        self.kubeconf.set_current_context(name)