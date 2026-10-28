
from pathlib import Path

from pywinauto import Desktop
from pywinauto.application import Application


EXE_PATH = Path(r"C:\Lagamine\VS_Project\Prepro\x64\Debug\Prepro.exe")

REFERENCE_FILE = Path(r"C:\Program Files (x86)\LagaProgs\THOMMES ELIOTT\Diffusion\Test\dif_mesh.LAG")

INPUT_FILES = [
    Path(r"C:\Program Files (x86)\LagaProgs\THOMMES ELIOTT\Diffusion\Test\dif_mesh.LAG"),
]


def select_file(app: Application, file_path: Path) -> None:
    """Select a file in a standard Windows Open dialog."""

    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    dialog = app.window(
        class_name="#32770",
        title_re=r"(?i).*(Open|Ouvrir).*",
    )
    dialog.wait("ready", timeout=60)

    # Remember this dialog's identity.
    handle = dialog.wrapper_object().handle

    # Locate the filename field.
    file_edit = dialog.child_window(
        auto_id="1148",
        control_type="Edit",
    )

    file_edit.set_edit_text(str(file_path))

    # Confirm the file selection.
    file_edit.type_keys("{ENTER}")

    # Wait for this specific dialog to close.
    Desktop(backend="uia").window(
        handle=handle
    ).wait_not("exists", timeout=30)


def run_computation(
    reference_file: Path,
    input_file: Path,
) -> None:
    """Launch the executable and supply its two files."""

    print(f"Processing: {input_file.name}")

    app = Application(backend="uia").start(
        f'"{EXE_PATH}"'
    )

    # First file-selection dialog.
    select_file(app, reference_file)

    # Second file-selection dialog.
    select_file(app, input_file)

    # Assumes the executable exits after the computation.
    app.wait_for_process_exit(timeout=1800)

    print(f"Finished: {input_file.name}")


def main() -> None:
    for input_file in INPUT_FILES:
        run_computation(REFERENCE_FILE, input_file)


if __name__ == "__main__":
    main()

