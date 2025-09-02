# Custom-Canvas-Generator
A simple web application built with Flask that generates custom images based on user-defined width and height dimensions. Access via URL (e.g., /50/60) to create a gray canvas with the dimensions displayed.

## Docker

Build the image:

```bash
docker build -t custom-canvas-generator:latest .
```

Run the container:

```bash
docker run -p 8080:8080 custom-canvas-generator:latest
```

The app will be available at http://localhost:8080.
