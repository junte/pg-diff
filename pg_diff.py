import enum
import re
import sys


class DBChanges(enum.StrEnum):
    ColumnAdded = "column added"
    ColumnDeleted = "column deleted"
    ColumnChanged = "column changed"
    TableAdded = "table added"
    TableDeleted = "table deleted"
    TableChanged = "table changed"


TOC = {
    "Missing Column(s)": DBChanges.ColumnAdded,
    "Unexpected Column(s)": DBChanges.ColumnDeleted,
    "Changed Column(s)": DBChanges.ColumnChanged,
    "Missing Table(s)": DBChanges.TableAdded,
    "Unexpected Table(s)": DBChanges.TableDeleted,
    "Changed Table(s)": DBChanges.TableChanged,
}

HEADING_PATTERN = r"(\w+.\w+\(s\)):"
COLUMN_PATTERN = r"^\s{5}public.(\w+).(\w+)"
TABLE_PATTERN = r"^\s{5}(\w+)"


current_type = None
columns_changes = {}
tables_changes = {}

for line in sys.stdin.readlines():
    heading = re.match(HEADING_PATTERN, line)
    if heading:
        current_type = TOC.get(heading.group(1))
        continue

    match current_type:
        case DBChanges.ColumnAdded | DBChanges.ColumnDeleted | DBChanges.ColumnChanged:
            column_name = re.match(COLUMN_PATTERN, line)
            columns_changes.setdefault(current_type, {}).setdefault(
                column_name.group(1),
                [],
            ).append(column_name.group(2))
        case DBChanges.TableAdded | DBChanges.TableDeleted | DBChanges.TableChanged:
            table_name = re.match(TABLE_PATTERN, line)
            if table_name:
                tables_changes.setdefault(
                    current_type,
                    [],
                ).append(table_name.group(1))


sys.stdout.write("*" * 100 + "\n")
sys.stdout.write(" " * 42 + "DB changes report\n")
sys.stdout.write("*" * 100 + "\n\n")

ignore_tables = set()
for change_type, tables in tables_changes.items():
    ignore_tables.update(tables)
    sys.stdout.writelines(
        [
            "- {0} `{1}`\n".format(
                change_type.value,
                table,
            )
            for table in tables
        ],
    )

for change_type, tables in columns_changes.items():
    for table, columns in tables.items():
        if table in ignore_tables:
            continue

        sys.stdout.writelines(
            [
                "- {0} `{1}` table `{2}`\n".format(
                    change_type.value,
                    column,
                    table,
                )
                for column in columns
            ],
        )
