import click
from snark.log import logger
from snark.client.hyper_control import HyperControlClient
import yaml
from os import walk
import pprint
from tabulate import tabulate
import json
import os

def get_all_files(path = "./"):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.append((dirpath, dirnames, filenames))
        #break
    #print(f)
    return f

@click.command()
@click.argument('name_id', default='my_experiment')
@click.option('--file', '-f', default='snark.yml', help='YAML descriptor file for uploading')
@click.pass_context
def up(ctx, file, name_id):
   """ up """
   get_all_files()
   with open(file, 'r') as stream:
       data_loaded = yaml.load(stream)
  # print(data_loaded)
   descriptor = open(file,'rb')
   print("Creating Experiments...")
   pods_dict = HyperControlClient().upload(descriptor)
   print("Starting Cluster...")

@click.command()
@click.argument('name_id', default='my_experiment')
@click.option('--file', '-f', default='snark.yml', help='YAML descriptor file for uploading')
@click.pass_context
def down(ctx, file, name_id):
   """ up """
   get_all_files()
   with open(file, 'r') as stream:
       data_loaded = yaml.load(stream)
   descriptor = open(file,'rb')
   pods_dict = HyperControlClient().down(descriptor)

@click.command()
@click.argument('name_id', default='')
@click.pass_context
def ps(ctx, name_id):
   """ up """
   if name_id == "":
        experiments = HyperControlClient().list()

        experiments = [[e['ID'][:6], e['Name'], e['State'], e['IPs'], len(e['Tasks'])]
                 for e in experiments]
        print (tabulate(experiments, headers=['ID', 'Name', 'State', 'IPs', 'Tasks']))
   else:
       exp = HyperControlClient().list_task(name_id)
       tasks = exp['Tasks']
       task_list = [[t['TaskId'][:6], t['State'], t['AssignedNode']]
                   for t in tasks]
       print (tabulate(task_list, headers=['Name', 'State', 'Node']))


@click.command()
@click.argument('name_id', default='')
@click.pass_context
def logs(ctx, name_id):
   """ up """
   if name_id == '':
       print('please provide experiment id')
       exit()

   exp = HyperControlClient().list_task(name_id)
   tasks = exp['Tasks']
   for task in tasks:
       print(str(json.loads(task['Logs'][0])['result']).replace("\\r\\n", "\n"))
