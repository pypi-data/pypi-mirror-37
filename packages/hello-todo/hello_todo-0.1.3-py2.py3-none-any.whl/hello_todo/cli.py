import click
import os

if __name__ == '__main__':
    from hello_todo import db
else:
    from . import db

@click.command()
def todo_lists():
    results = db.get_all_todolist()
    print("%s|%s" % ("name".center(20), "description".center(20)))
    print("%s+%s" % ("-" * 20, "-" * 20))
    for r in results:
        name = r["name"]
        desc = r["description"] or ""
        print("%s|%s" % (name.center(20), desc.center(20)))


@click.command()
@click.option("-l", "--todolist_id", help="Todo list id")
def todo_list(todolist_id):
    todolist_name = db.get_todolist(todolist_id)["name"]
    results = db.get_todos(todolist_id)
    print("** %s **" % todolist_name.upper())
    print(
        "%s|%s|%s|%s"
        % ("status".center(6), "deadline".center(25), "name".center(20), "description".center(20))
    )
    print("%s+%s+%s+%s" % ("-" * 6, "-" * 25, "-" * 20, "-" * 20))

    for r in results:
        status = "x" if r["status"] else " "
        deadline = r["deadline"]
        name = r["name"]
        description = r["description"]
        print(
            "%s|%s|%s|%s"
            % (status.center(6), deadline.center(25), name.center(20), description.center(20))
        )


@click.command()
def init_todo():
    db.init_db()
    click.echo("initialized db at %s", os.path.join(os.environ["HOME"], ".todolist.db"))


@click.command()
@click.option("-n", "--name", help="Todo list name")
@click.option("-d", "--description", default=None, help="Todo list description")
def add_todolist():
    db.add_todolist(name, description)


@click.command()
@click.option("-n", "--name", help="Todo name")
@click.option("-l", "--todolist_id", help="Todo list id")
@click.option("-x", "--deadline", default=None, help="Deadline in format YYYY-MM-dd hh:mm:ss.sss")
@click.option("-d", "--description", default=None, help="Todo description")
def add_todo(name, todolist_id, deadline, description):
    db.add_todo(name, todolist_id, description, deadline)


if __name__ == "__main__":
    todo_list()
