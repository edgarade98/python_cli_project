import click
from database import SessionLocal
from models import Contact, Address, PhoneNumber

@click.group()
def cli():
    pass

@cli.command()
@click.option("--first-name", required=True)
@click.option("--last-name", required=True)
@click.option("--email", required=True)
@click.argument("contact_details", nargs=-1)
@click.option("--phone-type", default="personal", type=click.Choice(["friends", "work", "home", "family"]))

def add_contact(first_name, last_name, email, contact_details, phone_type):
    session = SessionLocal()
    contact = Contact(first_name=first_name, last_name=last_name, email=email)
    addresses, phone_numbers = [], []
    for detail in contact_details:
        if detail.endswith(','):  
            detail = detail[:-1]  
        if ';' in detail:
            address, phone_number = detail.split(';')
            addresses.append(address)
            phone_numbers.append(phone_number)
        else:
            addresses.append(detail)

    for address in addresses:
        new_address = Address(city=address, country="Kenya", contact=contact)
        contact.addresses.append(new_address)

    for phone_number in phone_numbers:
        new_phone_number = PhoneNumber(number=phone_number, type=phone_type, contact=contact)
        contact.phone_numbers.append(new_phone_number)

    session.add(contact)
    session.commit()
    session.close()
    click.echo(f"Contact : {first_name} {last_name} added.")


@cli.command()
def list_contacts():
    session = SessionLocal()
    contacts = session.query(Contact).all()
    for contact in contacts:
        print(f"{contact.first_name} {contact.last_name} ({contact.email})")
        for address in contact.addresses:
            print(f"  - {address.city}, {address.country} ")
        for phone_number in contact.phone_numbers:
            print(f"  - {phone_number.number} ({phone_number.type})")
    session.close()

@cli.command()
@click.argument("email", required=True)
def delete_contact(email):
    session = SessionLocal()
    contact = session.query(Contact).filter_by(email=email).first()
    if contact:
        session.delete(contact)
        session.commit()
        session.close()
        click.echo(f"Contact with email {email} deleted.")
    else:
        click.echo(f"No contact found with email {email}.")

@cli.command()
@click.argument("search_term", required=True)
def search_contacts(search_term):
    session = SessionLocal()
    contacts = session.query(Contact).filter(Contact.first_name.ilike(f"%{search_term}%") | Contact.last_name.ilike(f"%{search_term}%") | Contact.email.ilike(f"%{search_term}%")).all()
    for contact in contacts:
        print(f"{contact.first_name} {contact.last_name} ({contact.email})")
        for address in contact.addresses:
            print(f"  - {address.city}, {address.country}")
        for phone_number in contact.phone_numbers:
            print(f"  - {phone_number.number} ({phone_number.type})")
    session.close()

if __name__ == "__main__":
    cli()
