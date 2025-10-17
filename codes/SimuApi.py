class SimuApi:
    def do_action(self, data):
        if isinstance(data, dict):
            if 'id' in data:
                return {'result': data.get('value', None)}
            return {'result': None}
        elif isinstance(data, list):
            return [self.do_action(x) for x in data]
        else:
            return None

    def get(self, *args, **kwargs):
        return 'ok'
