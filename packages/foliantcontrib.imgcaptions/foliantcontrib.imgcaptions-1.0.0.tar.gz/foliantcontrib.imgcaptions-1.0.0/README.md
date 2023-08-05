# ImgCaptions

ImgCaptions is a preprocessor that generates visible captions for the images from alternative text descriptions of the images. The preprocessor is useful in projects built with MkDocs or another backend that provides HTML output.

## Installation

```bash
$ pip install foliantcontrib.imgcaptions
```

## Usage

To enable the preprocessor, add `imgcaptions` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - imgcaptions
```

The preprocessor supports the following options:

```yaml
    - imgcaptions:
        stylesheet_path: !path imgcaptions.css
        targets:
            - pre
            - mkdocs
            - site
            - ghp
```

`stylesheet_path`
:   Path to the CSS stylesheet file. This stylesheet should define rules for the `.image_caption` class. Default path is `imgcaptions.css`. If stylesheet file does not exist, default built-in stylesheet will be used.

`targets`
:   Allowed targets for the preprocessor. If not specified (by default), the preprocessor applies to all targets.

Image definition example:

```markdown
(leading exclamation mark here)[My Picture](picture.png)
```

This Markdown source will be finally transformed into the HTML code:

```html
<p><img alt="My Picture" src="picture.png"></p>
<p class="image_caption">My Picture</p>
```

(Note that ImgCaptions preprocessor does not convert Markdown syntax into HTML; it only inserts HTML tags `<p class="image_caption">My Picture</p>` into Markdown code after the image definitions. Empty alternative text descriptions are ignored.)
