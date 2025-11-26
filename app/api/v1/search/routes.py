from fastapi import APIRouter, UploadFile, File
from app.services.search_service import SearchService
search_router = APIRouter()
service = SearchService()


@search_router.get("/keyword")
async def search_by_keyword(q: str):
    result = await service.search_keyword(q)
    return result


@search_router.post("/photo/upload")
async def upload_photo(file: UploadFile = File(...)):
    return await service.upload_photo(file)

@search_router.get("/photo/results")
async def search_results(image_id: str):
    return await service.search_by_image_id(image_id)

@search_router.post("/photo")
async def auto_photo_search(file: UploadFile = File(...)):
    return await service.search_photo(file)

