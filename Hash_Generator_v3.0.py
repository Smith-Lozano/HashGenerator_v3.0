# Hash_Generator_v3.0.py

import os
import sys
import csv
import json
import time
import hashlib
import zlib
import datetime
from pathlib import Path
from typing import Optional, Callable, List, Dict

# GUI libs
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import customtkinter as ctk
except Exception as e:
    raise RuntimeError("Este programa requiere customtkinter. Instálalo con `pip install customtkinter`. Error: " + str(e))

# optional libs
try:
    import xxhash
except Exception:
    xxhash = None

try:
    from Crypto.Hash import Whirlpool
except Exception:
    Whirlpool = None

# --------------------------- Config ---------------------------
CHUNK = 4 * 1024 * 1024
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
AUDIT_CSV = LOGS_DIR / "audit_log.csv"

SUPPORTED_ALGOS = [
    "MD5", "SHA1", "SHA256", "SHA512",
    "BLAKE2b", "BLAKE2s", "SHA3-256", "SHA3-512",
    "Whirlpool", "xxHash64", "CRC32", "Adler32"
]

if xxhash is None:
    SUPPORTED_ALGOS = [a for a in SUPPORTED_ALGOS if a != "xxHash64"]
if Whirlpool is None:
    SUPPORTED_ALGOS = [a for a in SUPPORTED_ALGOS if a != "Whirlpool"]

# Ensure audit file header
if not AUDIT_CSV.exists():
    with open(AUDIT_CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(["timestamp","algorithm","path_or_text","type","size_bytes","duration","hash"])

# --------------------------- Helpers ---------------------------

def ts() -> str:
    """ISO timestamp (not for filenames)."""
    return datetime.datetime.now().isoformat()

def safe_timestamp() -> str:
    """Timestamp safe to use in filenames on Windows: YYYYMMDD_HHMMSS"""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

class CRC32Hash:
    def __init__(self):
        self.value = 0
    def update(self, data: bytes):
        self.value = zlib.crc32(data, self.value)
    def hexdigest(self):
        return format(self.value & 0xFFFFFFFF, '08x')

class Adler32Hash:
    def __init__(self):
        self.value = 1
    def update(self, data: bytes):
        self.value = zlib.adler32(data, self.value)
    def hexdigest(self):
        return format(self.value & 0xFFFFFFFF, '08x')

def _init_hasher(algo: str):
    a = algo.upper()
    if a == 'MD5': return hashlib.md5()
    if a == 'SHA1': return hashlib.sha1()
    if a == 'SHA256': return hashlib.sha256()
    if a == 'SHA512': return hashlib.sha512()
    if a == 'BLAKE2B': return hashlib.blake2b()
    if a == 'BLAKE2S': return hashlib.blake2s()
    if a == 'SHA3-256': return hashlib.sha3_256()
    if a == 'SHA3-512': return hashlib.sha3_512()
    if a == 'WHIRLPOOL':
        if Whirlpool is None:
            raise Exception('Whirlpool no disponible (instala pycryptodome)')
        return Whirlpool.new()
    if a == 'XXHASH64':
        if xxhash is None:
            raise Exception('xxhash no disponible (instala xxhash)')
        return xxhash.xxh64()
    if a == 'CRC32': return CRC32Hash()
    if a == 'ADLER32': return Adler32Hash()
    raise Exception('Algoritmo no soportado: '+algo)

# compute_hash_file_sync adapted to tkinter: accepts root to call update()
def compute_hash_file_sync(path: str, algo: str, progress_cb: Optional[Callable[[int], None]] = None, tk_root: Optional[tk.Tk] = None) -> tuple[str, float]:
    """Compute file hash synchronously but keep GUI responsive by calling tk_root.update() if provided."""
    start = time.time()
    total = os.path.getsize(path)
    processed = 0
    h = _init_hasher(algo)
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(CHUNK)
            if not chunk:
                break
            h.update(chunk)
            processed += len(chunk)
            if total > 0:
                pct = int((processed/total)*100)
            else:
                pct = 100
            if progress_cb:
                try:
                    progress_cb(pct)
                except Exception:
                    pass
            if tk_root:
                try:
                    tk_root.update()
                except Exception:
                    pass
    digest = h.hexdigest()
    duration = time.time() - start
    if progress_cb:
        try:
            progress_cb(100)
        except Exception:
            pass
    return digest, duration

# --------------------------- Manifest TXT helpers ---------------------------
def export_manifest_txt(entries: List[Dict[str,str]], file_path: str) -> None:
    """Export manifest in human-readable TXT format."""
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write("# MANIFEST - formato TXT (humano legible)\n")
        f.write(f"# generado: {ts()}\n\n")
        for it in entries:
            fname = it.get('file') or it.get('path') or ''
            alg = it.get('algorithm') or it.get('alg') or ''
            h = it.get('hash') or it.get('checksum') or ''
            f.write(f"Archivo: {fname}\n")
            if alg:
                f.write(f"Algoritmo: {alg}\n")
            f.write(f"Hash: {h}\n\n")

def export_batch_txt_detailed(entries: List[Dict[str,str]], file_path: str, algo_declared: Optional[str] = None) -> None:
    """
    Exporta lote en formato TXT detallado y legible.
    entries = lista de dicts con: file, size, hash, duration, algorithm (optional)
    algo_declared = algoritmo seleccionado para el lote (se usa como fallback)
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    datetime_str = now.strftime("%d/%m/%Y %H:%M:%S")
    total_items = len(entries)
    # calcular tiempo total sumando duraciones parseables
    total_duration = 0.0
    for e in entries:
        d = e.get('duration', '')
        try:
            total_duration += float(d)
        except Exception:
            # si duración tiene formato '0.123' o ' - ' o 'Procesando...'
            # ignorar si no es convertible
            pass

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# EXPORTACIÓN DE HASHES - LOTE\n")
        f.write(f"# Fecha y hora de exportación: {datetime_str}\n")
        if algo_declared:
            f.write(f"# Algoritmo seleccionado para el lote: {algo_declared}\n")
        f.write(f"# Elementos: {total_items}\n")
        f.write(f"# Duración total (sumada cuando disponible): {total_duration:.6f} segundos\n")
        f.write("# ------------------------------------------------------------\n\n")

        for e in entries:
            filepath = e.get('file', '')
            nombre = os.path.basename(filepath) if filepath else ''
            extension = Path(filepath).suffix.replace(".", "").upper() if filepath else "DESCONOCIDO"
            size = e.get('size', '')
            h = e.get('hash', '')
            alg = e.get('algorithm') or algo_declared or ""
            duration = e.get('duration', '')
            f.write(f"Archivo: {nombre}\n")
            f.write(f"Ruta completa: {filepath}\n")
            f.write(f"Tipo: {extension}\n")
            f.write(f"Tamaño: {size} bytes\n")
            f.write(f"Hash: {h}\n")
            if alg:
                f.write(f"Tipo de hash: {alg}\n")
            f.write(f"Duración: {duration} segundos\n")
            f.write(f"Fecha: {date_str}\n")
            f.write("------------------------------------------------------------\n\n")

def parse_manifest_txt(file_path: str) -> List[Dict[str,str]]:
    """Parse human readable manifest TXT into list of entries."""
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [ln.rstrip('\n') for ln in f]

    buf = {'file': None, 'algorithm': None, 'hash': None}
    for line in lines:
        s = line.strip()
        if not s:
            if buf['file'] and buf['hash']:
                entries.append({'path': buf['file'], 'hash': buf['hash'], 'algorithm': buf['algorithm']})
            buf = {'file': None, 'algorithm': None, 'hash': None}
            continue
        if s.lower().startswith('archivo:'):
            buf['file'] = s.partition(':')[2].strip()
        elif s.lower().startswith('algoritmo:'):
            buf['algorithm'] = s.partition(':')[2].strip()
        elif s.lower().startswith('hash:'):
            buf['hash'] = s.partition(':')[2].strip()
        else:
            if '|' in s:
                parts = [p.strip() for p in s.split('|')]
                if len(parts) >= 3:
                    buf['file'] = parts[0]
                    buf['algorithm'] = parts[1]
                    buf['hash'] = parts[2]
    if buf['file'] and buf['hash']:
        entries.append({'path': buf['file'], 'hash': buf['hash'], 'algorithm': buf['algorithm']})
    return entries

# --------------------------- Main App (CustomTkinter) ---------------------------
class HashManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hash Generator v3.0 | Smith Lozano")
        self.geometry("1000x700")
        # default appearance and color theme
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # state
        self.root_tk = self  # use CTk as root for update() calls

        # Tabview container (CTkTabview)
        self.tabview = ctk.CTkTabview(self, width=980, height=640)
        self.tabview.pack(fill="both", expand=True, padx=12, pady=12)

        # Add tabs (names) and get frames via tab()
        tabs = ["Hash Individual", "Hash en Lote", "Comparador", "Verificación de Integridad", "Configuración"]
        for t in tabs:
            self.tabview.add(t)

        # fetch frames
        self.frame_single = self.tabview.tab("Hash Individual")
        self.frame_batch = self.tabview.tab("Hash en Lote")
        self.frame_compare = self.tabview.tab("Comparador")
        self.frame_integrity = self.tabview.tab("Verificación de Integridad")
        self.frame_config = self.tabview.tab("Configuración")

        # Build content in each tab
        self._build_single_tab()
        self._build_batch_tab()
        self._build_compare_tab()
        self._build_integrity_tab()
        self._build_config_tab()

    # ------------------ Tab: Single ------------------
    def _build_single_tab(self):
        parent = self.frame_single

        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=12, pady=8)
        self.single_path_var = tk.StringVar()
        self.single_entry = ctk.CTkEntry(row, textvariable=self.single_path_var)
        self.single_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        btn_browse = ctk.CTkButton(row, text="Seleccionar archivo", command=self.single_browse)
        btn_browse.pack(side="left")

        action_row = ctk.CTkFrame(parent)
        action_row.pack(fill="x", padx=12, pady=(4,8))
        self.single_algo_var = tk.StringVar(value=SUPPORTED_ALGOS[0])
        self.single_algo = ctk.CTkOptionMenu(action_row, values=SUPPORTED_ALGOS, variable=self.single_algo_var)
        self.single_algo.pack(side="left", padx=(0,8))
        self.single_progress = ctk.CTkProgressBar(action_row)
        self.single_progress.set(0.0)
        self.single_progress.pack(side="left", fill="x", expand=True, padx=8)
        btn_hash = ctk.CTkButton(action_row, text="Calcular Hash", command=self.single_hash)
        btn_hash.pack(side="left", padx=(8,4))
        btn_copy = ctk.CTkButton(action_row, text="Copiar", command=self.single_copy)
        btn_copy.pack(side="left")

        out_frame = ctk.CTkFrame(parent)
        out_frame.pack(fill="both", expand=False, padx=12, pady=(4,12))
        ctk.CTkLabel(out_frame, text="Resultado:").pack(anchor="w")
        self.single_out_var = tk.StringVar()
        self.single_out = ctk.CTkEntry(out_frame, textvariable=self.single_out_var, state="readonly")
        self.single_out.pack(fill="x", pady=(4,0))

    def single_browse(self):
        f = filedialog.askopenfilename(title="Seleccionar archivo")
        if f:
            self.single_path_var.set(f)

    def single_hash(self):
        path = self.single_path_var.get().strip()
        if not path or not os.path.isfile(path):
            messagebox.showwarning("Error", "Selecciona un archivo válido")
            return
        algo = self.single_algo_var.get()
        self.single_progress.set(0.0)
        try:
            digest, duration = compute_hash_file_sync(path, algo, lambda p: self.single_progress.set(p/100.0), tk_root=self.root_tk)
            self.single_out_var.set(digest)
            self._append_audit(algo=algo, path_or_text=path, type_='file', size_bytes=os.path.getsize(path), duration=duration, hexdigest=digest)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def single_copy(self):
        v = self.single_out_var.get().strip()
        if v:
            try:
                self.clipboard_clear()
                self.clipboard_append(v)
                messagebox.showinfo("Copiado", "Hash copiado al portapapeles")
            except Exception:
                messagebox.showerror("Error", "No fue posible copiar al portapapeles")

    # ------------------ Tab: Batch ------------------
    def _build_batch_tab(self):
        parent = self.frame_batch

        top = ctk.CTkFrame(parent)
        top.pack(fill="x", padx=12, pady=8)
        btn_add = ctk.CTkButton(top, text="Agregar archivos", command=self.batch_add)
        btn_add.pack(side="left", padx=(0,8))
        btn_clear = ctk.CTkButton(top, text="Limpiar", command=self.batch_clear)
        btn_clear.pack(side="left", padx=(0,8))
        self.batch_algo_var = tk.StringVar(value=SUPPORTED_ALGOS[0])
        batch_algo_menu = ctk.CTkOptionMenu(top, values=SUPPORTED_ALGOS, variable=self.batch_algo_var)
        batch_algo_menu.pack(side="left", padx=(8,8))
        btn_run = ctk.CTkButton(top, text="Calcular Lote", command=self.batch_run)
        btn_run.pack(side="left", padx=(8,0))

        mid = ctk.CTkFrame(parent)
        mid.pack(fill="both", expand=True, padx=12, pady=(4,12))
        left = ctk.CTkFrame(mid)
        left.pack(side="left", fill="y", padx=(0,8))
        ctk.CTkLabel(left, text="Archivos:").pack(anchor="w")
        self.batch_listbox = tk.Listbox(left, selectmode=tk.EXTENDED, width=40)
        self.batch_listbox.pack(fill="y", expand=True, pady=(4,0))

        right = ctk.CTkFrame(mid)
        right.pack(side="left", fill="both", expand=True)
        columns = ("file", "size", "hash", "duration", "export")
        self.batch_tree = ttk.Treeview(right, columns=columns, show="headings")
        for col, w in (("file", 380), ("size", 80), ("hash", 320), ("duration", 80), ("export", 80)):
            self.batch_tree.heading(col, text=col.capitalize())
            self.batch_tree.column(col, width=w, anchor="w")
        self.batch_tree.pack(fill="both", expand=True)
        vsb = ttk.Scrollbar(right, orient="vertical", command=self.batch_tree.yview)
        vsb.pack(side="right", fill="y")
        self.batch_tree.configure(yscrollcommand=vsb.set)

    def batch_add(self):
        files = filedialog.askopenfilenames(title="Seleccionar archivos")
        for f in files:
            self.batch_listbox.insert(tk.END, f)

    def batch_clear(self):
        self.batch_listbox.delete(0, tk.END)
        for iid in self.batch_tree.get_children():
            self.batch_tree.delete(iid)

    def batch_run(self):
        algo = self.batch_algo_var.get()
        items = list(self.batch_listbox.get(0, tk.END))
        if not items:
            messagebox.showwarning("Lista vacía", "Agrega archivos antes")
            return
        for iid in self.batch_tree.get_children():
            self.batch_tree.delete(iid)
        for path in items:
            size = os.path.getsize(path) if os.path.exists(path) else 0
            iid = self.batch_tree.insert("", "end", values=(path, str(size), "Procesando...", "-", ""))
            def progress_cb(pct, row_iid=iid):
                try:
                    self.batch_tree.set(row_iid, column="hash", value=f"{pct}% - procesando")
                except Exception:
                    pass
            try:
                digest, duration = compute_hash_file_sync(path, algo, lambda p: progress_cb(p), tk_root=self.root_tk)
                self.batch_tree.set(iid, column="hash", value=digest)
                self.batch_tree.set(iid, column="duration", value=f"{duration:.3f}")
                self._append_audit(algo, path, 'file', size, duration, digest)
            except Exception as e:
                self.batch_tree.set(iid, column="hash", value="ERROR:"+str(e))

    # ------------------ Tab: Compare ------------------
    def _build_compare_tab(self):
        parent = self.frame_compare

        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=12, pady=8)
        self.cmp_a_var = tk.StringVar()
        self.cmp_b_var = tk.StringVar()
        entry_a = ctk.CTkEntry(row, textvariable=self.cmp_a_var)
        entry_a.pack(side="left", fill="x", expand=True, padx=(0,8))
        btn_a = ctk.CTkButton(row, text="Seleccionar A (archivo)", command=lambda: self._select_file(self.cmp_a_var))
        btn_a.pack(side="left", padx=(0,8))
        entry_b = ctk.CTkEntry(row, textvariable=self.cmp_b_var)
        entry_b.pack(side="left", fill="x", expand=True, padx=(8,8))
        btn_b = ctk.CTkButton(row, text="Seleccionar B (archivo)", command=lambda: self._select_file(self.cmp_b_var))
        btn_b.pack(side="left")

        hint = ctk.CTkLabel(parent, text="Nota: puedes pegar un hash en el campo B para compararlo con A.")
        hint.pack(anchor="w", padx=12)

        algo_row = ctk.CTkFrame(parent)
        algo_row.pack(fill="x", padx=12, pady=(8,4))
        self.cmp_algo_var = tk.StringVar(value=SUPPORTED_ALGOS[0])
        self.cmp_algo = ctk.CTkOptionMenu(algo_row, values=SUPPORTED_ALGOS, variable=self.cmp_algo_var)
        self.cmp_algo.pack(side="left", padx=(0,8))
        btn_cmp = ctk.CTkButton(algo_row, text="Comparar", command=self.compare_files)
        btn_cmp.pack(side="left")

        self.cmp_result_var = tk.StringVar(value="")
        self.cmp_result_lbl = ctk.CTkLabel(parent, textvariable=self.cmp_result_var, wraplength=900, anchor="w", justify="left")
        self.cmp_result_lbl.pack(fill="x", padx=12, pady=(8,4))

    def _select_file(self, var: tk.StringVar):
        f = filedialog.askopenfilename(title="Seleccionar archivo")
        if f:
            var.set(f)

    def compare_files(self):
        a = self.cmp_a_var.get().strip(); b = self.cmp_b_var.get().strip()
        if not a:
            messagebox.showwarning("Error", "Campo A vacío")
            return
        algo = self.cmp_algo_var.get()
        if os.path.isfile(a):
            ha = self._compute_sync(a, algo)
            if ha is None:
                messagebox.showerror("Error", "No se pudo calcular hash de A")
                return
        else:
            messagebox.showwarning("Error", "Campo A debe ser un archivo válido")
            return

        if os.path.isfile(b):
            hb = self._compute_sync(b, algo)
            if hb is None:
                messagebox.showerror("Error", "No se pudo calcular hash de B")
                return
            source_b = f'file: {b}'
        elif b and all(c in '0123456789abcdefABCDEF' for c in b) and len(b) >= 8:
            hb = b.lower()
            source_b = 'raw hash'
        else:
            messagebox.showwarning("Error", "Campo B debe ser un archivo válido o un hash hexadecimal")
            return

        if ha == hb:
            self.cmp_result_var.set(f'COINCIDENCIA — A hash: {ha} — B ({source_b}) matches')
        else:
            self.cmp_result_var.set(f'DISTINTO — A: {ha} — B ({source_b}): {hb}')

    def _compute_sync(self, path: str, algo: str) -> Optional[str]:
        try:
            digest, _ = compute_hash_file_sync(path, algo, tk_root=self.root_tk)
            return digest
        except Exception:
            return None

    # ------------------ Tab: Integrity ------------------
    def _build_integrity_tab(self):
        parent = self.frame_integrity

        row1 = ctk.CTkFrame(parent)
        row1.pack(fill="x", padx=12, pady=8)
        self.manifest_path_var = tk.StringVar()
        manifest_entry = ctk.CTkEntry(row1, textvariable=self.manifest_path_var)
        manifest_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        btn_manifest = ctk.CTkButton(row1, text="Cargar manifest", command=self.load_manifest)
        btn_manifest.pack(side="left")

        row2 = ctk.CTkFrame(parent)
        row2.pack(fill="x", padx=12, pady=(4,8))
        self.folder_path_var = tk.StringVar()
        folder_entry = ctk.CTkEntry(row2, textvariable=self.folder_path_var)
        folder_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        btn_folder = ctk.CTkButton(row2, text="Seleccionar carpeta", command=self.select_folder)
        btn_folder.pack(side="left")

        algo_row = ctk.CTkFrame(parent)
        algo_row.pack(fill="x", padx=12, pady=(4,8))
        self.integrity_algo_var = tk.StringVar(value=SUPPORTED_ALGOS[0])
        integrity_algo_menu = ctk.CTkOptionMenu(algo_row, values=SUPPORTED_ALGOS, variable=self.integrity_algo_var)
        integrity_algo_menu.pack(side="left", padx=(0,8))
        btn_verify = ctk.CTkButton(algo_row, text="Verificar contra manifest", command=self.verify_manifest)
        btn_verify.pack(side="left", padx=(0,8))
        btn_create = ctk.CTkButton(algo_row, text="Crear manifest desde carpeta", command=self.create_manifest_from_folder)
        btn_create.pack(side="left")

        self.integrity_out = tk.Text(parent, height=18)
        self.integrity_out.pack(fill="both", expand=True, padx=12, pady=(8,12))

    def load_manifest(self):
        f = filedialog.askopenfilename(title="Cargar manifest (CSV, JSON o TXT)", filetypes=[("CSV Files","*.csv"),("JSON Files","*.json"),("TXT Files","*.txt"),("All files","*.*")])
        if f:
            self.manifest_path_var.set(f)

    def select_folder(self):
        d = filedialog.askdirectory(title="Seleccionar carpeta")
        if d:
            self.folder_path_var.set(d)

    def create_manifest_from_folder(self):
        folder = self.folder_path_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Error", "Selecciona una carpeta válida")
            return
        algo = self.integrity_algo_var.get()
        manifest = []
        for root, _, files in os.walk(folder):
            for name in files:
                p = os.path.join(root, name)
                h = self._compute_sync(p, algo)
                size = os.path.getsize(p)
                manifest.append({'path': os.path.relpath(p, folder), 'hash': h, 'size': size, 'algorithm': algo})

        default_name = f"manifest_{safe_timestamp()}"
        f = filedialog.asksaveasfilename(title="Guardar manifest", initialfile=f"{default_name}.json", defaultextension=".json",
                                         filetypes=[("JSON Files","*.json"), ("CSV Files","*.csv"), ("TXT Files","*.txt"), ("All files","*.*")])
        if not f:
            return
        lower = f.lower()
        if lower.endswith('.json'):
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump({'algorithm': algo, 'base_folder': folder, 'files': manifest}, fh, ensure_ascii=False, indent=2)
        elif lower.endswith('.csv'):
            with open(f, 'w', encoding='utf-8', newline='') as fh:
                writer = csv.DictWriter(fh, fieldnames=['path','hash','size','algorithm'])
                writer.writeheader()
                for it in manifest:
                    writer.writerow({'path': it.get('path',''), 'hash': it.get('hash',''), 'size': it.get('size',0), 'algorithm': it.get('algorithm','')})
        else:
            entries_for_txt = [{'file': it.get('path',''), 'hash': it.get('hash',''), 'algorithm': it.get('algorithm','')} for it in manifest]
            export_manifest_txt(entries_for_txt, f)

        messagebox.showinfo("Manifest creado", f"Manifest guardado en {f}")

    def verify_manifest(self):
        manifest_file = self.manifest_path_var.get().strip(); folder = self.folder_path_var.get().strip()
        if not manifest_file or not os.path.exists(manifest_file):
            messagebox.showwarning("Error", "Carga un manifest válido")
            return

        data = None
        files_entries = []
        algo_declared = None
        if manifest_file.lower().endswith('.json'):
            with open(manifest_file, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                files_entries = data.get('files', [])
                algo_declared = data.get('algorithm')
            elif isinstance(data, list):
                files_entries = data
        elif manifest_file.lower().endswith('.csv'):
            rows = []
            with open(manifest_file, 'r', encoding='utf-8') as fh:
                r = csv.DictReader(fh)
                for row in r:
                    rows.append(row)
            files_entries = rows
            algo_declared = rows[0].get('algorithm') if rows else None
        elif manifest_file.lower().endswith('.txt'):
            parsed = parse_manifest_txt(manifest_file)
            files_entries = parsed
        else:
            messagebox.showwarning("Error", "Formato de manifest no soportado (usa JSON, CSV o TXT)")
            return

        algo = algo_declared or self.integrity_algo_var.get()
        base = None
        if isinstance(data, dict):
            base = data.get('base_folder') or folder
        base = base or folder or os.path.dirname(manifest_file)

        issues = []
        out_lines = []
        for entry in files_entries:
            rel = entry.get('path') or entry.get('file') or entry.get('relative_path') or entry.get('file_path') or entry.get('0')
            expected = entry.get('hash') or entry.get('checksum')
            entry_algo = entry.get('algorithm') or entry.get('alg')
            use_algo = entry_algo or algo
            if rel is None:
                continue
            path = os.path.join(base, rel)
            if not os.path.exists(path):
                issues.append((rel, 'MISSING', ''))
                out_lines.append(f'{rel} - MISSING')
                continue
            actual = self._compute_sync(path, use_algo)
            if actual != expected:
                issues.append((rel, 'MISMATCH', actual))
                out_lines.append(f'{rel} - MISMATCH (expected {expected}, got {actual})')
            else:
                out_lines.append(f'{rel} - OK')
        self.integrity_out.delete("1.0", tk.END)
        self.integrity_out.insert(tk.END, "\n".join(out_lines))
        messagebox.showinfo("Verificación finalizada", f"Encontradas {len(issues)} discrepancias")

    # ------------------ Tab: Config ------------------
    def _build_config_tab(self):
        parent = self.frame_config

        ctk.CTkLabel(parent, text="Apariencia:").pack(anchor="w", padx=12, pady=(12,2))
        # Only Light / Dark options as requested
        self.appearance_var = tk.StringVar(value="Light")
        appearance_options = ["Light", "Dark"]
        self.appearance_menu = ctk.CTkOptionMenu(parent, values=appearance_options, variable=self.appearance_var, command=self._on_change_appearance)
        self.appearance_menu.pack(anchor="w", padx=12)

        ctk.CTkLabel(parent, text="Exportación avanzada: formato por defecto al exportar lote").pack(anchor="w", padx=12, pady=(8,2))
        self.export_format_var = tk.StringVar(value="TXT")
        rb_frame = ctk.CTkFrame(parent)
        rb_frame.pack(anchor="w", padx=12, pady=(4,8))
        for opt in ("TXT","CSV","JSON"):
            rb = ctk.CTkRadioButton(rb_frame, text=opt, variable=self.export_format_var, value=opt)
            rb.pack(side="left", padx=6)

        btn_export_now = ctk.CTkButton(parent, text="Exportar tabla de lote ahora", command=self.export_batch_table)
        btn_export_now.pack(padx=12, pady=(8,12))

    def _on_change_appearance(self, value: str):
        """Apply appearance mode: Light / Dark"""
        try:
            if value == "Light":
                ctk.set_appearance_mode("Light")
            else:
                ctk.set_appearance_mode("Dark")
        except Exception as e:
            # fallback
            try:
                ctk.set_appearance_mode(value)
            except Exception:
                print("Error aplicando apariencia:", e)

    # ------------------ Utilities ------------------
    def _append_audit(self, algo, path_or_text, type_, size_bytes, duration, hexdigest):
        with open(AUDIT_CSV, 'a', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow([ts(), algo, path_or_text.replace('\n',' '), type_, size_bytes, f'{duration:.6f}', hexdigest])

    def export_batch_table(self):
        items = []
        for iid in self.batch_tree.get_children():
            vals = self.batch_tree.item(iid, 'values')
            # vals expected: (file, size, hash, duration, export)
            file_path = vals[0] if len(vals) > 0 else ""
            size = vals[1] if len(vals) > 1 else ""
            hashv = vals[2] if len(vals) > 2 else ""
            duration = vals[3] if len(vals) > 3 else ""
            items.append({'file': file_path, 'size': size, 'hash': hashv, 'duration': duration, 'algorithm': self.batch_algo_var.get()})

        if not items:
            messagebox.showwarning("Vacío", "No hay datos en la tabla de lote")
            return

        fmt = self.export_format_var.get()
        default_name = f"batch_export_{safe_timestamp()}"

        f = filedialog.asksaveasfilename(title="Guardar export", initialfile=f"{default_name}.{fmt.lower()}",
                                         defaultextension=f".{fmt.lower()}",
                                         filetypes=[("TXT Files","*.txt"),("CSV Files","*.csv"),("JSON Files","*.json"),("All files","*.*")])
        if not f:
            return
        lower = f.lower()
        try:
            if fmt == "TXT" or lower.endswith('.txt'):
                # use detailed TXT exporter
                algo_used = self.batch_algo_var.get()
                export_batch_txt_detailed(items, f, algo_declared=algo_used)
            elif fmt == "CSV" or lower.endswith('.csv'):
                with open(f, 'w', encoding='utf-8', newline='') as fh:
                    writer = csv.DictWriter(fh, fieldnames=['file','size','hash','duration','algorithm'])
                    writer.writeheader()
                    writer.writerows(items)
            else:
                # JSON
                with open(f, 'w', encoding='utf-8') as fh:
                    json.dump(items, fh, ensure_ascii=False, indent=2)
            messagebox.showinfo("Exportado", f"Exportado a {f}")
        except Exception as e:
            messagebox.showerror("Error exportando", str(e))

# --------------------------- Run ---------------------------
def main():
    app = HashManagerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
