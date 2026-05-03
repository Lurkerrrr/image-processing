import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
from utils.loader import load_images
from processing.worker import process_images_concurrently


SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

LANGUAGES = {
    "English": {
        "title": "Image Processor",
        "input_folder": "Input folder:",
        "output_folder": "Output folder:",
        "browse": "Browse",
        "select_filters": "Select Filters:",
        "process": "Process Images",
        "log": "Log:",
        "no_images": "No images found in the input folder.",
        "please_wait": "Processing... please wait.",
        "done": "Done! {} image(s) processed successfully.",
        "no_filters": "Please select at least one filter.",
        "loaded": "Loaded: {}",
        "language": "Language:",
        "workers": "Worker processes:",
        "all_cores": "All CPU cores",
        "input_not_exist": "Input folder does not exist.",
        "input_empty": "Input folder is empty.",
        "no_supported_images": "No supported images found. Supported formats: {}",
        "output_empty": "Output folder path cannot be empty.",
    },
    "Polski": {
        "title": "Przetwarzacz Obrazów",
        "input_folder": "Folder wejściowy:",
        "output_folder": "Folder wyjściowy:",
        "browse": "Przeglądaj",
        "select_filters": "Wybierz filtry:",
        "process": "Przetwórz obrazy",
        "log": "Dziennik:",
        "no_images": "Nie znaleziono obrazów w folderze wejściowym.",
        "please_wait": "Przetwarzanie... proszę czekać.",
        "done": "Gotowe! Przetworzono {} obraz(ów).",
        "no_filters": "Proszę wybrać co najmniej jeden filtr.",
        "loaded": "Wczytano: {}",
        "language": "Język:",
        "workers": "Procesy robocze:",
        "all_cores": "Wszystkie rdzenie CPU",
        "input_not_exist": "Folder wejściowy nie istnieje.",
        "input_empty": "Folder wejściowy jest pusty.",
        "no_supported_images": "Nie znaleziono obsługiwanych obrazów. Obsługiwane formaty: {}",
        "output_empty": "Ścieżka folderu wyjściowego nie może być pusta.",
    }
}

FILTERS = [
    "grayscale",
    "blur",
    "sharpen",
    "edge_detection",
    "brighten",
    "darken",
    "increase_contrast",
    "invert",
    "flip_horizontal",
    "flip_vertical",
]


class ImageProcessingApp:
    """Main application class for the Image Processing Pipeline GUI."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_language = "English"
        self.texts = LANGUAGES[self.current_language]

        self.input_dir = tk.StringVar(value="inputs")
        self.output_dir = tk.StringVar(value="outputs")
        self.filter_vars = {f: tk.BooleanVar(value=False) for f in FILTERS}
        self.num_workers = tk.StringVar(value="all_cores")

        self._build_ui()
        self._update_texts()

    def _build_ui(self):
        """Build all UI components."""
        self.root.resizable(False, False)
        self.root.configure(padx=15, pady=15)

        lang_frame = tk.Frame(self.root)
        lang_frame.pack(fill="x", pady=(0, 10))

        self.lang_label = tk.Label(lang_frame, font=("Arial", 9))
        self.lang_label.pack(side="left")

        self.lang_var = tk.StringVar(value=self.current_language)
        lang_dropdown = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=10
        )
        lang_dropdown.pack(side="left", padx=(5, 0))
        lang_dropdown.bind("<<ComboboxSelected>>", self._on_language_change)

        folder_frame = tk.LabelFrame(self.root, padx=10, pady=10)
        folder_frame.pack(fill="x", pady=(0, 10))
        self.folder_frame = folder_frame

        self.input_label = tk.Label(folder_frame, font=("Arial", 9))
        self.input_label.grid(row=0, column=0, sticky="w", pady=3)
        tk.Entry(folder_frame, textvariable=self.input_dir, width=35).grid(row=0, column=1, padx=5)
        self.input_browse_btn = tk.Button(folder_frame, command=self._browse_input)
        self.input_browse_btn.grid(row=0, column=2)

        self.output_label = tk.Label(folder_frame, font=("Arial", 9))
        self.output_label.grid(row=1, column=0, sticky="w", pady=3)
        tk.Entry(folder_frame, textvariable=self.output_dir, width=35).grid(row=1, column=1, padx=5)
        self.output_browse_btn = tk.Button(folder_frame, command=self._browse_output)
        self.output_browse_btn.grid(row=1, column=2)

        filter_frame = tk.LabelFrame(self.root, padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        self.filter_frame = filter_frame

        self.filter_checkboxes = {}
        for i, f in enumerate(FILTERS):
            cb = tk.Checkbutton(filter_frame, text=f, variable=self.filter_vars[f])
            cb.grid(row=i // 3, column=i % 3, sticky="w", padx=5, pady=2)
            self.filter_checkboxes[f] = cb

        worker_frame = tk.Frame(self.root)
        worker_frame.pack(fill="x", pady=(0, 10))

        self.workers_label = tk.Label(worker_frame, font=("Arial", 9))
        self.workers_label.pack(side="left")

        self.workers_dropdown = ttk.Combobox(
            worker_frame,
            textvariable=self.num_workers,
            values=["all_cores", "1", "2", "4", "8"],
            state="readonly",
            width=22
        )
        self.workers_dropdown.pack(side="left", padx=(5, 0))

        self.process_btn = tk.Button(
            self.root,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
            command=self._on_process
        )
        self.process_btn.pack(fill="x", pady=(0, 10))

        log_frame = tk.LabelFrame(self.root, padx=10, pady=10)
        log_frame.pack(fill="both", expand=True)
        self.log_frame = log_frame

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            state="disabled",
            font=("Courier", 9)
        )
        self.log_area.pack(fill="both", expand=True)

    def _update_texts(self):
        """Update all UI text elements to the current language."""
        t = self.texts
        self.root.title(t["title"])
        self.lang_label.config(text=t["language"])
        self.folder_frame.config(text=t["title"])
        self.input_label.config(text=t["input_folder"])
        self.output_label.config(text=t["output_folder"])
        self.input_browse_btn.config(text=t["browse"])
        self.output_browse_btn.config(text=t["browse"])
        self.filter_frame.config(text=t["select_filters"])
        self.process_btn.config(text=t["process"])
        self.log_frame.config(text=t["log"])
        self.workers_label.config(text=t["workers"])
        self.workers_dropdown.config(
            values=[t["all_cores"], "1", "2", "4", "8"]
        )
        if self.num_workers.get() in ["all_cores", "Wszystkie rdzenie CPU", "All CPU cores"]:
            self.num_workers.set(t["all_cores"])

    def _on_language_change(self, event=None):
        """Handle language dropdown change."""
        self.current_language = self.lang_var.get()
        self.texts = LANGUAGES[self.current_language]
        self._update_texts()

    def _browse_input(self):
        """Open folder browser for input directory."""
        folder = filedialog.askdirectory(initialdir=self.input_dir.get())
        if folder:
            self.input_dir.set(folder)

    def _browse_output(self):
        """Open folder browser for output directory."""
        folder = filedialog.askdirectory(initialdir=self.output_dir.get())
        if folder:
            self.output_dir.set(folder)

    def _log(self, message: str):
        """Append a message to the log area."""
        self.log_area.config(state="normal")
        self.log_area.insert("end", f"> {message}\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def _clear_log(self):
        """Clear the log area."""
        self.log_area.config(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.config(state="disabled")

    def _validate(self) -> bool:
        """
        Validate all inputs before processing.

        :return: True if all inputs are valid, False otherwise
        """
        t = self.texts
        input_dir = self.input_dir.get().strip()
        output_dir = self.output_dir.get().strip()
        is_valid = True

        if not output_dir:
            self._log(t["output_empty"])
            is_valid = False

        if not os.path.exists(input_dir):
            self._log(t["input_not_exist"])
            is_valid = False
        else:
            all_files = os.listdir(input_dir)
            if not all_files:
                self._log(t["input_empty"])
                is_valid = False
            else:
                supported_files = [
                    f for f in all_files
                    if f.lower().endswith(SUPPORTED_FORMATS)
                ]
                if not supported_files:
                    formats = ", ".join(SUPPORTED_FORMATS)
                    self._log(t["no_supported_images"].format(formats))
                    is_valid = False

        steps = [f for f, var in self.filter_vars.items() if var.get()]
        if not steps:
            self._log(t["no_filters"])
            is_valid = False

        return is_valid

    def _on_process(self):
        """Handle the Process Images button click."""
        self._clear_log()

        if not self._validate():
            return

        steps = [f for f, var in self.filter_vars.items() if var.get()]

        self.process_btn.config(state="disabled")
        self._log(self.texts["please_wait"])

        thread = threading.Thread(target=self._run_processing, args=(steps,))
        thread.daemon = True
        thread.start()

    def _run_processing(self, steps: list[str]):
        """Run the image processing pipeline in a background thread."""
        t = self.texts

        workers_val = self.num_workers.get()
        if workers_val in ["all_cores", t["all_cores"]]:
            num_workers = None
        else:
            num_workers = int(workers_val)

        images = load_images(self.input_dir.get())

        if not images:
            self.root.after(0, self._log, t["no_images"])
            self.root.after(0, self.process_btn.config, {"state": "normal"})
            return

        for filename, _ in images:
            self.root.after(0, self._log, t["loaded"].format(filename))

        process_images_concurrently(
            images=images,
            steps=steps,
            output_dir=self.output_dir.get(),
            num_workers=num_workers
        )

        self.root.after(0, self._log, t["done"].format(len(images)))
        self.root.after(0, self.process_btn.config, {"state": "normal"})


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("icon.ico")
    except Exception:
        pass
    app = ImageProcessingApp(root)
    root.mainloop()