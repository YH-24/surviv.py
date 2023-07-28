from aiohttp import ClientResponse


class HTTPException(Exception):
    """Exception that's raised when an HTTP request operation fails.
    Attributes
    ------------
    response: :class:`aiohttp.ClientResponse`

    text: :class:`str`

    status: :class:`int`

    """

    def __init__(self, response: ClientResponse):
        self.response: response
        self.status: int = response.status
        self.text: str = response.reason
        self.message = f"{self.status}"

        if len(self.text) > 0:
            self.message += f": {self.text}"

        super().__init__()
