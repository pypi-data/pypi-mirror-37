from argparse import ArgumentParser
from tinydb import TinyDB, Query, operations
from getpass import getpass
from datetime import datetime
from cryptography.fernet import InvalidToken
from security import DefaultCryptography, StorageFormat
from storage import SecureStorage
from utils import generateKey
import os
import sys
import pyperclip

def create(args):
    format = args.storage_format.lower()
    if (format == 'json'):
        storage_format = StorageFormat.JSON
    elif (format == 'bson'):
        storage_format = StorageFormat.BSON
    else:
        storage_format = None
        print("Storage format not exists", file=sys.stderr)
        exit(-1)

    print("Creating new database in", args.file, "using",storage_format.name, "format")

    if (os.path.isfile(args.file)):
        print("Database file already exists", file=sys.stderr)
        exit(-1)
    else:
        password = getpass(prompt="Insert your master password: ")
        conf_password = getpass(prompt="Confirm your master password: ")

        if (password != conf_password):
            print("Passwords do not match", file=sys.stderr)
            exit(-1)
        else:
            try:
                SecureStorage.create(filename=args.file, password=password, storage_format=storage_format)
                print("Database created successfully")
            except Exception as err:
                print("There something wrong", file=sys.stderr)
                print(err, file=sys.stderr)
                exit(-1)

def login(database_name):
    if (not os.path.isfile(database_name)):
        print("Database not exists", file=sys.stderr)
        exit(-1)
    password = getpass(prompt="Password for " + database_name + ": ")

    try:
        db = TinyDB(args.file, password, storage=SecureStorage)
        return db
    except InvalidToken:
        print("Wrong password", file=sys.stderr)
        exit(-1)

def add(args):
    print("Adding password labeled ", args.label, " to the database in ", args.file)

    db = login(args.file)

    query = Query()
    if (len(db.search(query.label == args.label)) > 0):
        print("This label already in use")
        exit(-1)
    new_password = getpass(prompt="Insert password for " + args.label+ ": ")
    conf_password = getpass(prompt="Confirm your password: ")

    if (new_password != conf_password):
        print("Passwords don't match")
        exit(-1)
    db.insert({'label': args.label, 'password': new_password, 'created_date': datetime.now().isoformat(), 'last_access': None, 'last_update': None})

    print("Successfully")

def get(args):

    db = login(args.file)

    query = Query()
    result = db.search(query.label == args.label)
    if (len(result) == 0):
        print("This label not exists in this database")
        exit(-1)


    password_model = result[0]
    password = password_model['password']
    

    if (password_model["last_access"] != None):
        last_access = datetime.strptime(password_model["last_access"], "%Y-%m-%dT%H:%M:%S.%f")
        print("The last access was in ", last_access.strftime("%d/%m/%Y %I:%M%p"))
    else: 
        print("First access for this password")
    
    if (password_model["last_update"] != None):
        last_update = datetime.strptime(password_model["last_update"], "%Y-%m-%dT%H:%M:%S.%f")
        print("The last access was in ", last_update.strftime("%d/%m/%Y %I:%M%p"))

    if (args.to_clipboard):
        pyperclip.copy(password)
        print("Password copied to clipboard")
    else:
        print("The password for ", args.label, " is: ", password)

    db.update(operations.set("last_access", datetime.now().isoformat()), doc_ids=[password_model.doc_id])

def update(args):
    print("Updating password for ", args.label)
    db = login(args.file)

    query = Query()
    result = db.search(query.label == args.label)
    if (len(result) == 0):
        print("This label not exists in this database")
        exit(-1)

    password_model = result[0]

    new_password = getpass(prompt="Insert a new password for " + args.label+ ": ")
    conf_password = getpass(prompt="Confirm your password: ")

    if (new_password != conf_password):
        print("Passwords don't match")
        exit(-1)

    db.update({"last_update": datetime.now().isoformat(), "password": new_password}, doc_ids=[password_model.doc_id])

    print("Successfully")
    

def remove(args):
    print("Removing password for ", args.label)
    db = login(args.file)


    query = Query()
    result = db.search(query.label == args.label)
    if (len(result) == 0):
        print("This label not exists in this database")
        exit(-1)

    db.remove(doc_ids=[result[0].doc_id])
    print("Password ", args.label, " removed successfully")

def generate(args):
    print("Generating password")
    password = generateKey(length=args.length, uppers=not args.no_uppercase, lowers=not args.no_lowercase, punctuation=not args.no_punctuation, digits= not args.no_digits, except_chars=args.except_chars)
    if (args.save):
        db = login(args.file)
        query = Query()
        if (len(db.search(query.label == args.save)) > 0):
            print("This label already in use")
            exit(-1)
        db.insert({'label': args.save, 'password': password, 'created_date': datetime.now().isoformat(), 'last_access': None, 'last_update': None})
        print("Password has been saved with the label ", args.save)
    if (args.to_clipboard):
        pyperclip.copy(password)
        print("Password copied to clipboard")
    else:
        print("The generated password is: ", password)

def list_labels(args):
    print("Listing all labels")
    db = login(args.file)
    for p in db.all():
        print(p['label'])
    
# Menu 
parser = ArgumentParser()
operation_subparser = parser.add_subparsers(title="Operations", dest="operation")
operation_subparser.required = True
parser.add_argument("-f", "--file", metavar="FILE", help="Database file", default="keyring.db")

create_parser = operation_subparser.add_parser("create", help="Create database keyring")
create_parser.add_argument("-F", "--storage-format", metavar="format", default="bson", help="The storage format (JSON or BSON) [default=BSON]")
create_parser.set_defaults(func=create)

add_parser = operation_subparser.add_parser("add", help="Add a password")
add_parser.add_argument("label", help="label for the password")
add_parser.set_defaults(func=add)

get_parser = operation_subparser.add_parser("get", help="get a password")
get_parser.add_argument("label", help="label for the password")
get_parser.add_argument("-c", "--to-clipboard", action="store_true", help="Copy the password to clipboard and don't show it")
get_parser.set_defaults(func=get)

update_parser = operation_subparser.add_parser("update", help="update a password")
update_parser.add_argument("label", help="label for the password")
update_parser.set_defaults(func=update)

remove_parser = operation_subparser.add_parser("remove", help="Remove a password")
remove_parser.add_argument("label", help="label for the password to remove")
remove_parser.set_defaults(func=remove)

generate_parser = operation_subparser.add_parser("generate", help="generate a password")
generate_parser.add_argument("-l", "--length", metavar="length", type=int, default="12", help="The length for the generated password [default=12]")
generate_parser.add_argument("-u", "--no-uppercase", action="store_true", help="Don't use uppercase chars in the password")
generate_parser.add_argument("-ll", "--no-lowercase", action="store_true", help="Don't use lowercase chars in the password")
generate_parser.add_argument("-d", "--no-digits", action="store_true", help="Don't use digits in the password")
generate_parser.add_argument("-p", "--no-punctuation", action="store_true", help="Don't use punctuation chars in the password")
generate_parser.add_argument("-e", "--except-chars", metavar="except_chars", default="", help="Don't use these chars in the password")
generate_parser.add_argument("-s", "--save", metavar="label", help="Save the generate password using this label")
generate_parser.add_argument("-c", "--to-clipboard", action="store_true", help="Copy the password to clipboard and don't show it")
generate_parser.set_defaults(func=generate)

list_parser = operation_subparser.add_parser("list", help="List all password labels")
list_parser.set_defaults(func=list_labels)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)

    
