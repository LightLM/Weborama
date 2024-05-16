import csv
from collections import Counter


class DataAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.id_counts = Counter()

        self._load_and_analyze()

    def _load_and_analyze(self):
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            self.data = [row['id'] for row in reader]
            self.id_counts = Counter(self.data)

    def get_ids_3(self):
        return [id for id, count in self.id_counts.items() if count == 3]

    def get_ids_frequency(self):
        frequency_id = Counter(self.id_counts.values())
        return frequency_id


if __name__ == '__main__':
    analyzer = DataAnalyzer('./files/table.csv')
    print('ID, встречающиеся только 3 раза:', analyzer.get_ids_3())
    for occurrences, frequency in analyzer.get_ids_frequency().items():
        print(f'{frequency} уникальных ид встречались {occurrences} раз(а)')
