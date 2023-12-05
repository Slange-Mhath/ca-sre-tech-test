# Citizens Advice SRE Technical Assessment

## Assessment Overview

This assessment is designed for junior to mid-level Site Reliability Engineer candidates coming from a development background.

You have been provided a Python application that is using the `cdk8s-plus-26` framework. This generates a kubernetes manifest for a very simple web application that is currently in a non-working state. You are to deploy it into a local minikube cluster, fix the issues, and then complete as many additional tasks as you can. Please read the instructions completely before proceeding with the assessment. We would prefer you do not use any AI assistance to complete this assessment, but if you do please state when and why.

You have been provided links to documentation and guides that will help you complete the tasks.

If you have any questions about the assessment, please feel free to ask your interviewer. Asking questions is part of learning!

You aren't expected to be able to fix every issue and solve every task, just learn as much as you can while making notes so you can feed back your thoughts to us. We want you to demonstrate your ability to:

- Learn new skills
- Problem solve
- Understand new codebases
- Work with Python and Kubernetes
- Ask and answer questions about your work in a follow-up session

## Lets Get Started

1. Fork this repository to your own Github account
2. Read the contents of the repository to gain an understanding of what the code is doing
3. Configure your Python development environment and install the requirements
4. Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
5. [Install and start](https://minikube.sigs.k8s.io/docs/start/) a local Kubernetes cluster with Minikube. You will need to have [Docker](https://docs.docker.com/get-docker/) installed to do this
6. Run the `main.py` file to generate the Kubernetes manifest, it will be found in at `dist/tech-test.k8s.yaml`
7. Deploy the manifest to your Minikube cluster. You can do this by running `kubectl apply -f dist/ca-tech-test.k8s.yaml`
8. The application will now be deployed to the minikube cluster. You can check the status of the deployment with `kubectl describe deployment tech-test-deployment`
9. You will see that the application has not been deployed successfully. Debug the application, fix the errors and repeat steps 7 to 9 until the application deploys successfully
10. Complete as many of the additional tasks as you can

## Additional tasks

1. The code is currently uncommented, can you add small comments to describe each kubernetes component? Can you explain what the code between lines 8 and 11 does?
2. The deployment uses the default cdk8s replica count of `2`, can you increase this to `5`?
3. There is currently no liveness probes set up for the container, can you add one?
4. The kubernetes components are all in one file. As the application grows in complexity this will become unmanagable. Can you reorganise the project?

## Links

- [Docker installation guide](https://docs.docker.com/get-docker/)
- [Minikube getting started guide](https://minikube.sigs.k8s.io/docs/start/)
- [Accessing apps in Minikube](https://minikube.sigs.k8s.io/docs/handbook/accessing/)
- [Kubectl installation guide](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [Kubectl command reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)
- [What is cdk8s?](https://cdk8s.io/docs/latest/)
- [cdk8s-plus-26 Python API reference](https://cdk8s.io/docs/latest/reference/cdk8s-plus-26/python/)
- [Kubernetes deployment documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes probes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

## Tips

- To access the deployed application from the browser, you can run `minikube service <service name>` to expose the service
- If you have already connected to clusters with kubectl, you may need to switch the context with `kubectl config use-context minikube`

## Solution

1. To test the solution run the `main.py` file and generate the separated Kubernetes manifests, which will be found in `dist/`.
2. To deploy the manifests to the kubernetes cluster simply run `kubectl apply -f dist`.
3. Running `minikube service tech-test-service` should now expose the service so that the application can be accessed from the browser.
