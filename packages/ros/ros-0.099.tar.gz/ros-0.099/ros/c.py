
import json
import os
import requests
import logging
import logging.config
import sys
import time
import yaml
from types import SimpleNamespace
from jsonpath_rw import jsonpath, parse
from ros.router import Router
from ros.workflow import Workflow
from ros.lib.ndex import NDEx
from ros.tasks import exec_operator
from ros.util import JSONKit
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logger = logging.getLogger("runner")
logger.setLevel(logging.WARNING)

def execute_remote (workflow="mq2.ros", host="localhost", port=8080, args={}, library_path=["."]):
    """ Execute the workflow remotely via a web API. """
    logger.debug (f"execute remote: {workflow} libpath: {library_path} port: {port} host: {host} args: {args}")
    workflow = Workflow (
        spec=workflow,
        inputs=args,
        libpath=library_path)
    return requests.post (
        url = f"{host}:{port}/api/executeWorkflow",
        json = {
            "workflow" : workflow.spec,
            "args"     : args
        }).json ()


workflow = 'workflows/workflow_one.ros'
libpath = [ 'workflows' ]
args = {
    "disease_name" : "type 2 diabetes mellitus",
}
response = execute_remote (workflow=workflow,
                           port=5002,
                           host="http://localhost",
                           args = args,
                           library_path = libpath)
workflow = Workflow (
    spec=workflow,
    inputs=args,
    libpath=libpath)

print (json.dumps (response, indent=2))

for r in response:
    nx = workflow.graph_tools.to_nx (r)
    for n in nx.nodes (data=True):
        print (n)
