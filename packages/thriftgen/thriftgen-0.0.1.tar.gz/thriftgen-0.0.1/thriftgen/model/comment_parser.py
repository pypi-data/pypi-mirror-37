import re
from typing import List


JAVADOC_COMMENT = re.compile(r'\/\*\*(.*?)\*\/', re.M | re.S)


def comment_text(text: str) -> str:
    """
    Extract the text from a javadoc comment.
    :param text:
    :return:
    """
    comment_lines: List[str] = []
    m = JAVADOC_COMMENT.match(text)

    if not m:
        raise Exception("Not a javadoc sent for parsing: %s" % text)

    for line in m.group(1).strip().splitlines():
        comment_lines.append(
            re.sub(r'^[ *]+\s*', ' ', line).strip()
        )

    return "\n".join(comment_lines)

