import click
from myblog.extensions import db
from myblog.models import Admin,Category,Post
def register_commands(app):
    @app.cli.command()
    @click.option('--drop',is_flag=True,help="Create atfer drop")
    def initdb(drop):
        if drop:
            click.confirm("this operation will delete the database,do you want to continue?",abort=True)
            db.drop_all()
            click.echo('Drop tables')
        db.create_all()
        click.echo('Initilize database')

    @app.cli.command()
    @click.option('--username',prompt=True,help="the username used to login")
    @click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help="the password used to login")
    def init(username,password):
        click.echo('initilize the database')
        db.create_all()
        admin=Admin.query.first()
        if admin is not None:
            click.echo("the administrator already exists, updating...")
            admin.username=username
            admin.set_password(password)
        else:
            click.echo("Creating the temporary adminstrator account")
            admin=Admin(
                username=username,
                blog_title='主页',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category=Category.query.first()
        if category is None:
            click.echo("Creating the default category...")
            category=Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done')

    @app.cli.command()
    @click.option('--category',default=10,help="quantity of categoies,default is 10")
    @click.option('--post',default=50,help="quantity of posts,default is 50")
    def forge(category,post):
        from myblog.fakes import fake_posts,fake_categories,fake_admin,fake_links

        db.drop_all()
        db.create_all()
        click.echo('Generating the administrator...')
        fake_admin()

        click.echo("Generating %d categories..." % category)
        fake_categories(category)

        click.echo("Generating %d posts" % post)
        fake_posts(post)



        click.echo("Generating links")
        fake_links()

        click.echo("ok")



def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,Admin=Admin,Post=Post,Category=Category)