from typing import Optional, Union

from django.core.exceptions import ObjectDoesNotExist

from db.models.repos import CodeReference


def get_code_reference(instance, commit: str = None) -> Optional['CodeReference']:
    project = instance.project

    if not project.has_code:
        return None

    repo = project.repo or project.external_repo

    if commit:
        try:
            return CodeReference.objects.get(repo=repo, commit=commit)
        except ObjectDoesNotExist:
            return None

    # If no commit is provided we get the last commit, and save new ref if not found
    try:
        last_commit = repo.last_commit
    except ValueError:
        return None

    code_reference, _ = CodeReference.objects.get_or_create(repo=repo, commit=last_commit[0])
    return code_reference


RefModel = Union['Experiment',
                 'ExperimentGroup',
                 'Job',
                 'BuildJob',
                 'TensorboardJob',
                 'NotebookJob']


def assign_code_reference(instance: RefModel, commit: str = None) -> RefModel:
    if instance.code_reference is not None or instance.specification is None:
        return instance
    build = instance.specification.build if instance.specification else None
    if not commit and build:
        commit = build.ref
    code_reference = get_code_reference(instance=instance, commit=commit)
    if code_reference:
        instance.code_reference = code_reference

    return instance
