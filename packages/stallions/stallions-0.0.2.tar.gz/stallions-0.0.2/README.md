# Stallion
Parsing any web page context.

## Use
```
from stallions import extract
url = "https://www.rtbasia.com/"
article = extract(url=url)
print("title", article.title)
print("h1", article.h1)
print("meta_keywords", article.meta_keywords)
print("meta_description", article.meta_description)
print(article.content)
```

## Version
- v-0.0.1 Static web page download.

Galen _@20180510_