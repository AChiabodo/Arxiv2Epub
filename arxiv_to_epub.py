import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import re
import argparse
from urllib.parse import urljoin, urlparse
import sys
from datetime import datetime
import hashlib
import mimetypes
from pathlib import Path


class ArxivToEpub:
    MATHML_VALID_ATTRS = {
        'accent', 'accentunder', 'align', 'alignmentscope', 'altimg', 
        'altimg-height', 'altimg-valign', 'altimg-width', 'bevelled', 
        'cdgroup', 'charalign', 'charspacing', 'close', 'columnalign', 
        'columnlines', 'columnspacing', 'columnspan', 'columnwidth', 
        'crossout', 'decimalpoint', 'denomalign', 'depth', 'dir', 
        'displaystyle', 'edge', 'equalcolumns', 'equalrows', 'fence', 
        'form', 'frame', 'framespacing', 'groupalign', 'height', 'href', 
        'id', 'indentalign', 'indentalignfirst', 'indentalignlast', 
        'indentshift', 'indentshiftfirst', 'indentshiftlast', 'indenttarget', 
        'infixlinebreakstyle', 'largeop', 'leftoverhang', 'length', 
        'linebreak', 'linebreakmultchar', 'linebreakstyle', 'lineleading', 
        'linethickness', 'location', 'longdivstyle', 'lquote', 'lspace', 
        'macros', 'mathbackground', 'mathcolor', 'mathsize', 'mathvariant', 
        'maxsize', 'maxwidth', 'minlabelspacing', 'minsize', 'mode', 
        'movablelimits', 'mslinethickness', 'notation', 'numalign', 'open', 
        'other', 'overflow', 'position', 'rightoverhang', 'rowalign', 
        'rowlines', 'rowspacing', 'rowspan', 'rquote', 'rspace', 
        'scriptlevel', 'scriptminsize', 'scriptsizemultiplier', 'selection', 
        'separator', 'separators', 'shift', 'side', 'stackalign', 'stretchy', 
        'style', 'subscriptshift', 'superscriptshift', 'symmetric', 'valign', 
        'width', 'xmlns', 'class'
    }

    def __init__(self, url, config=None):
        self.url = url
        self.soup = None
        self.title = "arXiv Paper"
        self.authors = []
        self.images = {}
        self.config = config or self._default_config()
        self.has_mathml = False

    @staticmethod
    def _default_config():
        return {
            'remove_abstract': False,
            'remove_figures': False,
            'max_image_width': 800,
            'timeout': 30,
            'quiet': False,
            'max_authors': 4
        }

    def log(self, message):
        if not self.config.get('quiet', False):
            print(message)

    def download_html(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            timeout = self.config.get('timeout', 30)
            response = requests.get(self.url, headers=headers, timeout=timeout)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
            return True
        except Exception as e:
            print(f"Errore durante il download: {e}")
            return False

    def download_image(self, img_url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(img_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.content
        except Exception as e:
            self.log(f"Warning: impossibile scaricare immagine {img_url}: {e}")
            return None

    def get_image_extension(self, img_url, content_type=None):
        if content_type:
            ext = mimetypes.guess_extension(content_type)
            if ext:
                return ext

        parsed = urlparse(img_url)
        path = parsed.path
        ext = Path(path).suffix
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
            return ext

        return '.png'

    def clean_html(self):
        if not self.soup:
            return None

        tags_to_remove = [
            'script', 'style', 'nav', 'header', 'footer',
            'aside', 'iframe', 'noscript'
        ]
        for tag in tags_to_remove:
            for element in self.soup.find_all(tag):
                element.decompose()

        classes_to_remove = [
            'navigation', 'nav-bar', 'menu', 'sidebar',
            'header', 'footer', 'ads', 'advertisement',
            'social-share', 'comments', 'cookie-notice'
        ]
        for class_name in classes_to_remove:
            for element in self.soup.find_all(class_=re.compile(class_name, re.I)):
                element.decompose()

        ids_to_remove = ['header', 'footer', 'nav', 'navigation', 'sidebar']
        for id_name in ids_to_remove:
            for element in self.soup.find_all(id=re.compile(id_name, re.I)):
                element.decompose()

        if self.config.get('remove_abstract', False):
            self._remove_abstract()

        if self.config.get('remove_figures', False):
            self._remove_figures()

        return self.soup

    def _remove_abstract(self):
        abstract_selectors = [
            {'name': 'section', 'class_': re.compile('abstract', re.I)},
            {'name': 'div', 'class_': re.compile('abstract', re.I)},
            {'id': re.compile('abstract', re.I)}
        ]

        for selector in abstract_selectors:
            for element in self.soup.find_all(**selector):
                element.decompose()

        for heading in self.soup.find_all(['h1', 'h2', 'h3'], 
                                          string=re.compile(r'^abstract$', re.I)):
            parent = heading.find_parent(['section', 'div'])
            if parent:
                parent.decompose()
            else:
                heading.decompose()

    def _remove_figures(self):
        for figure in self.soup.find_all('figure'):
            figure.decompose()

        for element in self.soup.find_all(class_=re.compile('figure', re.I)):
            element.decompose()

    def _clean_mathml_attributes(self, math_elem):
        attrs_to_remove = []
        for attr in math_elem.attrs:
            if attr not in self.MATHML_VALID_ATTRS and not attr.startswith('aria-'):
                attrs_to_remove.append(attr)

        for attr in attrs_to_remove:
            del math_elem[attr]

        for child in math_elem.find_all():
            child_attrs_to_remove = []
            for attr in child.attrs:
                if attr not in self.MATHML_VALID_ATTRS and not attr.startswith('aria-'):
                    child_attrs_to_remove.append(attr)

            for attr in child_attrs_to_remove:
                del child[attr]

    def fix_math_elements(self, content):
        content = self.soup.find('body') if self.soup else content
        if not content:
            return content

        for math_elem in content.find_all('math'):
            self.has_mathml = True

            if not math_elem.get('xmlns'):
                math_elem['xmlns'] = 'http://www.w3.org/1998/Math/MathML'

            self._clean_mathml_attributes(math_elem)

        return content

    def _clean_author_name(self, author):
        author = re.sub(r'[^\w\s\-.,]', '', author)
        author = re.sub(r'\s+', ' ', author)
        return author.strip()

    def extract_metadata(self):
        if not self.soup:
            return

        title_tag = self.soup.find('h1')
        if title_tag:
            self.title = title_tag.get_text(strip=True)
        else:
            title_tag = self.soup.find('title')
            if title_tag:
                self.title = title_tag.get_text(strip=True)

        author_patterns = [
            {'name': 'meta', 'attrs': {'name': 'citation_author'}},
            {'name': 'meta', 'attrs': {'name': 'author'}},
        ]

        for pattern in author_patterns:
            for meta in self.soup.find_all(**pattern):
                content = meta.get('content', '').strip()
                if content and content not in self.authors:
                    cleaned = self._clean_author_name(content)
                    if cleaned and len(cleaned) < 100:
                        self.authors.append(cleaned)

        if not self.authors:
            for elem in self.soup.find_all(class_=re.compile('author', re.I)):
                author_text = elem.get_text(strip=True)
                if author_text and author_text not in self.authors:
                    cleaned = self._clean_author_name(author_text)
                    if cleaned and len(cleaned) < 100:
                        self.authors.append(cleaned)

    def process_images(self, main_content):
        if not main_content:
            return main_content

        img_counter = 1
        max_width = self.config.get('max_image_width', 800)

        for img in main_content.find_all('img'):
            src = img.get('src', '')

            if src.startswith('data:'):
                continue

            if not src.startswith(('http://', 'https://')):
                src = urljoin(self.url + "/", src)

            if src in self.images:
                img['src'] = self.images[src]['local_path']
                continue

            img_data = self.download_image(src)
            if img_data:
                img_hash = hashlib.md5(src.encode()).hexdigest()[:8]
                ext = self.get_image_extension(src)
                local_name = f"images/img_{img_counter}_{img_hash}{ext}"

                self.images[src] = {
                    'local_path': local_name,
                    'data': img_data,
                    'original_url': src
                }

                img['src'] = local_name

                if max_width:
                    img['style'] = f'max-width: {max_width}px; height: auto;'

                img_counter += 1
            else:
                img.decompose()

        return main_content

    def extract_main_content(self):
        if not self.soup:
            return None

        content_selectors = [
            {'id': re.compile('content|main|article|paper', re.I)},
            {'class_': re.compile('content|main|article|paper', re.I)},
            {'name': 'article'},
            {'name': 'main'}
        ]

        main_content = None
        for selector in content_selectors:
            main_content = self.soup.find(**selector)
            if main_content:
                break

        if not main_content:
            main_content = self.soup.find('body')

        if not main_content:
            main_content = self.soup

        main_content = self.fix_math_elements(main_content)
        main_content = self.process_images(main_content)

        return str(main_content)

    def create_epub(self, output_filename=None):
        if not self.soup:
            print("Errore: nessun contenuto da convertire")
            return False

        self.extract_metadata()

        book = epub.EpubBook()

        book.set_identifier(f'arxiv_{datetime.now().strftime("%Y%m%d%H%M%S")}')
        book.set_title(self.title)
        book.set_language('en')

        max_authors = self.config.get('max_authors', 4)
        if self.authors:
            authors_to_add = self.authors[:max_authors]
            for author in authors_to_add:
                book.add_author(author, uid='author')
                break
        else:
            book.add_author('Unknown')

        content_html = self.extract_main_content()
        if not content_html:
            print("Errore: impossibile estrarre il contenuto")
            return False

        chapter = epub.EpubHtml(
            title=self.title,
            file_name='content.xhtml',
            lang='en'
        )

        if self.has_mathml:
            chapter.properties.append('mathml')

        html_content = f"""<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:m="http://www.w3.org/1998/Math/MathML">
<head>
    <title>{self.title}</title>
    <link rel="stylesheet" href="style/nav.css" type="text/css"/>
</head>
<body>
    {content_html}
</body>
</html>"""

        chapter.content = html_content
        book.add_item(chapter)

        for img_info in self.images.values():
            img_item = epub.EpubItem(
                file_name=img_info['local_path'],
                media_type=self.get_mime_type(img_info['local_path']),
                content=img_info['data']
            )
            book.add_item(img_item)

        book.toc = (epub.Link('content.xhtml', self.title, 'content'),)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        style = """@namespace epub "http://www.idpf.org/2007/ops";
@namespace m "http://www.w3.org/1998/Math/MathML";

body {
    font-family: Georgia, "Times New Roman", serif;
    margin: 5%;
    line-height: 1.6;
}
h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #333;
}
h1 { font-size: 2em; }
h2 { font-size: 1.6em; }
h3 { font-size: 1.3em; }
p {
    text-align: justify;
    margin: 0.8em 0;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1.5em 0;
    font-size: 0.9em;
}
th, td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
}
th {
    background-color: #f2f2f2;
    font-weight: bold;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
code, pre {
    font-family: "Courier New", monospace;
    background-color: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
}
pre {
    padding: 15px;
    overflow-x: auto;
}
m|math {
    display: inline-block;
}"""

        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style
        )
        book.add_item(nav_css)

        book.spine = ['nav', chapter]

        if not output_filename:
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', self.title)
            safe_title = safe_title[:100].strip()
            output_filename = f"{safe_title}.epub"

        try:
            epub.write_epub(output_filename, book)
            self.log(f"EPUB creato con successo: {output_filename}")
            if self.images:
                self.log(f"  Immagini incluse: {len(self.images)}")
            if self.has_mathml:
                self.log(f"  Contenuto MathML rilevato e dichiarato")
            return True
        except Exception as e:
            print(f"Errore durante la creazione dell\'EPUB: {e}")
            return False

    @staticmethod
    def get_mime_type(filename):
        ext = Path(filename).suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.webp': 'image/webp'
        }
        return mime_types.get(ext, 'application/octet-stream')


def main():
    parser = argparse.ArgumentParser(
        description='Scarica e converte paper arXiv HTML in formato EPUB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  %(prog)s https://ar5iv.labs.arxiv.org/html/2401.12345
  %(prog)s https://ar5iv.labs.arxiv.org/html/2401.12345 -o paper.epub
  %(prog)s https://ar5iv.labs.arxiv.org/html/2401.12345 --no-abstract --max-authors 3
  %(prog)s https://ar5iv.labs.arxiv.org/html/2401.12345 --remove-figures --quiet
        """
    )
    parser.add_argument('url', help='URL del paper arXiv in formato HTML')
    parser.add_argument('-o', '--output', help='Nome del file EPUB di output', default=None)
    parser.add_argument('--no-abstract', action='store_true', 
                       help="Rimuovi l\'abstract dal documento")
    parser.add_argument('--remove-figures', action='store_true', 
                       help='Rimuovi tutte le figure dal documento')
    parser.add_argument('--max-image-width', type=int, default=800,
                       help='Larghezza massima delle immagini in pixel (default: 800)')
    parser.add_argument('--max-authors', type=int, default=4,
                       help='Numero massimo di autori da includere nei metadata (default: 4)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout per il download in secondi (default: 30)')
    parser.add_argument('--quiet', action='store_true',
                       help='Modalita silenziosa, mostra solo errori')

    args = parser.parse_args()

    config = {
        'remove_abstract': args.no_abstract,
        'remove_figures': args.remove_figures,
        'max_image_width': args.max_image_width,
        'timeout': args.timeout,
        'quiet': args.quiet,
        'max_authors': args.max_authors
    }

    if not config['quiet']:
        print(f"Download della pagina da: {args.url}")

    converter = ArxivToEpub(args.url, config)

    if not converter.download_html():
        sys.exit(1)

    if not config['quiet']:
        print("Pulizia del contenuto HTML...")
    converter.clean_html()

    if not config['quiet']:
        print("Creazione dell\'EPUB...")

    if converter.create_epub(args.output):
        if not config['quiet']:
            print("\n✓ Conversione completata con successo!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
