import asyncio, httpx, zipfile, os, aiofiles, platform


async def download_and_extract(url, extract_to="camoufox", on_progress=None):
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            async with client.stream("GET", url) as r:
                if r.status_code != 200:
                    return False
                async with aiofiles.open("data.zip", "wb") as f:
                    downloaded = 0
                    async for chunk in r.aiter_bytes():
                        await f.write(chunk)
                        downloaded += len(chunk)
                        if on_progress:
                            await on_progress(downloaded, int(r.headers.get("content-length", 0)), "Загрузка")
                    
                    # Ensure the file is completely written to disk
                    await f.flush()
                    os.fsync(f.fileno())
    except Exception as e:
        print('Download error ', e)
        return False

    try:
        # Verify that the downloaded file is actually a valid zip file before extraction
        if not zipfile.is_zipfile("data.zip"):
            raise Exception("Downloaded file is not a valid zip file")
        
        os.makedirs(extract_to, exist_ok=True)
        with zipfile.ZipFile("data.zip") as zf:
            files = zf.infolist()
            for i, member in enumerate(files):
                await asyncio.to_thread(zf.extract, member, extract_to)
                if on_progress:
                    await on_progress(i + 1, len(files), "Распаковка")
                await asyncio.sleep(0)
    except Exception as e:
        print('Arhiv error ', e)
        return False

    if platform.system() != "Windows":
        bin_path = os.path.join(extract_to, "camoufox-bin")
        if os.path.exists(bin_path):
            os.chmod(bin_path, 0o755)

    os.remove("data.zip")
    return True
