import { Router } from "express";
import { scrapeProductURLController } from "../controllers/urlScraperController.js";

const urlScraperRouter = Router();
urlScraperRouter.get("/", scrapeProductURLController);

export default urlScraperRouter;
