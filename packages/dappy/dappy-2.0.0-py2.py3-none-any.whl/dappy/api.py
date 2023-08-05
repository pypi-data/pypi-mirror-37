from dappy.endpoint import CompleteEndpoint


# Represents an API and all of its endpoints
class API:

    def __init__(self, netloc, endpoints, scheme='https', json=True):
        for endpoint in endpoints:
            # This allows us to do things like API.endpoint.get(...)
            setattr(
                self,
                endpoint.name,
                CompleteEndpoint(
                    scheme, netloc, endpoint, json=json
                )
            )


