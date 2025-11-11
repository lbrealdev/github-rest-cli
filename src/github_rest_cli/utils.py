from rich import print as rprint
import json


class CliFormatOutput:
    def to_json(self, data):
        return json.dumps(data, indent=2)

    def to_table(self, fields, data):
        from prettytable import PrettyTable

        table = PrettyTable()
        table.title = "GitHub Repositories"
        table.header_style = "upper"

        if isinstance(fields, list):
            table.field_names = fields

            # Align all columns to left.
            table.align = "l"

        if isinstance(data, list):
            for row in data:
                table.add_row(row)

        return table


class CliOutput:
    # What's the role of `data` here?
    # `data` is a parameter of the __init__ method, provided when creating an instance.
    # When you create an instance of the CliOutput class,
    # `self.data` stores the value of the `data` parameter as an instance attribute.
    def __init__(self, data):
        self.data = data
        self.formatter = CliFormatOutput()

    def json_format(self):
        repos = {
            "repositories": [
                {
                    "name": f.get("name"),
                    "owner": f.get("owner", {}).get("login"),
                    "url": f.get("html_url"),
                    "visibility": f.get("visibility"),
                }
                for f in self.data
            ],
        }
        return self.formatter.to_json(repos)

    def table_format(self):
        fields = ["name", "owner", "url", "visibility"]
        values = []
        for repo in self.data:
            values.append(
                [
                    repo.get("name"),
                    repo.get("owner", {}).get("login"),
                    repo.get("html_url"),
                    repo.get("visibility"),
                ]
            )

        return self.formatter.to_table(fields, values)

    def get_json_output(self):
        return self.formatter.to_json(self.data)

    def default_format(self):
        return self.table_format()


def rich_output(message: str, format_str: str = "bold green"):
    return rprint(f"[{format_str}]{message}[/{format_str}]")
