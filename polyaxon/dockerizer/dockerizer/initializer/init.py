import traceback

from . import settings
from .download import download
from .generate import generate


def init(job: 'Job',
         build_context: str,
         from_image: str,
         commit: str) -> bool:
    build_path = '{}/{}'.format(build_context, 'build')
    # Download repo
    filename = '_code'
    status = download(
        job=job,
        build_path=build_path,
        filename=filename,
        commit=commit)
    if not status:
        return status
    # Generate dockerfile
    return generate(job=job,
                    build_path=build_path,
                    from_image=from_image,
                    build_steps=settings.CONTAINER_BUILD_STEPS,
                    env_vars=settings.CONTAINER_ENV_VARS,
                    nvidia_bin=settings.MOUNT_PATHS_NVIDIA)


def cmd(job: 'Job',
        build_context: str,
        from_image: str,
        commit: str):
    # Initializing the docker context
    try:
        status = init(job=job,
                      build_context=build_context,
                      from_image=from_image,
                      commit=commit)
        if not status:
            job.failed(message='Failed to initialize build job job.')
            return
    except Exception as e:  # Other exceptions
        job.failed(
            message='Failed to build job encountered an {} exception'.format(e.__class__.__name__),
            traceback=traceback.format_exc())
        return
