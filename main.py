from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

app = FastAPI(
    title="Trading App",
    description="API for a trading application",
    version="1.0",
)

fake_users = [
    {"id": 1, "role": "admin", "name": "nurba"},
    {"id": 2, "role": "investor", "name": "kuri"},
    {"id": 3, "role": "trader", "name": "beks"},
    {"id": 4, "role": "trader", "name": "beks", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]},
]

class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []

@app.get("/users/{user_id}", response_model=List[User], description="Get user details by user ID")
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]

fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 2, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12},
]

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float

@app.post('/trades', description="Add trades to the system")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
