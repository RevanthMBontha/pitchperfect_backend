import { spawn } from "child_process";
import { join } from "path";

export const scrapeProductURLService = (url) => {
  console.log("###########################################");
  console.log("Scraping URL:", url);
  console.log("###########################################");

  return new Promise((resolve, reject) => {
    const venvScriptPath = join("python", "venv", "bin", "python");
    const pythonScriptPath = join("python", "url-scraping", "scraper.py");

    const python = spawn(venvScriptPath, [pythonScriptPath, url]);

    let stdoutData = "";
    let stderrData = "";

    python.stdout.on("data", (data) => {
      stdoutData += data.toString();
    });

    python.stderr.on("data", (data) => {
      stderrData += data.toString();
    });

    python.on("close", (code) => {
      if (code === 0) {
        try {
          console.log("Python script output: ", stdoutData);
          const parsed = JSON.parse(stdoutData);
          resolve(parsed);
        } catch (err) {
          reject(
            new Error("Failed to parse JSON from Python output: " + err.message)
          );
        }
      } else {
        console.error("Python script error:", stderrData);
        reject(
          new Error(`Python script exited with code ${code}: ${stderrData}`)
        );
      }
    });
  });
};
