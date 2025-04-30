# StockPulse Client Applicatipn

This is a Dockerized application that includes a FastAPI backend, an HTML frontend, and monitoring with Prometheus and Grafana for both system resource usage and API call metrics.

## Prerequisites
- Docker and Docker Compose installed on your system.

## Setup Instructions
1. **Clone or Download the Repository**
   - Clone this repository or extract the provided archive to a directory (e.g., `client/`).
   - Tar link: https://drive.google.com/file/d/1Rq-abpy42xTU7LjsE4c97tkrPj5NAnfZ/view?usp=sharing
  
   - ```bash
     tar -xzvf model-app.tar.gz
     ```

2. **Navigate to the Project Directory**
   - if ypu're cloning the git repo
      ```bash
      cd Stock-Pulse_Client
      ```
   - if you're using the tar file
     ```bash
      cd client
      ```

4. **Run the Application**
   - Start all services using Docker Compose:
  ```bash
  docker-compose up --build
  ```
   - This will build and start the containers for the backend, frontend, Prometheus, Grafana, and Node Exporter.

5. **Access the Application**
   - **Frontend**: Open http://localhost in your browser to access the HTML interface.
   - **Backend**: The API is available at http://localhost:8000 (e.g., http://localhost:8000/docs for Swagger UI).
   - **Prometheus**: Access metrics at http://localhost:9090.
   - **Grafana**: Access dashboards at http://localhost:3000 (default login: `admin`/`admin`).
   - **Node Exporter**: Metrics available at http://localhost:9100/metrics (used by Prometheus).

6. **Using the Application**
   <img width="1552" alt="image" src="https://github.com/user-attachments/assets/66afbb45-9b99-461f-ad2a-cc633b8483db" />
   - Here, in the drop down menu, you can select your company of interest.
   - You can press the predict button, it will give 3 reponses:
        - UP: if the model predicts that stock will go up in value
        - DOWN: if the model predicts that stock will go down in value
        - Company does not exist: if you type some other company that is not in the list
        - Network Error: if there is some connection issue with the backend api call

7. **Setting Up Grafana**
   - Log in to Grafana (http://localhost:3000, default: `admin`/`admin`).
     <img width="1552" alt="image" src="https://github.com/user-attachments/assets/c08f946f-46d6-4b65-9bb0-bea2379283be" />

   - Add a Prometheus data source:
     - URL: `http://host.docker.internal:9090`
       <img width="1552" alt="image" src="https://github.com/user-attachments/assets/fb694275-80c5-426c-ab77-46896518f9d9" />

     - Save and test the connection.
       
   - Create dashboards for:
    - Import grafana-dashboard.json into the grafana dashboard after connecting with prometheus
      <img width="1552" alt="image" src="https://github.com/user-attachments/assets/c6851633-a0cd-4a70-8e31-4a4ff5f50f0d" />

      
8. **Stopping the Application**
   - Press `Ctrl+C` in the terminal to stop the containers.
   - Remove the containers:
     ```bash
     docker-compose down
     ```

## Monitoring Details
- **API Metrics**:
  - Collected from the FastAPI backend (`/metrics` endpoint).
  - Includes request counts, latency, error rates, and custom prediction latency.
- **System Metrics**:
  - Collected via Node Exporter (port 9100).
  - Includes CPU usage, memory, disk I/O, and network activity of the host system.
- Access raw metrics:
  - FastAPI: http://localhost:8000/metrics
  - Node Exporter: http://localhost:9100/metrics
  - Query in Prometheus (http://localhost:9090).

## Troubleshooting
- Ensure all ports (80, 8000, 9090, 9100, 3000) are free.
- Check container logs for errors:
  ```bash
  docker-compose logs <service_name>
  ```
  (e.g., `backend`, `frontend`, `prometheus`, `grafana`, `node-exporter`).
- Verify Node Exporter metrics in Prometheus (`node_cpu_seconds_total` should be available).

## Notes
- The `model.pth` file is included in the backend container.
- Adjust the input format in the frontend to match your model's requirements.
- For production, secure Grafana with a custom password (edit `grafana/grafana.ini`) and restrict CORS in the backend.
- System metrics reflect the host system, not individual containers.# Stock-Pulse_Client



