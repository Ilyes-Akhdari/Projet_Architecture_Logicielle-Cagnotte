import click
from sqlalchemy.exc import IntegrityError
from archilog.data import (
    init_database,
    create_expense,
    delete_expense,
    delete_money_pot,
    get_all_money_pots,
)
from archilog.domain import get_money_pot_details


@click.group()
def cli():
    """Archilog — interface en ligne de commande."""
    pass


@cli.command("init-db")
def init_db_command():
    """Initialise la base de données."""
    init_database()
    click.echo("Base de données initialisée avec succès.")


@cli.command("create-pot")
@click.argument("pot_name")
@click.argument("paid_by")
@click.argument("amount", type=float)
def create_pot_command(pot_name, paid_by, amount):
    """Crée une nouvelle cagnotte avec une première dépense.

    \b
    Exemple :
        archilog create-pot "Vacances" "Alice" 50.0
    """
    try:
        create_expense(pot_name, paid_by, amount)
        click.echo(f"✓ Cagnotte '{pot_name}' créée avec une dépense de {amount}€ pour {paid_by}.")
    except IntegrityError:
        click.echo(f"✗ Erreur : {paid_by} a déjà une dépense dans '{pot_name}'.", err=True)


@cli.command("add-expense")
@click.argument("pot_name")
@click.argument("paid_by")
@click.argument("amount", type=float)
def add_expense_command(pot_name, paid_by, amount):
    """Ajoute une dépense à une cagnotte existante.

    \b
    Exemple :
        archilog add-expense "Vacances" "Bob" 30.0
    """
    try:
        create_expense(pot_name, paid_by, amount)
        click.echo(f"✓ Dépense de {amount}€ ajoutée pour {paid_by} dans '{pot_name}'.")
    except IntegrityError:
        click.echo(f"✗ Erreur : {paid_by} a déjà une dépense dans '{pot_name}'.", err=True)


@cli.command("delete-expense")
@click.argument("pot_name")
@click.argument("paid_by")
def delete_expense_command(pot_name, paid_by):
    """Supprime la dépense d'un participant dans une cagnotte.

    \b
    Exemple :
        archilog delete-expense "Vacances" "Bob"
    """
    delete_expense(pot_name, paid_by)
    click.echo(f"✓ Dépense de {paid_by} supprimée dans '{pot_name}'.")


@cli.command("delete-pot")
@click.argument("pot_name")
def delete_pot_command(pot_name):
    """Supprime définitivement une cagnotte et toutes ses dépenses.

    \b
    Exemple :
        archilog delete-pot "Vacances"
    """
    delete_money_pot(pot_name)
    click.echo(f"✓ Cagnotte '{pot_name}' supprimée.")


@cli.command("list-pots")
def list_pots_command():
    """Liste toutes les cagnottes existantes."""
    pots = get_all_money_pots()
    if not pots:
        click.echo("Aucune cagnotte trouvée.")
        return
    click.echo(f"{'Cagnotte':<30}")
    click.echo("-" * 30)
    for pot in pots:
        click.echo(f"{pot.name:<30}")


@cli.command("show-pot")
@click.argument("pot_name")
def show_pot_command(pot_name):
    """Affiche les dépenses et le bilan 'qui doit à qui' d'une cagnotte.

    \b
    Exemple :
        archilog show-pot "Vacances"
    """
    mp, transactions = get_money_pot_details(pot_name)

    if not mp.expenses:
        click.echo(f"La cagnotte '{pot_name}' est vide.")
        return

    click.echo(f"\n=== Cagnotte : {mp.name} ===")
    click.echo(f"\n{'Participant':<20} {'Montant':>10}")
    click.echo("-" * 32)
    for e in mp.expenses:
        click.echo(f"{e.paid_by:<20} {e.amount:>9.2f}€")

    total = sum(e.amount for e in mp.expenses)
    click.echo("-" * 32)
    click.echo(f"{'Total':<20} {total:>9.2f}€")
    click.echo(f"{'Moyenne':<20} {total / len(mp.expenses):>9.2f}€")

    if transactions:
        click.echo("\n=== Qui doit à qui ? ===")
        for t in transactions:
            click.echo(f"  → {t.sender} doit {t.amount:.2f}€ à {t.receiver}")
    else:
        click.echo("\n✓ Tout le monde est quitte !")
