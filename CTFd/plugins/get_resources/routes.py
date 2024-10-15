from flask import Blueprint, jsonify
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Define the API route for getting resource metrics
resource_api = Blueprint('resource_api', __name__, url_prefix='/api/v1')

#config= config.load_kube_config()
