# semantic-search-embedding-model
An API service for text embeddings designed for semantic search

This service was built for my Udemy course: MLOps and Applied AI.  The instructions below are for the sprint 2 work.

## Steps to Deploy to K8s

For help creating the K8s manifests in the `k8s/` folder, see the GKE documentation for [deploying a web app with ingress](https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer#deploying_a_web_application).

### Build, Tag, and Push the Image to GCP Artifact Registry

<em>These instructions assume you have already [created a Docker repository](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images) in GCP artifact registry.</em>

Authenticate to GCP and add the remote repository to Docker config.  Change the region to wherever you created the remote repository.
```commandline
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Build the image.
```commandline
docker build -t semantic-search-embedding-model .
```

Test the image by running it in a local container.  Make sure everything looks good; port forward if you run this from the VM and check localhost in your browser.
```commandline
docker run -p 8080:8080 semantic-search-embedding-model
```

Tag.
```commandline
docker tag semantic-search-embedding-model us-central1-docker.pkg.dev/queryable-docs-dev/queryable-docs-docker-repository/semantic-search-embedding-model
```

Push.
```commandline
docker push us-central1-docker.pkg.dev/queryable-docs-dev/queryable-docs-docker-repository/semantic-search-embedding-model
```

### Test the Deployment Locally

<em>These commands could be run from your computer or the VM that we set up for the course.</em>

Install [Minikube](https://minikube.sigs.k8s.io/docs/start/) and [kubeval](https://kubeval.instrumenta.dev/installation/) (optional).

Start Minikube.  The first time it starts, it will download Kubernetes, so give it a minute.
```commandline
minikube start
```

Make sure you see the add-ons ingress and ingress-dns enabled.  If they are not enabled automatically, you can do it:
```commandline
minikube addons enable ingress
minikube addons enable ingress-dns
```

Make sure the image pull policy in `k8s/deployment.yaml` is set to always: `imagePullPolicy: Always`.  You could ignore this setting since you built the image locally, but it will be needed for deployment later.

`cd` into the `k8s/` folder and apply the manifests:
```commandline
kubectl apply -f .
```

Check to see everything is running
```commandline
kubectl get pods -n semantic-search
kubectl get ingress -n semantic-search
```

Go to the HTTP and port specified in the ingress, e.g. `http://192.168.49.2:80`

### Deploying to GKE

<em>These instructions assume you have [created a GKE autopilot cluster](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-an-autopilot-cluster) in us-central1. You can run the commands locally or from the VM we created for this course.</em>

If you want to create the cluster from the CLI, run this command but replace the project ID:
```commandline
gcloud container --project "queryable-docs-dev" clusters create-auto "autopilot-cluster-1" --region "us-central1" --release-channel "regular" --enable-master-authorized-networks --network "projects/queryable-docs-dev/global/networks/default" --subnetwork "projects/queryable-docs-dev/regions/us-central1/subnetworks/default"
```

Get the cluster connection details from the 3 dots next to your cluster name in Cloud Console > Kubernetes Engine > Clusters.  Connect to the cluster.  Run a kubectl command to verify it is pointing to the cluster:
```commandline
kubectl get nodes
```

You should see 3 nodes, as autopilot creates one in 3 of the zones in the region you specify when you set it up.

Apply the manifests:
```commandline
cd k8s
kubectl apply -f namespace.yaml
kubectl apply -f .
```

Check the pod:
```commandline
kubectl get pods -n semantic-search
kubectl describe pods <YOUR_POD> -n semantic-search
```

Check the ingress.  As soon as the pod is running and the ingress says HEALTHY in the annotations for the NEG, you can access your API at the URL and port shown by the ingress.
```commandline
kubectl get ingress -n semantic-search
kubectl describe ingress embedding-model-ingress -n semantic-search
```

You can verify the health checks from Cloud Console > Compute Engine > Health Checks.

#### Destroying Everything

The command to remove resources from the cluster:
```commandline
kubectl delete namespaces semantic-search
```

Make sure you delete the autopilot cluster too.
