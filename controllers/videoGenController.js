import { mergeAudioWithVideo } from "../services/stitchService.js";
import { ttsService } from "../services/ttsService.js";
import { generateVideoService } from "./../services/videoGenService.js";
import { parseFile } from "music-metadata";
import { unlink } from "fs/promises";

const getAudioDuration = async (filePath) => {
  try {
    const metadata = await parseFile(filePath);
    const duration = metadata.format.duration; // duration in seconds
    console.log(`Audio duration: ${duration.toFixed(2)} seconds`);
    return duration;
  } catch (err) {
    console.error("Failed to get audio duration:", err.message);
  }
};

export const generateVideoController = async (req, res) => {
  try {
    // Audio Parameters
    const script = req.body.script;
    const voice = "echo";

    const audioName = await ttsService(script, voice);
    const audioFullPath = `public/audios/${audioName}`;
    const audio_duration = await getAudioDuration(audioFullPath);

    // Video Parameters
    const images = req.body.images;
    const orientation = req.body.orientation;

    console.log("Audio Duration:", audio_duration);

    const videoPath = await generateVideoService(
      images,
      orientation,
      audio_duration
    );
    const videoFullPath = `public/videos/${videoPath}`;

    const outputName = `${Date.now()}.mp4`;

    const outputPath = await mergeAudioWithVideo(
      videoFullPath,
      audioFullPath,
      outputName
    );

    try {
      await unlink(audioFullPath);
      console.log("🗑️ Audio File deleted successfully");
    } catch (err) {
      console.error("❌ Error deleting audio file:", err);
    }

    try {
      await unlink(videoFullPath);
      console.log("🗑️ Video File deleted successfully");
    } catch (err) {
      console.error("❌ Error deleting video file:", err);
    }

    res.status(200).json({
      success: true,
      message: "Merged successfully",
      videoPath: outputPath,
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};
