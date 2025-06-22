import { Router } from "express";
const router = Router();
import { generateVideoController } from "./../controllers/videoGenController.js";

router.post("/", generateVideoController);

export default router;
