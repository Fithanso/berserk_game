import pygame


def get_anim_frames(dir, frames_num, scale=None):
    frames = []
    for i in range(1, frames_num+1):

        filename = f'{i}.png'
        filepath = f'images/{dir}/' + filename
        image = pygame.image.load(filepath)
        if scale:
            image = pygame.transform.scale(image, scale)
        frames.append(image)

    return frames
