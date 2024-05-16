from ebooklib import epub


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = None
        self.title = None
        self.author = None
        self.publisher = None
        self.date = None

        self.parse()

    def _load_data(self, flag):
        try:
            if flag:
                with open(self.file_path, 'rb') as file:
                    self.content = file.read().decode('utf-8')
            else:
                self.content = epub.read_epub(self.file_path)
        except FileNotFoundError:
            print('File not found.')

    def parse_epub(self):
        metadata = self.content.metadata
        dc_namespace = 'http://purl.org/dc/elements/1.1/'
        self.title = metadata[dc_namespace]['title'][0][0] if 'title' in metadata[dc_namespace] else 'Unknown'
        self.author = metadata[dc_namespace]['creator'][0][0] if 'creator' in metadata[
            dc_namespace] else 'Unknown'
        self.publisher = metadata['http://purl.org/dc/elements/1.1/']['publisher'][0][0] if 'publisher' in metadata[
            'http://purl.org/dc/elements/1.1/'] else 'Unknown'
        self.date = metadata['http://purl.org/dc/elements/1.1/']['date'][0][0][:4] if 'date' in metadata[
            'http://purl.org/dc/elements/1.1/'] else 'Unknown'

    def parse_fb2(self):
        title_start = self.content.find('<book-title>') + 12
        title_end = self.content.find('</book-title>')
        self.title = self.content[title_start:title_end] if title_end != -1 else 'Unknown'

        author_first_name_start = self.content.find('<first-name>') + 12
        author_first_name_end = self.content.find('</first-name>')
        first_name = self.content[
                     author_first_name_start:author_first_name_end] if author_first_name_end != -1 else 'Unknown'

        author_last_name_start = self.content.find('<last-name>') + 11
        author_last_name_end = self.content.find('</last-name>')
        last_name = self.content[
                    author_last_name_start:author_last_name_end] if author_last_name_end != -1 else 'Unknown'

        self.author = (first_name + ' ' + last_name)

        publisher_start = self.content.find('<publisher>') + 11
        publisher_end = self.content.find('</publisher>')
        self.publisher = self.content[publisher_start:publisher_end] if publisher_end != -1 else 'Unknown'

        date_start = self.content.find('<year>', publisher_end) + 6
        date_end = self.content.find('</year>', date_start)
        self.date = self.content[date_start:date_end] if date_end != -1 else 'Unknown'

    def parse(self):
        if self.file_path.endswith('.epub'):
            self._load_data(False)
            self.parse_epub()
        elif self.file_path.endswith('.fb2'):
            self._load_data(True)
            self.parse_fb2()
        else:
            print('Unsupported file format')

    def get_info(self):
        return [self.title, self.author, self.publisher, self.date]


if __name__ == '__main__':
    file_path_fb2 = './files/avidreaders.ru__poymat-nevestu-ili-kuharka-ponevole.fb2'
    file_path_epub = './files/avidreaders.ru__master-i-margarita.epub'
    parser_fb2 = Parser(file_path_fb2)
    print(parser_fb2.get_info())
    parser_epub = Parser(file_path_epub)
    print(parser_epub.get_info())
