import json
import os


class Parse():
    response = {}

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def open_json(self, path):
        with open(path, 'rb') as file:
            result = json.load(file)
        return result

    def run_sript(self):
        value = self.open_json(self.file1)
        test = self.open_json(self.file2)
        self.parse_json(value, False)
        self.parse_json(test, True)
        report_json = json.dumps(test, indent=4)
        return report_json

    def parse_json(self, test, write=False):
        if isinstance(test, dict):
            for item in test:
                if isinstance(test.get(item), list):
                    for x in test.get(item):
                        if not write:
                            self.change_value(x)
                            if x.get('values'):
                                self.parse_json(x['values'], write)
                        elif write:
                            self.write_json(x)
                            if x.get('values'):
                                self.parse_json(x['values'], write)
        elif isinstance(test, list):
            for i in test:
                if not write:
                    self.change_value(i)
                elif write:
                    self.write_json(i)
                self.parse_json(i, write)

    def change_value(self, dct):
        id = dct.get('id')
        value = dct.get('value')
        self.response[id] = value

    def write_json(self, dct):
        dct['value'] = self.response.get(dct['id'])


if __name__ == '__main__':
    task = Parse('values.json', 'tests.json')
    report = task.run_sript()
    with open(f'{os.getcwd()}/report.json', 'w') as f:
        f.write(report)
