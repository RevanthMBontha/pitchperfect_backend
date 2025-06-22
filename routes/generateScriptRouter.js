import { Router } from "express";
import { generateScriptController } from "../controllers/generateScriptController.js";

const router = Router();

router.post("/", generateScriptController);

export default router;
