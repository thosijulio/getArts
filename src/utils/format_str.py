from typing import Literal

def format_str(string: str, type: Literal["year", "author", "title"]):
  match type:
    case 'year':
      return string.replace('circa. ', 'c. ').replace("/", "-").replace("Around ", "c. ").replace(" - ", "-").replace("ca. ", "c. ").replace("About ", "c. ").replace("?", "").replace(':', '-').replace("\n", "")
    case 'title':
      return string.replace(':', '-').replace("/", "-").replace("?", "").replace("\n", "")
    case 'author':
      return string.replace(':', '-').replace("/", "-").replace("?", "").replace("\n", "")

  return string