"""SpecialEventsPolicy class"""


from .halo_endpoint import HaloEndpoint


class SpecialEventsPolicy(HaloEndpoint):
    """Initializing the SpecialEventsPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    """

    object_name = "special_events_policy"
    objects_name = "special_events_policies"

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

    def create(self, unimportant):
        """Not implemented for this module.  Raises exception."""
        raise NotImplementedError

    def delete(self, unimportant):
        """Not implemented for this module.  Raises exception."""
        raise NotImplementedError

    def update(self, unimportant):
        """Not implemented for this module.  Raises exception."""
        raise NotImplementedError
