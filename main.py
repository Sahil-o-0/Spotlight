from fastapi import FastAPI
from logics.api_logic import count_status, get_hrbp_data, proj_status

app = FastAPI()

@app.get("/count_status")
async def handle_count_status(fieldname: str):
    return await count_status(fieldname)

@app.get("/hrbp")
async def handle_hrbp():
    return await get_hrbp_data()

@app.get("/proj_status")
async def handle_proj_status():
    return await proj_status()