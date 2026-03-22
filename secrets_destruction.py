from google.cloud import secretmanager
from logger import logger


def destroy_secret_version(
    project_id: str, secret_id: str, version_id: str
) -> secretmanager.DestroySecretVersionRequest:
    """
    Destroy the given secret version, making the payload irrecoverable. Other
    secrets versions are unaffected.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret version
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # Destroy the secret version.
    response = client.destroy_secret_version(request={"name": name})
    logger.info(f"Destroyed secret version: {response.name}")


def run_destruction(project_id: str, secret_id: str) -> None:
    """
    List all secret versions in the given secret and their metadata.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the parent secret.
    parent = client.secret_path(project_id, secret_id)
    # List all secret versions.

    ls= [int(version.name.split('/')[5]) for version in client.list_secret_versions(request={"parent": parent}) if version.state.value == 1 ]
    ls.sort(reverse=True)
    if len(ls) < 2:
        logger.info("nothing to delete.")
    else:
        ls.pop(0)
        for vrsion_num in ls:
                logger.info(f"detroing.. {vrsion_num}")
                destroy_secret_version(project_id, secret_id, vrsion_num)



