import Client
import argparse, os, sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="slackscrapper")
    required = parser.add_argument_group("required named arguments")
    required.add_argument('-m', '--module', help="The name of the module you want to call", required=True)
    required.add_argument('-a', '--action', help="The name of the action you want to call", required=True)
    args = parser.parse_args()

    client = Client.Client()
    # print(client.list_actionner())

    if args.module + "Actionner" in client.list_actionner() or args.module in client.list_actionner():
        func = getattr(client, str(args.module).replace("Actionner", "").lower())
        func(action=args.action)
    else:
        print([c.replace("Actionner", "") for c in client.list_actionner()])
        err_msg = "The module '" + args.module + "' is not a valid module. Please, select one among: "
        first_line_printer = True
        for module in [c.replace("Actionner", "") for c in client.list_actionner()]:
            if not first_line_printer:
                err_msg = " "*len(err_msg)
            else:
                first_line_printer = False
            print(err_msg + module)

        sys.exit(1)
