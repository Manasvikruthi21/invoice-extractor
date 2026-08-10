from pathlib import Path


class DocumentLoader:
    """
    Loads and validates document paths.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".bmp",
    }

    @staticmethod
    def validate(path: str):
        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(f"{path} not found.")

        if file.suffix.lower() not in DocumentLoader.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {file.suffix}"
            )

        return file