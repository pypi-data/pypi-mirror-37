"""LidsPolicy class"""


from .halo_endpoint import HaloEndpoint


class LidsPolicy(HaloEndpoint):
    """Initializing the LidsPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    """

    object_name = "lids_policy"
    objects_name = "lids_policies"

    @classmethod
    def endpoint(cls):
        """Return endpoint for API requests"""
        return "/v1/%s" % cls.objects_name

    @classmethod
    def pagination_key(cls):
        """Return the pagination key for parsing paged results"""
        return cls.objects_name

    @classmethod
    def object_key(cls):
        """Defines the key used to pull the object from the json document"""
        return cls.object_name
