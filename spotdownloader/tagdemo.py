# -*- coding: utf-8 -*-
import taglib
import itunespy

song = taglib.File("sia.mp3")
print(song.tags)
song.tags["ALBUM"] = ["White Album"]
song.save()
