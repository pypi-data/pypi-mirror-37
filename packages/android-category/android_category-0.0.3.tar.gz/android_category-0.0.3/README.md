# android_category

Tool to retrieve the category of an app given a url to the source code (git/local).

## Install

```
pip install android-category
```

## Usage

### As a library


```
from android_category import android_category

repo = "https://github.com/ccrama/Slide/"
category = android_category.get_app_category_from_repo_git()
print(category)
```

Should output:

```
NEWS_AND_MAGAZINES
```

### CLI

We can also run the tool in the command line:

```
android_category https://github.com/ccrama/Slide/
```

Should output:

```
NEWS_AND_MAGAZINES
```

Get more options by running:

```
android_category --help
```

