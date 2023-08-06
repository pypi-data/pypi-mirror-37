import json

try:
    from importlib.resources import read_text
except ImportError:
    from importlib_resources import read_text


class HanziLevel:
    data = json.loads(read_text('hanzilvlib', 'level.json'))

    def get_level(self, hanzi):
        for i, hanzi_list in enumerate(self.data['levels']):
            if hanzi in hanzi_list:
                return i + 1

    def get_label(self, hanzi):
        for v in self.data['labels']:
            start, end, label = v
            if hanzi in range(start, end + 1):
                return label

    def get_hanzi_list(self, level):
        return self.data['levels'][level - 1]
