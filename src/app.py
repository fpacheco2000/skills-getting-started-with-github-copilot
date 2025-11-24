"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    # Add sports-related activities
    activities.setdefault("Basketball Team", {
        "description": "Competitive and recreational basketball practices and games",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["ryan@mergington.edu", "alex@mergington.edu"]
    })
    activities.setdefault("Soccer Club", {
        "description": "Outdoor soccer practices, drills, and friendly matches",
        "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["lisa@mergington.edu"]
    })

    # Add artistic activities
    activities.setdefault("Art Workshop", {
        "description": "Painting, drawing, and mixed-media projects for all skill levels",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["nora@mergington.edu"]
    })
    activities.setdefault("Drama Club", {
        "description": "Acting, stagecraft, and production of school plays",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["maria@mergington.edu", "kevin@mergington.edu"]
    })

    # Add intellectual activities
    activities.setdefault("Debate Team", {
        "description": "Competitive debate practice and tournaments",
        "schedule": "Mondays, 3:45 PM - 5:15 PM",
        "max_participants": 12,
        "participants": ["oliver@mergington.edu"]
    })
    activities.setdefault("Science Club", {
        "description": "Hands-on experiments, science fairs, and research projects",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu"]
    })

    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate student is not already signed up
    for activity in activities.values():
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student already signed up for an activity")
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
