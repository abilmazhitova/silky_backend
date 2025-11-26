from app.core.http_client import client_1688


class SearchImageService:

    async def upload_image(self, file):
        """
        Шаг 1 — загрузка фото в Silky 1688
        Возвращает image_id
        """
        files = {
            "image_file": (
                file.filename,
                await file.read(),
                file.content_type,
            )
        }

        response = await client_1688.post(
            "/marketplaces/1688/search/upload/",
            files=files
        )

        # image_id лежит тут:
        image_id = response["data"]["image_id"]

        return {
            "status": "ok",
            "message": "Image uploaded successfully",
            "image_id": image_id,
            "raw": response
        }

    async def search_by_image_id(self, image_id: str):
        """
        Шаг 2 — поиск по ранее загруженному фото
        """
        response = await client_1688.get(
            "/marketplaces/1688/search/image-get/",
            params={
                "image_id": image_id,
                "begin_page": 1,
                "page_size": 10,
                "country": "ru",
                "sort": "default"
            }
        )

        return {
            "status": "ok",
            "message": "Search by image_id completed",
            "data": response
        }
