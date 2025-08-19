from rich import print as rprint
import json


class CliOutput:
    # What's the role of `data` here?
    # `data` is a parameter of the __init__ method, provided when creating an instance.
    # When you create an instance of the CliOutput class,
    # `self.data` stores the value of the `data` parameter as an instance attribute.
    def __init__(self, data):
        self.data = data

    def json_format(self):
        output = {
            # "total_repositories": len([repo["full_name"] for repo in self.data]),
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

        return json.dumps(output, indent=2)

    def table_format(self):
        from prettytable import PrettyTable

        table = PrettyTable()
        table.title = "GitHub Repositories"
        table.header_style = "upper"

        if isinstance(self.data, list):
            table.field_names = ["name", "owner", "url", "visibility"]

            for repo in self.data:
                table.add_row(
                    [
                        repo.get("name"),
                        repo.get("owner", {}).get("login"),
                        repo.get("html_url"),
                        repo.get("visibility"),
                    ]
                )

            return table

    def default_format(self):
        return self.table_format()


def rich_output(message: str, format_str: str = "bold green"):
    return rprint(f"[{format_str}]{message}[/{format_str}]")
