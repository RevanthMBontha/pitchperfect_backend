import { spawn } from "child_process";
import { join } from "path";

export const ttsService = (script, voice) => {
  return new Promise((resolve, reject) => {
    const venvScriptPath = join("python", "venv", "bin", "python");
    const pythonScriptPath = join("python", "tts", "tts.py");

    const python = spawn(venvScriptPath, [
      pythonScriptPath,
      script,
      voice,
      process.env.OPENAI_API_KEY,
    ]);

    let audioPath = "";

    python.stdout.on("data", (data) => {
      const result = data.toString().trim();
      if (result.endsWith(".mp3")) {
        audioPath = result;
      }
    });

    python.stderr.on("data", (data) => {
      console.error("[Python error]:", data.toString());
    });

    python.on("close", (code) => {
      if (code === 0 && audioPath) {
        resolve(audioPath);
      } else {
        reject(new Error("Python script failed or returned no output."));
      }
    });
  });
};
