class BaseAgent:
    def invoke(self, state: dict):
        raise NotImplementedError("Agent must implement invoke")
