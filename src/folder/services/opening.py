import short_url


class FolderOpenManager:

    @staticmethod
    async def create_open_url(workspace_id: int):
        url = short_url.encode_url(workspace_id, 10)
        return url

    @staticmethod
    async def get_folder_id(workspace_open_url):
        workspace_id = short_url.decode_url(workspace_open_url)
        return workspace_id

