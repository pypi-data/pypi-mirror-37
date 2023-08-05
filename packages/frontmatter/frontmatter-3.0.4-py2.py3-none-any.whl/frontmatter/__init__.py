import re
import yaml

class Frontmatter:
    _yaml_delim = r'(?:---|\+\+\+)'
    _all = r'(.*?)'
    _re_pattern = r'^\s*' + _yaml_delim + _all + _yaml_delim + r'\s*' + _all + r'$'
    _regex = re.compile(_re_pattern, re.S | re.M)

    @classmethod
    def read_file(cls, path):
        """Reads file at path and returns dict with separated frontmatter.
        See read() for more info on dict return value.
        """
        with open(path, encoding="utf-8") as file:
            file_contents = file.read()
            return cls.read(file_contents)

    @classmethod
    def read(cls, string):
        """Returns dict with separated frontmatter from string.

        Returned dict keys:
        attributes -- extracted YAML attributes in dict form.
        body -- string contents below the YAML separators
        frontmatter -- string representation of YAML
        """
        fmatter = ""
        body = ""
        result = cls._regex.search(string)

        if result:
            fmatter = result.group(1)
            body = result.group(2)
        return {
            "attributes": yaml.load(fmatter),
            "body": body,
            "frontmatter": fmatter,
        }
