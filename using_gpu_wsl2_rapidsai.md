Alright — here’s the clean, step-by-step way to get **VS Code on Windows** working with your **RAPIDS GPU environment inside WSL2** so you can run GPU-accelerated Python scripts directly.

---

## **1️⃣ Install VS Code WSL Extension**

1. Open **VS Code** on Windows.
2. Go to the **Extensions** view (`Ctrl+Shift+X`).
3. Search for **Remote - WSL** and install it.

   * Publisher: *Microsoft*
   * This lets VS Code open a folder *inside* your WSL2 distro.

---

## **2️⃣ Open VS Code in WSL Mode**

1. In Windows **Command Prompt** or **PowerShell**, run:

   ```powershell
   wsl
   ```

   This drops you into your WSL2 shell.
2. Navigate to your project folder in WSL2. Example:

   ```bash
   cd ~/projects/rapids-tests
   ```
3. Open VS Code from inside WSL:

   ```bash
   code .
   ```

   * This launches VS Code **attached to your WSL2 environment**.
   * You should see `WSL: <YourDistro>` in the **green status bar** at the bottom left.

---

## **3️⃣ Select the RAPIDS Conda Environment as the Interpreter**

1. Press `Ctrl+Shift+P` → search for **"Python: Select Interpreter"**.
2. In the list, find the path to your RAPIDS environment:

   ```
   /home/<youruser>/miniconda3/envs/rapids-24.06/bin/python
   ```

   Select it.
3. VS Code will now use your GPU-enabled Python for:

   * Python scripts (`.py`)
   * Jupyter notebooks (`.ipynb`)

---

## **4️⃣ Test GPU from VS Code**

1. Create a file called `gpu_test.py` with:

   ```python
   import cudf
   import cupy as cp
   from numba import cuda

   print("cuDF version:", cudf.__version__)
   print("cuPy version:", cp.__version__)
   print("GPU count:", len(cuda.gpus))
   if cuda.gpus:
       print("GPU name:", cuda.get_current_device().name)
   ```
2. Run it in VS Code:

   * Open **Terminal** (\`Ctrl+\`\`) in VS Code.
   * Make sure the terminal says `(rapids-24.06)` at the start.
   * Run:

     ```bash
     python gpu_test.py
     ```
3. If all is good, you’ll see your **RTX 2000 Ada** GPU detected.

---

## **5️⃣ Optional – Jupyter Notebooks in VS Code**

If you want to run notebooks in VS Code:

```bash
conda activate rapids-24.06
python -m ipykernel install --user --name=rapids-24.06 --display-name "Python (RAPIDS GPU)"
```

* Then, when you open a `.ipynb` in VS Code, select the **"Python (RAPIDS GPU)"** kernel.

---

If you follow these steps, every script or notebook you run from VS Code in WSL will be **GPU-accelerated by default** — no more CUDA errors.

---

## RAPIDS in WSL2: Why We Do It This Way

**RAPIDS** is a suite of GPU-accelerated data processing libraries (like cuDF, cuML) that bring pandas-like APIs to NVIDIA GPUs. WSL2 enables you to access Windows GPUs from Linux environments without dual-booting or full-fledged VMs.

Per NVIDIA’s updated guidance (after v22.02):

1. Install the **latest WSL2-capable NVIDIA driver on Windows**
2. Don’t install Linux GPU drivers inside WSL—WSL uses the Windows driver to handle GPU access.
3. Inside WSL2, install RAPIDS (via Conda or Docker); CUDA toolkit is included in RAPIDS packages. ([RAPIDS Docs][1], [NVIDIA Docs][2])

---

## Setting Up RAPIDS with Conda in WSL2

### Step-by-Step Install

```bash
# 1. Inside WSL2, install Miniforge (Conda)
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
# Reset or open a new shell after installation.

# 2. Create your RAPIDS 24.06 environment
conda create -n rapids-24.06 -c rapidsai -c conda-forge -c nvidia \
    rapids=24.06 python=3.10

# 3. Activate it
conda activate rapids-24.06
```

* **Why Conda?**
  It ensures the correct CUDA toolkit version matches the driver, and packages (cuDF, cuML, cuGraph) are pre-built for compatibility. Conda avoids conflicting system installs, unlike `apt` ([RAPIDS Docs][1]).

* Python version: RAPIDS supports up to 3.10 (currently). If you need newer, you’ll see package conflicts like with Plotly; unfortunately RAPIDS hasn’t released builds for 3.11+ yet.

---

## Using RAPIDS GPU inside VS Code (Windows → WSL2)

1. **Install** the **Remote - WSL** extension in Windows VS Code.
2. Open your WSL2 project directory via `wsl` shell:

   ```bash
   cd ~/projects/card_transactions_analysis
   code .
   ```
3. In VS Code status bar, confirm you're connected to WSL.
4. Press `Ctrl+Shift+P` → **Python: Select Interpreter** → choose:

   ```
   rapids-24.06 (/home/…/miniconda3/envs/rapids-24.06/bin/python)
   ```
5. Test GPU access:

   ```python
   import cudf, cupy as cp
   print(cp.cuda.runtime.getDeviceCount())
   print(cp.cuda.runtime.getDeviceProperties(0)['name'])
   ```
6. For Jupyter notebooks:

   ```bash
   python -m ipykernel install --user --name=rapids-24.06 --display-name "Python (RAPIDS GPU)"
   ```

Now all notebook and script executions in VS Code will run through your WSL2 GPU environment.

---

## Recap of Key Takeaways

* **No need** for `apt` CUDA or Linux driver installs inside WSL—these cause conflicts.
* Use **Conda** to manage RAPIDS dependencies and CUDA toolkit versions.
* **VS Code Remote-WSL** allows seamless editing and GPU-powered execution from Windows.

---


[1]: https://docs.rapids.ai/notices/rgn0024/?utm_source=chatgpt.com "Updated WSL2 Installation Method - RAPIDS Docs"
[2]: https://docs.nvidia.com/cuda/wsl-user-guide/index.html?utm_source=chatgpt.com "CUDA on WSL User Guide"
