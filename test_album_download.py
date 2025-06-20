#!/usr/bin/env python3
"""
Test des Fotoalbum Download-Features
"""
from gridfs_demo import PhotoAlbum
import os

def test_album_download():
    album = PhotoAlbum()
    
    # Download Ordner erstellen
    download_dir = "/tmp/downloaded_albums"
    
    print("Verfügbare Alben:")
    albums = album.list_albums()
    for album_name in albums:
        print(f"- {album_name}")
        album.list_album_contents(album_name)
    
    print(f"\nDownload Test: Album 'Urlaub 2025' nach {download_dir}")
    album.download_album("Urlaub 2025", download_dir)
    
    print(f"\nDownloaded Dateien:")
    if os.path.exists(download_dir):
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            size = os.path.getsize(file_path)
            print(f"- {file} ({size} bytes)")

if __name__ == "__main__":
    test_album_download()
