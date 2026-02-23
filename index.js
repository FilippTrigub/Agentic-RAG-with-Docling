import express from 'express';

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  const foobarSet = process.env.NEXT_PUBLIC_FOOBAR ? true : false;

  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Landing Page</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 0;
          padding: 20px;
          background-color: #f5f5f5;
        }
        .container {
          max-width: 800px;
          margin: 0 auto;
          background-color: white;
          padding: 40px;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
          color: #333;
        }
        .banner {
          background-color: #d4edda;
          border: 1px solid #c3e6cb;
          color: #155724;
          padding: 12px 20px;
          border-radius: 4px;
          margin-bottom: 20px;
          font-weight: bold;
        }
      </style>
    </head>
    <body>
      <div class="container">
        ${foobarSet ? '<div class="banner">foobar is set</div>' : ''}
        <h1>Welcome to the Landing Page</h1>
        <p>This is a simple landing page application.</p>
      </div>
    </body>
    </html>
  `;

  res.send(html);
});

app.listen(port, () => {
  console.log(`App running at http://localhost:${port}`);
});
