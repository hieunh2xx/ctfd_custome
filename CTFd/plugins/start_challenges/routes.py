from flask import Blueprint, jsonify, request
from kubernetes import client, config
from CTFd.models import Challenges, DeployedChallenge, db
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO,  # Set to INFO level
                    format='%(asctime)s - %(levelname)s - %(message)s')




start_challenge_api = Blueprint('start_challenge_api', __name__, url_prefix='/api/v1')

@start_challenge_api.route('/start_challenge/<int:challenge_id>', methods=['POST'])
def start_challenge(challenge_id):
    user_Id= request.json.get("user_id")

    #config.load_kube_config() 
    if not user_Id:
        logging.warning(f"User attempted to start challenge {challenge_id} without being logged in.")
        return jsonify({"message":"User is not logged in"}), 401
    
    challenge= Challenges.query.filter_by(id= challenge_id).first()

    if not challenge:
        logging.error(f"Challenge {challenge_id} not found when user {user_Id} attempted to start it.")
        return jsonify({"success": False, "message": "Challenge not found"}), 404
    
    #find the challenge
    deployed_challenge= DeployedChallenge.query.filter_by(challenge_id=challenge_id, user_id= user_Id ).first()

    if not deployed_challenge:
        # If not deployed, generate a new docker_image and create a new deployment
        docker_image = f"challenge_image_{challenge_id}_{user_Id}"

        deployment_name = f"challenge-{challenge_id}"

        # container = client.V1Container(
        #     name=deployment_name,
        #     image=docker_image,
        #     ports=[client.V1ContainerPort(container_port=80)],
        #     resources=client.V1ResourceRequirements(
        #         requests={"cpu": "100m", "memory": "256Mi"},
        #         limits={"cpu": "500m", "memory": "512Mi"}
        #     )
        # )

        # pod_template = client.V1PodTemplateSpec(
        #     metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
        #     spec=client.V1PodSpec(containers=[container])
        # )

        # deployment_spec = client.V1DeploymentSpec(
        #     replicas=1,
        #     selector=client.V1LabelSelector(match_labels={"app": deployment_name}),
        #     template=pod_template
        # )

        # deployment = client.V1Deployment(
        #     api_version="apps/v1",
        #     kind="Deployment",
        #     metadata=client.V1ObjectMeta(name=deployment_name),
        #     spec=deployment_spec
        # )

        # k8s_client = client.AppsV1Api()
        # k8s_client.create_namespaced_deployment(namespace="default", body=deployment)

        #add deployment to table
        # new_deployment = DeployedChallenge(
        #     challenge_id=challenge_id,
        #     image_name= docker_image,
        #     deploy_state= "Success",
        #     last_update= datetime.now(),
        #     deployment_name= deployment_name
        #     )
        #db.session.add(new_deployment)
        challenge.connection_info = f"http://{deployment_name}.ctfd.local"
        db.session.commit()

        challenge_url = f"http://{deployment_name}.ctfd.local"
        logging.info(f"User {user_Id} started challenge {challenge_id}. Deployment created: {deployment_name}.")

        return jsonify({"success": True, "message": "Challenge started", "challenge_url": challenge_url}), 200

#when users restart instance, uses existing one
    else:
        logging.info(f"User {user_Id} is using an existing deployment for challenge {challenge_id}.")
        # If already deployed, use the existing deployment
        docker_image = deployed_challenge.docker_image
        deployment_name = deployed_challenge.deployment_name

    # Fetch url dang co trong db
    challenge_url = challenge.connection_info

    return jsonify({"success": True, "message": "Challenge started", "challenge_url": challenge_url}), 200

    
    
@start_challenge_api.route('/stop_challenge/<int:challenge_id>', methods=['POST'])
def stop_challenge(challenge_id):
    # Load Kubernetes configuration
    #config.load_incluster_config()  
    
    # or config.load_kube_config() for local development

    
    user_id = request.json.get("user_id")
    deployment_name = f"challenge-{challenge_id}-{user_id}"

   
    apps_v1 = client.AppsV1Api()
    try:
        apps_v1.delete_namespaced_deployment(name=deployment_name, namespace="default", body=client.V1DeleteOptions())
        return jsonify({"success": True, "message": "Challenge stopped", "deployment_name": deployment_name}), 200
    except client.exceptions.ApiException as e:
        return jsonify({"success": False, "message": f"Error stopping challenge: {str(e)}"}), 400