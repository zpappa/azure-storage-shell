import argparse
import collections
from types import SimpleNamespace

from argcomplete.completers import ChoicesCompleter
from azure.storage.blob.aio import BlobServiceClient
from azss.vars import context
import os
import tabulate


def ls(*args):
    parser = argparse.ArgumentParser(description='list a directory')
    parser.add_argument('path', default=context.cwd, nargs='?')
    parser.add_argument('-l', dest="l", action="store_true")
    parser.add_argument('-a', dest="a", action="store_true")
    parser.add_argument('-t', dest="t", action="store_true")
    cmd = parser.parse_args(args)

    path = normalize_path(cmd.path)
    pparts = path.split("/")

    if len(pparts) == 2 and pparts[1] == '':
        print_active_connections(cmd)
    elif len(pparts) == 2 and pparts != '':
        print_containers(cmd)
    elif len(pparts) > 2:
        print_blobs(cmd)


def print_active_connections(cmd):
    if len(context.active_connections.keys()) == 0:
        print("No active connections, use connect to connect a storage account")
    else:
        for connection in context.active_connections.keys():
            print("/" + connection)


def print_containers(cmd):
    account_name = get_account_name(cmd.path)
    conn: BlobServiceClient = context.active_connections[account_name]
    containers = list(map(lambda x: x, conn.list_containers()))
    if cmd.l is False:
        p = " ".join(list(map(lambda c: c.name, containers)))
        print(p)
    else:
        tbl = []
        for container in containers:
            row = []
            row.append(container.name)
            if cmd.t is True:
                row.append(container.last_modified)
            if cmd.a is True:
                row.append(container.metadata)
            tbl.append(row)
        tabulateme = tabulate.tabulate(tbl)
        print(tabulateme)


def print_blobs(cmd):
    account_name = get_account_name(cmd.path)
    container_name = get_container_name(cmd.path)
    sub_dir = get_sub_dir(cmd.path)

    blobs = context.active_connections[account_name].get_container_client(container_name).list_blobs()
    blobs = list(map(lambda x: x, blobs))
    blobs_to_print = []
    directories_to_print = []

    for blob in blobs:
        blob_sub_dir = get_blob_sub_dir(blob.name)
        if blob_sub_dir == sub_dir:
            blob.name = after(blob.name, "/")
            blobs_to_print.append(blob)
        elif len(sub_dir)+1 == len(blob_sub_dir):
            directories_to_print.append(SimpleNamespace(**{"name": until("/", blob.name), "last_modified": "--", "metadata": None}))


    blobs = blobs_to_print
    blobs.extend(directories_to_print)

    if cmd.l is False:
        p = " ".join(list(map(lambda c: c.name, blobs)))
        print(p)
    else:
        tbl = []
        for blob in blobs:
            row = []
            row.append(blob.name)
            if cmd.t is True:
                row.append(blob.last_modified)
            if cmd.a is True:
                row.append(blob.metadata)
            tbl.append(row)
        tabulateme = tabulate.tabulate(tbl)
        print(tabulateme)


def get_account_name(path):
    path = str(path)
    d = path.split("/")
    if len(d) > 0 and d[1] in context.active_connections.keys():
        return d[1]
    else:
        raise NotADirectoryError("Account '{0}' doesn't exist or isn't connected".format(path))


def get_container_name(path):
    path = str(path)
    d = path.split("/")
    if len(d) > 1 and d[1] in context.active_connections.keys():
        return d[2]
    else:
        raise NotADirectoryError("Container '{0}' doesn't exist.".format(path))


def normalize_path(path):
    if str(path).endswith("/") and len(path) > 1:
        return path[0:len(path) - 1]
    else:
        return path


def get_sub_dir(path):
    path = str(path)
    d = path.split("/")
    if len(d) > 3:
        return d[3:]
    else:
        return []


def get_blob_sub_dir(path):
    d = path.split("/")
    if len(d) > 1:
        return d[0:len(d)-1]
    else:
        return []


def until(s, search):
    x = search.split(s)
    if len(x) > 0:
        return x[0]
    else:
        return None


def after(s, search):
    x = s.split(search)
    if len(x) > 1:
        return search.join(x[1:])
    else:
        return s
