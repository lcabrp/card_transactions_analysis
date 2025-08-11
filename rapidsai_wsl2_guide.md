
---

## **1. What is RAPIDS AI?**

RAPIDS AI is an open-source suite of GPU-accelerated Python libraries for data science, analytics, and machine learning.
Think of it as **Pandas + scikit-learn + NetworkX** — but running **entirely on your GPU**, often **10x–100x faster** for large datasets.

Core packages include:

* **cuDF** – GPU-accelerated DataFrames (Pandas-like)
* **cuML** – GPU-accelerated ML algorithms (scikit-learn-like)
* **cuGraph** – GPU-accelerated graph analytics

---

## **2. Why conda (and not `uv` or plain `pip`)**

* **GPU libraries require binary compatibility** between the installed CUDA toolkit, the driver, and the compiled RAPIDS binaries.
* Conda ensures all dependencies (CUDA runtime, cuDF, cuML, etc.) are version-matched without manual `.so` / `.dll` headaches.
* `pip` can work but is more fragile — RAPIDS conda packages come with prebuilt CUDA-compatible binaries.
* `uv` is great for pure Python, but RAPIDS has large compiled CUDA/C++ code — so conda is the safe choice.

---

## **3. Prerequisites**

On **Windows**:

1. Install the latest **NVIDIA GPU driver** (Game Ready or Studio) from [NVIDIA](https://www.nvidia.com/Download/index.aspx).

   * You don’t need to install CUDA separately — just the driver.

On **WSL2 (Ubuntu)**:

```bash
# Make sure your system is up to date
sudo apt update && sudo apt upgrade -y

# Install basic tools
sudo apt install -y build-essential git curl wget

# Remove apt-installed CUDA toolkit (if installed)
sudo apt remove --purge nvidia-cuda-toolkit -y
sudo apt autoremove -y
```

---

## **4. Installing Miniconda in WSL2**

```bash
# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Restart shell so conda is available
source ~/.bashrc
```

---

## **5. Creating a RAPIDS AI Environment**

Check the [RAPIDS AI version matrix](https://docs.rapids.ai/install) for the CUDA version matching your GPU driver.
For most modern GPUs with latest drivers → `cudatoolkit=12.0` works.

```bash
# Create RAPIDS 24.06 environment with Python 3.10
conda create -n rapids-24.06 -c rapidsai -c conda-forge \
    cudf=24.06 python=3.10 cudatoolkit=12.0
conda activate rapids-24.06
```

**Why Python 3.10?**

* RAPIDS 24.06 doesn’t yet support Python 3.12.
* 3.11 support is coming in later releases (check the matrix for updates).

---

## **6. Testing GPU Access**

```bash
python -c "import cudf; import cupy; print(cudf.Series([1,2,3]).to_gpu_array())"
```

If no errors appear and it prints a CuPy array, your GPU is being used.

---

## **7. Using RAPIDS AI in VS Code (Windows + WSL2)**

1. In Windows, install **Visual Studio Code** and the **Remote - WSL** extension.
2. Open VS Code → Press `F1` → type `Remote-WSL: New Window`.
3. Open your WSL2 workspace folder.
4. In the integrated terminal:

   ```bash
   conda activate rapids-24.06
   ```
5. Install the Jupyter extension in VS Code (in WSL).
6. When creating a notebook, select **Kernel → rapids-24.06**.

---

## **8. Adapting for Other GPUs**

* **T1200 / A1000 / 4060 Laptop**: All are CUDA-capable. As long as you have the **latest NVIDIA driver** and WSL2 is set up, the same process works.
* The main variable is **CUDA version compatibility** — always check [RAPIDS compatibility table](https://docs.rapids.ai/install) before creating the environment.

---

## **9. Common Issues**

* **Plotly map vs scattermap issue**: Sometimes due to older Plotly in conda channels — you can upgrade inside the environment:

  ```bash
  pip install --upgrade plotly
  ```
* **"CUDA driver version is insufficient"** → Update Windows NVIDIA driver.
* **"No CUDA-capable device detected"** → Make sure WSL GPU support is enabled:

  ```bash
  nvidia-smi
  ```

---

If you want, I can **extend this guide** into a single Markdown file you can drop into each laptop as your official **RAPIDS WSL2 Setup Blueprint** — with **GPU detection checks, environment verification, and driver version notes**.
That way, you just tweak the CUDA/Python versions per laptop.

Do you want me to prepare that portable blueprint next?

---

## **RAPIDS on WSL2 – Complete Guide (Blueprint)**

### 1️⃣ **What is RAPIDS?**

RAPIDS is a suite of open-source GPU-accelerated libraries for data science, machine learning, and analytics (think of it as "Pandas + Scikit-learn, but on GPU").

* **`cudf`** – Pandas-like DataFrame library on GPU.
* **`cuml`** – GPU-accelerated ML algorithms.
* **`cugraph`** – Graph analytics on GPU.
* **`cupy`** – NumPy on GPU.

It’s **built on CUDA**, so you need the correct **NVIDIA drivers** and **CUDA toolkit support**.

---

### 2️⃣ **Why WSL2?**

* Lets you run full Linux environments on Windows without dual boot.
* You can use NVIDIA GPU acceleration from Linux apps in WSL2.
* Good for using Linux-first tools (like RAPIDS) while keeping Windows for other tasks.

---

### 3️⃣ **Why Conda and Not uv/pip?**

* **RAPIDS packages depend on CUDA versions** and binary builds optimized for GPU — these are tricky to install via pip/uv without conflicts.
* Conda handles:

  * Matching `cudatoolkit` to your GPU driver.
  * Precompiled binaries for GPU libraries.
  * Environment isolation.
* Pip/uv would require manual compilation or prebuilt wheels that may not match your GPU/CUDA version.

---

### 4️⃣ **Prerequisites**

#### In **Windows**:

1. **Update NVIDIA Driver**

   * Install the latest Game Ready or Studio driver from [NVIDIA Driver Downloads](https://www.nvidia.com/Download/index.aspx).
   * Ensure it supports **CUDA 12.0 or later**.
   * On your laptop:

     ```powershell
     nvidia-smi
     ```

     This should show CUDA version compatibility.

2. **Enable WSL2 and Install Ubuntu**

   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

   Reboot if prompted.

3. **Check GPU access in WSL**
   Inside Ubuntu:

   ```bash
   nvidia-smi
   ```

---

### 5️⃣ **Installing RAPIDS in WSL2 with Conda**

1. **Install Miniconda (lightweight Conda)**

   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   source ~/.bashrc
   ```

2. **Create RAPIDS environment**
   This example uses RAPIDS 24.06 (CUDA 12.0, Python 3.10):

   ```bash
   conda create -n rapids-24.06 -c rapidsai -c conda-forge \
       cudf=24.06 python=3.10 cudatoolkit=12.0
   conda activate rapids-24.06
   ```

   🔹 *If newer Python is available*, check with:

   ```bash
   conda search cudf --channel rapidsai
   ```

3. **Install extra packages** (optional, e.g., Plotly, Jupyter):

   ```bash
   conda install -c conda-forge plotly jupyterlab
   ```

---

### 6️⃣ **Using RAPIDS with VS Code**

1. Install **VS Code** on Windows.
2. Install the **Remote - WSL** extension.
3. Open VS Code → Press `F1` → *Remote-WSL: Connect to WSL*.
4. Open your RAPIDS project folder from WSL.
5. Select the `rapids-24.06` kernel in VS Code for notebooks:

   * Open a `.ipynb` file → Click kernel dropdown → Choose `rapids-24.06`.

---

### 7️⃣ **Verification**

Run inside your environment:

```python
import cudf
import cupy
import cuml
print(cudf.__version__)
```

You should see `24.06` and no errors.

---

### 8️⃣ **GPU-Specific Notes**

* **T1200 / A1000 / RTX 4060 Laptop**:

  * All support CUDA 12.x, so this guide works unchanged.
  * Just ensure you **match cudatoolkit version** to your NVIDIA driver.
* If a laptop has older GPU architecture, you may need to install a matching RAPIDS version (check `rapidsai` release notes).

---


