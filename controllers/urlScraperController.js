import { scrapeProductURLService } from "../services/urlScraperService.js";

export const scrapeProductURLController = async (req, res) => {
  const url = req.query.url;

  if (!url) {
    return res.status(400).json({ success: false, message: "URL is required" });
  }

  try {
    const data = await scrapeProductURLService(url);
    res.status(200).json({ success: true, data });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
};
