import { generateScriptService } from "../services/generateScriptService.js";

export const generateScriptController = async (req, res) => {
  try {
    const product_details = req.body.product_details;
    const script_type = req.body.script_type;
    const duration = req.body.duration;

    console.log(typeof product_details);

    const script = await generateScriptService(
      product_details,
      script_type,
      duration
    );
    res.status(200).json({ success: true, script });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message,
      where: "here in controller",
    });
  }
};
