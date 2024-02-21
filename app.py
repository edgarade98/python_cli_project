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
def add_contact(first_name, last_name, email, contact_details):
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
        new_phone_number = PhoneNumber(number=phone_number, type="personal", contact=contact)
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
