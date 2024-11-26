import requests

from ligpargen_gui.model.util import safeguard


def download_file(url: str, save_path, timeout=(5, 10)) -> bool:
  """Downloads a file from the given URL to the given filepath.

  Args:
    url: The URL to download.
    save_path: The filepath to save the downloaded file to.

  Returns:
    True if the download finished successfully, Otherwise: False
  """
  # <editor-fold desc="Checks">
  safeguard.CHECK(url is not None)
  safeguard.CHECK(save_path is not None)
  # </editor-fold>
  try:
    # Send a GET request to the URL
    response = requests.get(url, stream=True, timeout=timeout)
    response.raise_for_status()  # Check for HTTP errors
    # Write the content to a file in chunks to avoid memory issues with large files
    with open(save_path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
          file.write(chunk)
    print(f"File downloaded successfully and saved to {save_path}")
    return True
  except requests.exceptions.RequestException as e:
    print(f"Error downloading file: {e}")
    return False
