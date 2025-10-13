# Task Manager App

A full-stack **Task Manager** application built with **React** (frontend), **Flask** (backend), and **PostgreSQL** (database). The app is containerized using **Docker Compose** for easy local deployment. CI/CD automation is included using **GitHub Actions**.

---

## Project Overview

The Task Manager allows users to **create, view, and delete tasks**.  
- Frontend built with **React**  
- Backend built with **Flask**  
- Data stored in **PostgreSQL**  

The app is fully containerized using **Docker Compose**.

---

## Features

- Add new tasks with title and status  
- View all tasks  
- Delete tasks  
- Persistent storage with PostgreSQL  
- Containerized with Docker  
- CI/CD integration using GitHub Actions  

---

## Tech Stack

- **Frontend:** React, Axios  
- **Backend:** Flask, SQLAlchemy, Gunicorn  
- **Database:** PostgreSQL  
- **Containerization:** Docker, Docker Compose  
- **CI/CD:** GitHub Actions  

---

## Folder Structure
task-manager/
├── backend/ # Flask backend code
├── frontend/ # React frontend code
├── .env # Environment variables
├── docker-compose.yaml # Docker Compose setup
├── .github/workflows/ci-cd.yaml # GitHub Actions workflows
├── screenshots/ # Application Screenshots
│ ├── add_task.png
│ ├── view_tasks.png
│ └── delete_task.png
└── README.md

## Setup & Deployment

### Prerequisites

- Docker and Docker Compose installed
  
- Node.js installed (optional if running frontend locally without Docker)

### Steps

1. Clone the repository:

git clone <your-repo-url>

cd task-manager

Copy .env.example to .env and update environment variables:


Copy code
cp .env.example .env

Start all services using Docker Compose:


Copy code

docker-compose up --build

Open your browser:

Frontend: http://localhost:3000

Backend API: http://localhost:5000/tasks

Frontend (.env):

REACT_APP_API_URL=http://localhost:5000/tasks


Make sure the frontend URL points to the backend API URL to avoid 404 errors.

CI/CD

GitHub Actions is configured to:

Build Docker images for frontend and backend

Push images to Docker Hub

Optionally deploy to a server or cloud instance

Usage

Open the frontend in your browser (http://localhost:3000)

Add a new task in the input box and click Add Task

View all tasks in the list

Delete a task using the ❌ button



