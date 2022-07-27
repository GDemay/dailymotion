from fastapi import APIRouter, Body, Depends, HTTPException

router = APIRouter()


@router.post("/login/coucou")
def coucou(coucou: str):
    return {"message": coucou}
