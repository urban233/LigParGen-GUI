import requests


def download_file(url, save_path) -> bool:
  try:
    # Send a GET request to the URL
    response = requests.get(url, stream=True)
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
