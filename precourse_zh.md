# Pre-Orientation: Data Analytics in Astronomy
**中文：** 课前说明：天文学中的数据分析

Welcome, Astronomers! We're thrilled you'll be joining our **Data Analytics in Astronomy** training. This short guide provides essential information to help you prepare for the course and ensure you have a smooth start.

**中文：** 欢迎各位天文学学习者！很高兴你将参加我们的 **Data Analytics in Astronomy** 培训。本简短指南提供关键信息，帮助你在开课前做好准备，并顺利开始学习。

---

## 1. Course Introduction
**中文：** 1. 课程介绍

This training is designed to equip you with the foundational Python programming skills necessary to tackle common tasks in astronomy. We'll move from the absolute basics of programming to applying Python concepts to analyze astronomical data, automate calculations, and understand how code can be a powerful tool in your scientific journey.

**中文：** 本次培训旨在帮助你掌握 Python 编程的基础技能，用于完成天文学中的常见任务。我们将从编程的最基础内容开始，逐步把 Python 概念用于天文数据分析、自动化计算，并理解代码如何成为你科研旅程中的强大工具。

Our focus will be on practical application, using relatable examples drawn from astronomy wherever possible. We aim to create a supportive learning environment where questions are encouraged. By the end of this course, you'll have a solid base to build upon and the confidence to start using Python in your own astronomical projects.

**中文：** 我们将重点强调实践应用，并尽可能使用来自天文学的例子。我们希望营造一个支持性的学习环境，鼓励大家提出问题。课程结束时，你将拥有扎实的基础，并有信心在自己的天文项目中开始使用 Python。

---

## 2. Target Audience & Prerequisites
**中文：** 2. 目标人群与先修要求

*   **Primary Audience:** Undergraduate students, researchers, or enthusiasts in astronomy (or related fields) who are **new to programming** or have very limited prior experience with Python.
    **中文：** **主要对象：** 天文学（或相关领域）的本科生、研究人员或爱好者，**刚开始学习编程**或只有很少的 Python 经验。
*   **Programming Level:** **Beginner**. No prior programming knowledge is required. We will start from the ground up.
    **中文：** **编程水平：** **初学者**。不要求任何编程基础。我们将从零开始。
*   **Astronomy Level:** A basic interest or background in astronomy is helpful for understanding the examples, but advanced astronomical knowledge is **not** required.
    **中文：** **天文学水平：** 具备基本兴趣或背景有助于理解例子，但**不要求**高级天文学知识。
*   **Technical Requirements:** Access to a computer (Windows, macOS, or Linux) with internet access and the ability to install software (see Section 4).
    **中文：** **技术要求：** 可使用一台计算机（Windows、macOS 或 Linux），能联网并能安装软件（见第 4 节）。

---

## 3. Course Objectives
**中文：** 3. 课程目标

Upon successful completion of this training, you will be able to:

**中文：** 完成本次培训后，你将能够：

*   Understand fundamental programming concepts (variables, data types, operators).
    **中文：** 理解基本编程概念（变量、数据类型、运算符）。
*   Write and execute basic Python scripts.
    **中文：** 编写并运行基础的 Python 脚本。
*   Implement control flow using loops (`for`, `while`) and conditional statements (`if`, `else`).
    **中文：** 使用循环（`for`、`while`）与条件语句（`if`、`else`）实现控制流程。
*   Define and use functions to create reusable and modular code.
    **中文：** 定义并使用函数，编写可复用、模块化的代码。

*   Read data from and write data to files.
    **中文：** 从文件读取数据，并将数据写入文件。
*   Implement basic error handling using `try...except` blocks.
    **中文：** 使用 `try...except` 代码块实现基础错误处理。
*   Import and utilize standard Python modules (like `math`, `time`).
    **中文：** 导入并使用标准 Python 模块（如 `math`、`time`）。
*   Understand the concept of packages and install external packages (like `numpy`, `pandas`, `astropy` and other packages) using `pip` or `conda`.
    **中文：** 理解包（package）的概念，并使用 `pip` 或 `conda` 安装外部包（如 `numpy`、`pandas`、`astropy` 等）。
*   Apply these Python concepts to solve simple problems relevant to astronomy.
    **中文：** 将这些 Python 概念用于解决与天文学相关的简单问题。

---


## 4. Installation Guidelines: Setting Up Your Environment
**中文：** 4. 安装指南：搭建你的环境

To participate fully in the hands-on exercises, you must install the necessary software before the first session. We strongly recommend using the **Anaconda Distribution**, as it simplifies the installation of Python and many essential scientific packages.

**中文：** 为了顺利完成动手练习，你需要在第一次课程开始前安装必要的软件。我们强烈建议使用 **Anaconda Distribution**，因为它能简化 Python 以及常用科学计算包的安装。

**Steps:**

**中文：** **步骤：**

1.  **Download Anaconda:**
    **中文：** **下载 Anaconda：**
    *   Go to the official Anaconda Distribution download page: [https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)
        **中文：** 进入 Anaconda Distribution 官方下载页面：[https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)
    *   Download the installer appropriate for your operating system (Windows, macOS, or Linux). Choose the Python 3.x version (the latest is recommended).
        **中文：** 下载适用于你操作系统（Windows、macOS 或 Linux）的安装包。选择 Python 3.x 版本（建议使用最新版）。

2.  **Install Anaconda:**
    **中文：** **安装 Anaconda：**
    *   Locate the downloaded installer file.
        **中文：** 找到已下载的安装包文件。
    *   Double-click the installer and follow the on-screen instructions.
        **中文：** 双击安装包并按屏幕提示完成安装。
    *   **Recommendation:** Unless you have a specific reason not to, we recommend accepting the default settings during installation. This usually includes adding Anaconda to your system's PATH environment variable (though the installer might advise against it for Windows, it often simplifies things for beginners – follow the installer's recommendation if unsure).
        **中文：** **建议：** 如果没有明确原因，我们建议在安装时使用默认设置。这通常包括将 Anaconda 加入系统的 PATH 环境变量（虽然在 Windows 上安装器可能不建议这样做，但对初学者往往更方便——不确定时请遵循安装器的建议）。

3.  **Verify Installation:**
    **中文：** **验证安装：**
    *   **Option A (Anaconda Navigator):** After installation, search for and open "Anaconda Navigator". This is a graphical interface. From Navigator, you should be able to launch "Jupyter Notebook". If Jupyter Notebook launches in your web browser, your installation is likely successful.
        **中文：** **选项 A（Anaconda Navigator）：** 安装完成后，搜索并打开 “Anaconda Navigator”。这是一个图形界面。在 Navigator 中，你应该可以启动 “Jupyter Notebook”。如果 Jupyter Notebook 能在浏览器中打开，说明安装大概率成功。
    *   **Option B (Terminal/Command Prompt):**
        **中文：** **选项 B（终端/命令提示符）：**
        *   Open your Terminal (macOS/Linux) or Command Prompt/Anaconda Prompt (Windows).
            **中文：** 打开终端（macOS/Linux）或命令提示符/Anaconda Prompt（Windows）。
        *   Type `python --version` and press Enter. You should see a Python version corresponding to the Anaconda installation (e.g., `Python 3.9.7`).
            **中文：** 输入 `python --version` 并回车。你应看到与 Anaconda 安装对应的 Python 版本（例如 `Python 3.9.7`）。
        *   Type `conda list anaconda$` and press Enter. This checks if the core Anaconda package is installed.
            **中文：** 输入 `conda list anaconda$` 并回车。该命令用于检查是否安装了核心 Anaconda 包。
        *   Type `jupyter lab` and press Enter. This should launch Jupyter Notebook in your web browser.
            **中文：** 输入 `jupyter lab` 并回车。这会在浏览器中启动 Jupyter Notebook。

4.  **Troubleshooting:**
    **中文：** **排错：**
    *   Installation issues are common, especially with path configurations.
        **中文：** 安装问题很常见，尤其是与路径（path）配置相关的问题。
    *   Refer to the official Anaconda documentation for detailed installation guides and troubleshooting tips: [https://docs.anaconda.com/anaconda/install/](https://docs.anaconda.com/anaconda/install/)
        **中文：** 参考 Anaconda 官方文档，获取更详细的安装指南与排错建议：[https://docs.anaconda.com/anaconda/install/](https://docs.anaconda.com/anaconda/install/)
    *   If you encounter persistent problems, please reach out using the contact information provided in Section 6 before the first training session.
        **中文：** 如果问题持续存在，请在第一次课程开始前，使用第 6 节提供的联系方式与我们联系。

---

## 6. Pre-Course Preparation (Optional)
**中文：** 6. 课前准备（可选）

While not mandatory, you might find it helpful to:

**中文：** 虽然不是必须，但你可能会觉得以下准备有帮助：

*   Familiarize yourself with your computer's file system (how to create folders, find files).
    **中文：** 熟悉你电脑的文件系统（如何创建文件夹、如何查找文件）。
*   Briefly browse a very basic Python tutorial online (e.g., the first few sections of the official Python tutorial at [https://docs.python.org/3/tutorial/](https://docs.python.org/3/tutorial/)) just to get a feel for the syntax, but don't worry if it doesn't all make sense – we will cover it!
    **中文：** 简单浏览一个入门级 Python 教程（例如 Python 官方教程的前几节：[https://docs.python.org/3/tutorial/](https://docs.python.org/3/tutorial/)），先熟悉一下语法即可。不用担心看不懂——我们会在课程中讲到！

---

## 7. Contact & Support (Pre-Course)
**中文：** 7. 联系与支持（课前）

If you face difficulties with the software installation or have urgent questions before the training begins, please contact us at through the Slack channel.

**中文：** 如果你在软件安装上遇到困难，或在开课前有紧急问题，请通过 Slack 频道联系我们。

Please try to resolve installation issues *before* the first session so we can dive right into the material.

**中文：** 请尽量在第一次课程开始前解决安装问题，这样我们就能直接进入学习内容。

---

We are looking forward to exploring the universe of Python with you! Get ready for an exciting journey into astronomical programming.

**中文：** 期待与你一起探索 Python 的宇宙！准备好开启一段精彩的天文编程之旅吧。

