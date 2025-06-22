# Backend

- Clone the repository.
- Use `npm install` to install all the dependencies
- Use `npm run start` to spin up the dev server.
- This runs an intermediate command `npm run build-python` which installs a _python venv_ in the `/python` folder. This step is crucial for the services to run, most of which spawn a python process that executes tasks.

## What to Expect

- The server consists of the routers, controllers, services, and then a python layer of processes that are executed as if on a cli.
- The major routes are:
  - api/v1/scrape-product-url : Used to call the python process that scrapes the URL and returns the details
  - /api/v1/generate-script : Used to generate scripts based on a keyword
  - /api/v1/generate-video : Used to generate audio and video and then stitch the two together
- There are multiple services that each spawn a specific python process. I decided to go by this approach to get the sweet spot between using Node and Express for the server, which is very fast and efficient, with the power of python which is the best when it comes to scraping, and working with any sort of Machine Learning or Artificial Intelligence problems.

## TechStack Used

- Node with Express for the server
- Python for low level interactions like scraping and generating prompts and video
- BeautifulSoup for web scraping
- Open AI GPT 4o model to generate the script from the product details
- Open AI TTS for converting the script to speech
- CV2 to create the video from the product images
- FFmpeg to stitch the audio and video together to get the final video output.
- Other common libraries used include ones like morgan, cors, dotenv, etc that are part of most servers.

## .env file

- Create a file called `.env` at the root folder
- The following need to be added to the file:
  - PORT : The port number that the backend runs on. Keep this as `8080` for smooth functionality.
  - OPENAI_API_KEY : OpenAI API key for generating the prompts and TTS services.

## Conclusion

After a lot of thinking, I went with this approach of using Python for low-level interactivity with data, and Express for the high level web server as I felt it provided the best of both worlds. Having to use only Fast API or only Express came with challenges of their own which are mitigated with this approach. Also this allowed me to flex my thinking muscles and come up with solutions that are out of the norm but still perform extremely well. The average time to generate a video was anywhere between 25 and 45 seconds which is pretty good considering all the tasks are happening on local machine that does not have the computational capabilities as a full blown server.
