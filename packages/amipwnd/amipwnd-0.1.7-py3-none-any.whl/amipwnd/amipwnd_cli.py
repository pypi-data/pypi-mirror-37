import click
import collections
from amipwnd.amipwnd import CheckPwnd

class BreachCheck(object):
    def __init__(self, debug=False):
        self.debug = debug


pass_email = click.make_pass_decorator(BreachCheck)

@click.group()
@click.option('--debug/--no-debug')
@click.pass_context
def cli(ctx, debug):
    ctx.obj = BreachCheck(debug)

@cli.command()
@click.argument('email')
@click.option('--passwords', is_flag=True)
@pass_email
def dump(breachcheck, email, passwords):
    '''
    '''
    if email:
        account = CheckPwnd(email)
        check = account.account_check()
        data = account.account_dump(check)
        print(data)



@cli.command()
@click.argument('email')
@click.option('--report', is_flag=True)
@pass_email
def check(breachcheck, email, report):
    '''
    '''
    account = CheckPwnd(email)
    check = account.account_check()

    if check and report:
        click.echo("Account Found")
        click.echo("Generating Report")
        data = account.account_stats()

    elif check:
        click.echo("Account Found")

    else:
        click.echo("Account Not Found")
