from dalloriam import filesystem, shell


def build(build_path: str, image_name: str, tag: str = 'latest') -> None:
    """
    Builds a docker image from a directory.
    Args:
        build_path: Path that contains the image-related files.
        image_name: Desired name of the built image.
        tag:        Desired tag of the built image.
    """
    # TODO: Give options to log or not.

    with filesystem.location(build_path):
        image_name = f'{image_name}:{tag}'
        shell.run([
            'docker',
            'build',
            '-t',
            image_name,
            '.'
        ], silent=True)


def push(image_name: str, tag: str = 'latest'):
    image_name = f'{image_name}:{tag}'
    shell.run([
        'docker',
        'push',
        image_name
    ], silent=False)
