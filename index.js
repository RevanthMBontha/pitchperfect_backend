import express, { json } from "express";
import morgan from "morgan";
import cors from "cors";
import "dotenv/config";
import generateScriptRouter from "./routes/generateScriptRouter.js";
import urlScraperRouter from "./routes/urlScraperRouter.js";
import generateVideoRouter from "./routes/videoGenRouter.js";
import path from "path";

const app = express();

app.use(cors());
app.use(morgan("dev"));
app.use(json());

const port = process.env.PORT || 3000;

app.use("/public", express.static(path.join("public")));

app.use("/api/v1/scrape-product-url", urlScraperRouter);

app.use("/api/v1/generate-script", generateScriptRouter);

app.use("/api/v1/generate-video", generateVideoRouter);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
