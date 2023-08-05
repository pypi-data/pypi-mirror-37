import click
from hello_todo import db

@click.command()
def todo_lists():
    results = db.get_all_todolist()
    print('%s|%s' %('name'.center(20), 'description'.center(20)))
    print('%s+%s' %('-' * 20, '-' * 20))
    for r in results:
        name = r['name']
        desc = r['description'] or ''
        print('%s|%s' % (name.center(20), desc.center(20)))

if __name__=='__main__':
    todo_lists()
