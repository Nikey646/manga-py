from manga_py.provider import Provider
from .helpers.std import Std


class MangaZukiMe(Provider, Std):

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'/manga/[^/]+/.+?(\d+(?:-\d+)?)[\?/]')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        chapters = []
        n = self.http().normalize_uri
        re = self.re.compile(r'(.+?)(?:\?style=list)?(?:/)?$')
        for ch in self._elements('.wp-manga-chapter > a'):
            href = re.search(ch.get('href')).group(1)
            chapters.append(n(href) + '?style=list')
        return chapters

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.wp-manga-chapter-img')

    def get_cover(self) -> str:
        return self._cover_from_content('.summary_image > a > img', 'data-src')


main = MangaZukiMe