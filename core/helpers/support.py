from csv import reader
from os import walk
import pygame


def import_csv_layout(path) -> list:
    """
    >>> Import and treat the content of a CSV file.
    """
    terrain_map = list()
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path) -> list:
    """
    >>> Import a folder content with pygame treatment.
    """
    surface_list = list()
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
