import { exec } from "child_process";
import path from "path";

export const mergeAudioWithVideo = (videoPath, audioPath, outputName) => {
  return new Promise((resolve, reject) => {
    const outputPath = path.join("public/stitched", outputName);
    const cmd =
      `ffmpeg -i video.mp4 -i audio.mp3 -c:v h264 -c:a aac -shortest output.mp4`
        .replace("video.mp4", videoPath)
        .replace("audio.mp3", audioPath)
        .replace("output.mp4", outputPath);

    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.error("[FFmpeg Error]", stderr);
        return reject(error);
      }
      console.log("✅ Merged video saved to", outputPath);
      resolve(outputPath);
    });
  });
};
