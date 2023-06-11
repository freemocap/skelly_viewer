# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from skelly_viewer.experimental.plotly.plotly_dash_setup import DataLoader
from skelly_viewer.experimental.plotly.skeleton_viewer import SAMPLE_DATA_PATH

app = FastAPI()

# Allow all origins to make requests to this app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_loader = DataLoader(SAMPLE_DATA_PATH)

@app.get("/data/trajectory")
def get_trajectory_data(trajectory_name: str="nose"):
    return data_loader.get_trajectory(trajectory_name=trajectory_name)

@app.get("/data/frame")
def get_frame_data(frame_number: int=0):
    return data_loader.get_frame_data(frame_number=frame_number)

@app.get("/data/next_frame")
def get_next_frame_data():
    return data_loader.get_frame_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
