# Microservices Website (Python + Kubernetes)

## What you get
- **Web UI** (HTML/CSS/JS) served by Nginx.
- **Catalog API** (FastAPI + SQLAlchemy) for CRUD-style calls.
- **PostgreSQL** database.
- **Kubernetes manifests** for deploying all services.

## Architecture overview
- **Web service**: static HTML + JS. Nginx proxies `/api/*` to the API service.
- **API service**: FastAPI app that creates an `items` table and exposes `/items` endpoints.
- **Database**: PostgreSQL Deployment + Service.

```
Browser
  -> Web Service (Nginx)
     -> /api/* proxied to API Service
        -> PostgreSQL
```

## Folder structure
```
microservices-site/
  services/
    api/
      app/
        main.py
        db.py
        models.py
      requirements.txt
      Dockerfile
    web/
      html/
        index.html
        app.js
        styles.css
      nginx.conf
      Dockerfile
  k8s/
    namespace.yaml
    configmap.yaml
    secret.yaml
    postgres-deployment.yaml
    postgres-service.yaml
    api-deployment.yaml
    api-service.yaml
    web-deployment.yaml
    web-service.yaml
```

## How the API works (high level)
- `db.py` builds the database URL from environment variables.
- `models.py` defines the `Item` table.
- `main.py`:
  - Creates tables on startup.
  - `GET /items`: returns all items.
  - `POST /items`: adds a new item.

## How the Web UI works (high level)
- `index.html` contains the form and list.
- `app.js` calls `/api/items` to load and save items.
- Nginx proxies `/api/` to the API service, so the browser only talks to one host.

## Kubernetes steps (local dev cluster)
1) Build the images (example tags used in manifests):
   - `microservices-api:latest`
   - `microservices-web:latest`

2) Load or push images to your cluster (for example, with Minikube or a registry).

3) Apply manifests:
   - `k8s/namespace.yaml`
   - `k8s/configmap.yaml`
   - `k8s/secret.yaml`
   - `k8s/postgres-deployment.yaml`
   - `k8s/postgres-service.yaml`
   - `k8s/api-deployment.yaml`
   - `k8s/api-service.yaml`
   - `k8s/web-deployment.yaml`
   - `k8s/web-service.yaml`

4) Access the UI:
   - Use your cluster’s LoadBalancer or port-forward the `web` service.

## Notes
- The DB password in [k8s/secret.yaml](k8s/secret.yaml) is a demo value (`apppassword`) encoded in base64.
- For production, use a real secret manager, persistent volumes, and an ingress controller.
