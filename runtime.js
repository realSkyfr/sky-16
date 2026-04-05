// Import your Python files as strings at the very top
import assemblerSource from "./assembler.py?raw";
import emulatorSource from "./emulator.py?raw";
import runtimeSource from "./webruntime.py?raw";

let pyodide;

async function init() {
  const startBtn = document.getElementById("start");
  const outElement = document.getElementById("stdout");

  outElement.value = "Initializing Environment...";
  startBtn.disabled = true;

  try {
    // 1. Load the engine
    pyodide = await loadPyodide({
      stdout: (text) => {
        outElement.value += text + "\n";
        outElement.scrollTop = outElement.scrollHeight;
      },
      stderr: (text) => {
        outElement.value += `\n[STDERR]: ${text}\n`;
      },
    });

    // 2. No more FETCH! Use the imported strings directly.
    pyodide.FS.writeFile("assembler.py", assemblerSource);
    pyodide.FS.writeFile("emulator.py", emulatorSource);

    console.log("Finished runtime initialization");
    outElement.value = "Ready.\n";
    startBtn.disabled = false;
    startBtn.innerText = "START";
  } catch (err) {
    console.error("Init failed:", err);
    outElement.value = "FATAL ERROR: Could not load Pyodide.";
  }
}

async function exec() {
  if (!pyodide) return;

  const outElement = document.getElementById("stdout");
  const asmElement = document.getElementById("asm");

  // Sync the textarea to the virtual disk
  pyodide.FS.writeFile("code.s16", asmElement.value, { encoding: "utf8" });

  try {
    // Run the main runtime source we imported at the top
    await pyodide.runPythonAsync(runtimeSource);
  } catch (err) {
    outElement.value += `\n\nPYTHON ERROR:\n${err}`;
  }
}

document.getElementById("start").addEventListener("click", exec);
init();
