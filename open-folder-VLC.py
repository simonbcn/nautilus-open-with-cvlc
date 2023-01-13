import gi 
import shutil
import subprocess

gi.require_version('Nautilus', '4.0')

from gi.repository import Nautilus, GObject
from typing import List

class openFolderVLC(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super().__init__()

    def menu_activate_cb(
         self,
         menu: Nautilus.MenuItem,
         file: Nautilus.FileInfo,
     ) -> None:
        if file.is_gone():
            return
        
        subprocess.Popen(["cvlc",file.get_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT,start_new_session=True)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
        ) -> List[Nautilus.MenuItem]:
        if len(files) != 1 or shutil.which("cvlc") is None:
            return []

        file = files[0]

        if not file.is_directory():
            return[]
        
        item = Nautilus.MenuItem(
            name="abrirConVLC",
            label="Abrir con VLC: %s" % file.get_name(),
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
         self,
         current_folder: Nautilus.FileInfo,
     ) -> List[Nautilus.MenuItem]:
         return []
