# Assignment Management Service

## Overview
Assignment management service is to create a new assignment, get the information of an assignment, get the assignments related to tag

## Steps to Run the Application

```
docker build -t assigment-management-service:v.1.0 .
docker run --restart unless-stopped -d -p 5000:5000 --name=ASSIGNMENT-MANAGEMENT-SERVICE assigment-management-service:v.1.0
```

The service will be up and running in PORT 5000

You can view the swagger documentation in <http://localhost:5000/api/doc>.

<p align="center">
  <img src="./swagger-amspng" width="500" title="Get tagged assignments">
</p>