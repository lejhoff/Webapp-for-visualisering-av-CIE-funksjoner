# To run deployed application
1. Connect to NTNU to network.
2. Navigate to the VM's IP adress

For frontend application navigate to 10.212.136.66:80 \
For backend API navigate to 10.212.136.66:8000

# To run on local machine
1. Install Docker and docker-compose
2. Clone the repoistory
3. Navigate to root folder of the project
4. run docker-compose up --build

For running on local machine or outside the VM environment where the application is deployed, you need to update the ip adresss in 'frontend/cie-react/utils/api-urls.tsx' to match your setup. You might also need to configure ports in the docker-compose.yml in the root folder of this project.