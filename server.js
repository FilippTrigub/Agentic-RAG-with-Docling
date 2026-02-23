const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

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
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .container {
      text-align: center;
      background: white;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
      color: #333;
      margin: 0;
    }
    .banner {
      background-color: #4CAF50;
      color: white;
      padding: 15px;
      margin-top: 20px;
      border-radius: 5px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome to Our Landing Page</h1>
    ${foobarSet ? '<div class="banner">foobar is set</div>' : ''}
  </div>
</body>
</html>
  `;

  res.send(html);
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
