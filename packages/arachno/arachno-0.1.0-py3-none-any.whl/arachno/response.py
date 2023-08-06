from html import escape
from typing import Any

import jmespath
import ujson


def ujson_loads(data):
    return ujson.loads(data)


class JSONResponse:
    def __init__(self, json, failed=False):
        self.json = json
        self.failed = failed

    @classmethod
    async def from_aiohttp(cls, response, json_only=True):
        obj = None
        failed = False

        if response.status > 400:
            failed = True
            obj = {
                "error": escape(await response.text()),
                "code": response.status
            }

        try:
            obj = await response.json(loads=ujson_loads)
        except Exception as e:
            if json_only:
                failed = True
            obj = {"text": str(e)}

        return cls(json=obj, failed=failed)

    @classmethod
    def success(cls, json):
        return cls(json)

    def resolve(self, definition: Any) -> Any:
        return jmespath.search(definition, self.json)
