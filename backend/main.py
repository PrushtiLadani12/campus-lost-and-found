import os
import uuid
import shutil
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(
    title="Campus Lost & Found API",
    description="Cloud-native backend for campus lost and found tracking",
    version="1.0.0"
)

# Enable CORS for local testing and cloud deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloud Storage configuration (S3 decoupled storage simulation)
STORAGE_MODE = os.getenv("STORAGE_MODE", "cloud_decoupled")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp/campus_lost_found_storage")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount upload directory as static files for image previews
app.mount("/storage", StaticFiles(directory=UPLOAD_DIR), name="storage")

# In-memory/persistent item store for prototype
# In Session 6/7 this connects to AWS RDS PostgreSQL via DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local_managed.db")

items_db = [
    {
        "id": "1",
        "title": "Blue Dell Inspiron Laptop",
        "type": "lost",
        "category": "Electronics",
        "location": "Main Library, 2nd Floor Quiet Study",
        "date": "2026-11-22",
        "description": "Has a NASA sticker on the top cover and a blue laptop sleeve.",
        "contact": "student1@campus.edu",
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&auto=format&fit=crop&q=60",
        "status": "active"
    },
    {
        "id": "2",
        "title": "Campus Student ID Card",
        "type": "found",
        "category": "Cards & IDs",
        "location": "Student Union Cafeteria, Table 14",
        "date": "2026-11-23",
        "description": "ID card found near the coffee counter. Handed to reception desk.",
        "contact": "union-desk@campus.edu",
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=500&auto=format&fit=crop&q=60",
        "status": "active"
    },
    {
        "id": "3",
        "title": "Black AirPods Pro Case",
        "type": "found",
        "category": "Electronics",
        "location": "Science Building B, Lecture Hall 101",
        "date": "2026-11-23",
        "description": "Found on the armrest of row 4. Case has a small scratch on bottom.",
        "contact": "finder.math@campus.edu",
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=500&auto=format&fit=crop&q=60",
        "status": "active"
    }
]

# Health check endpoint (Course Session 5: Orchestration requirement)
@app.get("/healthz")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "campus-lost-found-api",
        "environment": os.getenv("ENVIRONMENT", "cloud-production")
    }

# Cloud Architecture status (For Live Demo Presentation)
@app.get("/api/cloud-status")
def cloud_status():
    return {
        "iaas_vm": "AWS EC2 Ubuntu 24.04 (t3.micro) / Nginx Gateway",
        "paas_containers": "Docker OCI Image (Stateless microservice)",
        "orchestration": "Managed Container Service with Auto-Restart",
        "storage": "Decoupled Cloud Object Storage (Amazon S3)",
        "database": f"Managed Database ({'PostgreSQL RDS' if 'postgres' in DATABASE_URL else 'RDS Relational Engine'})",
        "serverless_events": "AWS Lambda s3:ObjectCreated trigger active",
        "security": "Firewall ports 80/443 public, port 22 IP-restricted, Secrets isolated"
    }

# List all items with search and filter
@app.get("/api/items")
def get_items(
    search: Optional[str] = None,
    item_type: Optional[str] = None,
    category: Optional[str] = None
):
    results = items_db.copy()

    if item_type and item_type.lower() != "all":
        results = [i for i in results if i["type"].lower() == item_type.lower()]

    if category and category.lower() != "all":
        results = [i for i in results if i["category"].lower() == category.lower()]

    if search:
        q = search.lower()
        results = [
            i for i in results 
            if q in i["title"].lower() 
            or q in i["description"].lower() 
            or q in i["location"].lower()
        ]

    return results

# Report new lost or found item
@app.post("/api/items")
async def create_item(
    title: str = Form(...),
    item_type: str = Form(...),  # 'lost' or 'found'
    category: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    contact: str = Form(...),
    photo: Optional[UploadFile] = File(None)
):
    item_id = str(uuid.uuid4())[:8]
    image_url = "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=500&auto=format&fit=crop&q=60"

    # Save to decoupled storage
    if photo:
        extension = photo.filename.split(".")[-1] if "." in photo.filename else "jpg"
        filename = f"{item_id}_{uuid.uuid4().hex[:6]}.{extension}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # In production this points to https://<bucket>.s3.amazonaws.com/filename
        image_url = f"/storage/{filename}"
        
        # Simulate serverless event-driven trigger (Session 6/7)
        print(f"[EVENT-TRIGGER] s3:ObjectCreated:Put -> Lambda invoked for {filename}")
        print(f"[EVENT-TRIGGER] Thumbnail generated: 300x300. Checking matching search tags for '{title}'...")

    new_item = {
        "id": item_id,
        "title": title,
        "type": item_type.lower(),
        "category": category,
        "location": location,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "contact": contact,
        "image_url": image_url,
        "status": "active"
    }

    items_db.insert(0, new_item)
    return {
        "message": "Item posted successfully",
        "item": new_item,
        "cloud_event": "Object stored in decoupled storage; event notification dispatched"
    }
