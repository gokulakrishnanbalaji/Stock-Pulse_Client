# StockPulse

This is a Dockerized application that includes a FastAPI backend, an HTML frontend, and monitoring with Prometheus and Grafana for both system resource usage and API call metrics.

## Prerequisites
- Docker and Docker Compose installed on your system.

## Setup Instructions
1. **Clone or Download the Repository**
   - Clone this repository or extract the provided archive to a directory (e.g., `client/`).

2. **Navigate to the Project Directory**
   ```bash
   cd client
   ```

3. **Run the Application**
   - Start all services using Docker Compose:
     ```bash
     docker-compose up --build
     ```
   - This will build and start the containers for the backend, frontend, Prometheus, Grafana, and Node Exporter.

4. **Access the Application**
   - **Frontend**: Open http://localhost in your browser to access the HTML interface.
   - **Backend**: The API is available at http://localhost:8000 (e.g., http://localhost:8000/docs for Swagger UI).
   - **Prometheus**: Access metrics at http://localhost:9090.
   - **Grafana**: Access dashboards at http://localhost:3000 (default login: `admin`/`admin`).
   - **Node Exporter**: Metrics available at http://localhost:9100/metrics (used by Prometheus).

5. **Using the Application**
   - In the frontend, enter input data as a JSON array (e.g., `[1, 2, 3]`) and click "Submit" to send a POST request to the backend.
   - The backend processes the input using the `model.pth` file and returns a prediction, which is displayed on the page.

6. **Setting Up Grafana**
   - Log in to Grafana (http://localhost:3000, default: `admin`/`admin`).
   - Add a Prometheus data source:
     - URL: `http://prometheus:9090`
     - Save and test the connection.
   - Create dashboards for:
     - **API Metrics**:
       - Import dashboard ID `4701` (FastAPI/Starlette) for API call metrics (e.g., request count, latency, errors).
       - Alternatively, create a custom dashboard using metrics like:
         - `http_requests_total` (total requests by endpoint/status).
         - `http_request_duration_seconds` (request latency).
         - `prediction_latency_seconds` (custom prediction latency).
     - **System Metrics**:
       - Import dashboard ID `1860` (Node Exporter Full) for system resource usage (CPU, memory, disk, network).
       - Key metrics include:
         - `node_cpu_seconds_total` (CPU usage).
         - `node_memory_MemAvailable_bytes` (available memory).
         - `node_disk_io_time_seconds_total` (disk I/O).
   - Save dashboards for reuse.

7. **Stopping the Application**
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
