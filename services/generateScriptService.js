import { spawn } from "child_process";
import { join } from "path";

export const generateScriptService = (
  product_details,
  script_type,
  duration
) => {
  if (!product_details || !script_type || !duration) {
    throw new Error(
      "Missing required parameters: product_details, script_type, or duration"
    );
  }

  return new Promise((resolve, reject) => {
    const venvScriptPath = join("python", "venv", "bin", "python");
    const scriptPath = join("python", "prompt", "prompt.py");
    console.log(process.env.OPENAI_API_KEY);
    console.log("###########################################");
    const python = spawn(venvScriptPath, [
      scriptPath,
      JSON.stringify(product_details),
      script_type,
      duration,
      process.env.OPENAI_API_KEY,
    ]);

    let output = "";
    let errorOutput = "";

    // TODO: Add custom input data
    // python.stdin.write(JSON.stringify({}))

    // python.stdin.end();

    python.stdout.on("data", (data) => {
      output += data.toString();
    });

    python.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    python.on("close", (code) => {
      if (code === 0) {
        resolve(output.trim());
      } else {
        reject(new Error(`Python script failed: ${errorOutput}`));
      }
    });
  });
};
