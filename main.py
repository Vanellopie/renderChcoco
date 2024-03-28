from supabase import create_client, Client
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException
from typing import List

# https://docs.render.com/deploy-fastapi

supabase_url: str = "https://pudktqwdyxdtkyxgxqzj.supabase.co"
supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1ZGt0cXdkeXhkdGt5eGd4cXpqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTAzODE1MzMsImV4cCI6MjAyNTk1NzUzM30._MzX-DYB7YOtSKrJPxUxXDSQFmS6HVBj0AdJJ6ShfWE"

supabase: Client = create_client(supabase_url, supabase_key)

class ChocolateBar(BaseModel):
    id: Optional[int] = None
    company: Optional[str] = None
    specific_bean_origin_or_bar_name: Optional[str] = None
    ref: Optional[int] = None
    review_date: Optional[int] = None
    cocoa_percent: Optional[str] = None
    company_location: Optional[str] = None
    rating: Optional[float] = None
    bean_type: Optional[str] = None
    broad_bean_origin: Optional[str] = None


app = FastAPI()

@app.post("/chocolate_bars/", response_model=ChocolateBar)
def create_chocolate_bar(chocolate_bar: ChocolateBar):
    data = chocolate_bar.dict(exclude_unset=True)
    inserted_data = supabase.table("chocolate_bars").insert(data).execute()
    if inserted_data.data:
        return inserted_data.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error inserting data")

@app.get("/chocolate_bars/", response_model=List[ChocolateBar])
def read_chocolate_bars():
    data = supabase.table("chocolate_bars").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Error reading data")
    

@app.put("/chocolate_bars/{chocolate_bar_id}", response_model=ChocolateBar)
def update_chocolate_bar(chocolate_bar_id: int, chocolate_bar: ChocolateBar):
    data = chocolate_bar.dict(exclude_unset=True)
    updated_data = supabase.table("chocolate_bars").update(data).eq("id", chocolate_bar_id).execute()
    if updated_data.data:
        return updated_data.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error updating data")

@app.delete("/chocolate_bars/{chocolate_bar_id}", response_model=List[ChocolateBar])
def delete_chocolate_bar(chocolate_bar_id: int):
    deleted_data = supabase.table("chocolate_bars").delete().eq("id", chocolate_bar_id).execute()
    if deleted_data.data:
        return deleted_data.data
    else:
        raise HTTPException(status_code=400, detail="Error deleting data")
