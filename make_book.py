import os
import glob
import markdown
from ebooklib import epub

book = epub.EpubBook()
book.set_title('文章收藏')

# add articles
file_count = 0
toc = []
spine = ['nav']
file_list = glob.glob('*.md')
file_list.sort()
for file_name in file_list:
    file_count += 1
    # convert to html
    print(file_name)
    md_source = open(file_name, 'r').read()
    html = markdown.markdown(md_source)
    # print(html)

    # add to book
    html_name = "chap_%02d.xhtml" % file_count
    title = file_name[:-3]
    chapter = epub.EpubHtml(title=title, file_name=html_name, lang="cn")
    chapter.content = html
    book.add_item(chapter)
    toc.append(epub.Link(html_name, title, title))
    spine.append(chapter)

# add images
image_count = 0
image_dir = './static'
for file_name in os.listdir(image_dir):
    print(file_name)
    if file_name.endswith('.png'):
        image_count += 1
        image_path = os.path.join(image_dir, file_name)
        image_data = open(image_path, "rb").read()
        image = epub.EpubImage(
            uid="image_{}".format(image_count),
            file_name=image_path.strip('./'),
            media_type="image/png",
            content=image_data,
        )
        book.add_item(image)

book.toc = toc
book.spine = spine
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
epub.write_epub('文章收藏.epub', book, {})
