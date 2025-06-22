import { spawn } from "child_process";
import { join } from "path";

export const generateVideoService = (images, orientation, audioDuration) => {
  console.log("Images: ", images);
  console.log("Orientation: ", orientation);
  console.log("Audio Duration: ", audioDuration);

  return new Promise((resolve, reject) => {
    const venvScriptPath = join("python", "venv", "bin", "python");
    const scriptPath = join("python", "video-gen", "video_gen.py");
    const python = spawn(venvScriptPath, [
      scriptPath,
      JSON.stringify(images),
      orientation,
      audioDuration,
    ]);

    let videoPath = "";
    let stderrData = "";

    python.stdout.on("data", (data) => {
      const result = data.toString().trim();
      if (result.endsWith(".mp4")) {
        videoPath = result;
      }
    });

    python.stderr.on("data", (data) => {
      stderrData += data.toString();
    });

    python.on("close", (code) => {
      if (code === 0) {
        resolve(videoPath);
      } else {
        reject(
          new Error(`Python script failed with code ${code}: ${stderrData}`)
        );
      }
    });
  });
};
