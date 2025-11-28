from app.core.http_client import client_1688


class SearchService:

    async def search_keyword(self, query: str, country: str):
        return await client_1688.get(
            "/marketplaces/1688/search/keyword/",
            params={
                "keyword": query,
                "country": country,
                "filter_forbidden_cats": True,
                "spell_check": True,
                "from_recent": False,
                "begin_page": 1,
                "page_size": 10
            }
        )


    async def upload_photo(self, file, user_id=None, out_member_id=None):
        files = {
            "image_file": (
                file.filename,
                await file.read(),
                file.content_type,
            )
        }

        params = {}
        if user_id is not None:
            params["user_id"] = user_id
        if out_member_id is not None:
            params["outMemberId"] = out_member_id

        response = await client_1688.post(
            "/marketplaces/1688/search/upload/",
            params=params,
            files=files
        )

        return response

    async def search_by_image_id(self, image_id):
        params = {
            "image_id": image_id,
            "page_size": 10,
            "begin_page": 1,
            "country": "ru",
            "sort": "default",
            "filter_forbidden_cats": True,
            "from_recent": False,
        }

        response = await client_1688.get(
            "/marketplaces/1688/search/image-get/",
            params=params
        )
        return response

    async def search_photo(self, file):
        upload_info = await self.upload_photo(file)
        image_id = upload_info["data"]["image_id"]

        results = await self.search_by_image_id(image_id)

        return {
            "status": "ok",
            "image_id": image_id,
            "upload_info": upload_info,
            "results": results,
        }
