-------------------------Setting up project structure---------------------------

1. Create repo, clone it in local
2. Create a virtual environment named 'atlas' - conda create -n atlas python=3.10
3. Activate the virtual environment - conda activate atlas
4. pip install cookiecutter
5. cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science
6. Rename src.models -> src.model
7. git add - commit - push
from root folder do pip install -e .

-------------------------Setup MLFlow on Dagshub---------------------------
8. Go to: https://dagshub.com/dashboard
9. Create > New Repo > Connect a repo > (Github) Connect > Select your repo > Connect
10. Copy experiment tracking url and code snippet. (Also try: Go To MLFlow UI)
11. pip install dagshub & mlflow

12. Run the exp notebooks
13. git add - commit - push

14. dvc init
15. create a local folder as "local_s3" (temporary work)
16. on terminal - "dvc remote add -d mylocal local_s3"

17. Add code to below files/folders inside src dir:
    - logger
    - data_ingestion.py
    - data_preprocessing.py
    - feature_engineering.py
    - model_building.py
    - model_evaluation.py
    - register_model.py
18. add file - dvc.yaml (till model evaluation.metrics)
19. add file - params.yaml
20. DVC pipeline is ready to run - dvc repro
21. Once do - dvc status
22. git add - commit - push

23. Need to add S3 as remote storage - Create IAM User(keep cred) and S3 bucket
24. pip install - dvc[s3] & awscli
25. Checking/deleting dvc remote (optional) - [dvc remote list & dvc remote remove <name>] 
26. Set aws cred - aws configure
27. Add s3 as dvc remote storage - dvc remote add -d myremote s3://<bucket-name>

28. Create new dir - flask_app | Inside that, add rest of the files and dir
29. pip install flask and run the app (dvc push - to push data to S3)

30. pip freeze > requirements.txt
31. Add .github/workflows/ci.yaml file

32. Create key token on Dagshub for auth: Go to dagshub repo > Your settings > Tokens > Generate new token
    >> Please make sure to save token <<
    >> Add this auth token to github secrets & update in CI file

33. Add dir "tests" & "scripts" for CI testing

-------------------------Docker Setup---------------------------
34. pip install pipreqs
35. cd flask_app & run "pipreqs . --force"
36. Add Dockerfile and start docker-desktop
37. Build Docker image:
    docker build -t capstone-app:latest .
38. Run Docker container:
    docker run -p 8888:5000 -e CAPSTONE_TEST=<token> -e repo_owner=<owner> -e repo_name=<repo> capstone-app:latest

-------------------------AWS Setup (ECR + EC2)---------------------------
39. Create IAM user and add permissions:
    - AmazonEC2ContainerRegistryFullAccess

40. Add GitHub secrets:
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_REGION
    AWS_ACCOUNT_ID
    ECR_REPOSITORY

41. Run CI/CD pipeline to:
    - Build Docker image
    - Push to AWS ECR

-------------------------Deployment on EC2---------------------------

42. Launch EC2 instance (Ubuntu)

43. SSH into EC2:
    ssh -i <key.pem> ubuntu@<EC2-IP>

44. Install Docker on EC2:
    sudo apt-get update -y
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    newgrp docker

45. Login to AWS ECR:
    aws ecr get-login-password --region <region> \
    | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

46. Pull Docker image:
    docker pull <ECR-IMAGE-URI>

47. Run Flask App container:
    docker run -d -p 5000:5000 --name flask-app <ECR-IMAGE-URI>

48. Access application:
    http://<EC2-IP>:5000

-------------------------Prometheus Setup---------------------------

49. Launch separate EC2 instance for Prometheus

50. Install Docker (same as above)

51. Create prometheus.yml:
    nano prometheus.yml

    Add:
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: "flask-app"
        static_configs:
          - targets: ["<FLASK-EC2-IP>:5000"]

52. Run Prometheus:
    docker run -d \
      -p 9090:9090 \
      --name prometheus \
      -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
      prom/prometheus

53. Open security group:
    - Allow port 9090 (Prometheus UI)
    - Allow Flask EC2 port 5000 from Prometheus EC2

54. Access Prometheus:
    http://<PROMETHEUS-EC2-IP>:9090

-------------------------Grafana Setup---------------------------

55. Run Grafana:
    docker run -d -p 3001:3000 --name grafana grafana/grafana

56. Open security group:
    - Allow port 3001

57. Access Grafana:
    http://<PROMETHEUS-EC2-IP>:3001

58. Login:
    Username: admin
    Password: admin

-------------------------Grafana + Prometheus Integration---------------------------

59. Add Prometheus Data Source:
    URL: http://172.17.0.1:9090

60. Save & Test → should show success

61. Create dashboard and add metrics:
    - app_request_count_total
    - model_prediction_count_total
    - app_request_latency_seconds

-------------------------Final Architecture---------------------------

GitHub → CI/CD → ECR → EC2 (Flask App)
        ↓
     Prometheus
        ↓
     Grafana Dashboard