# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## How to get the projet running 

1. Run in terminal: check for python and node.js versions 
$ python --version
Python 3.12.7
$ node --version
v22.11.0

2. Create vite/react project
   npm create vite@latest react-with-flask -- --template react

3. Switch to ecinemabookingsys and to run the vite/react app:
   $ npm install
   $ npm run dev

4. when inside ecinemabookingsys directory, run:
   bash -> source venv/bin/activate
   windows (cmd/poweshell) -> venv\Scripts\activate

5. install flask dependencies:
   pip install flask python-dotenv

6. create .env file inside of ecinemabookingsys directory, and add these two lines:
   FLASK_APP=api.py
   FLASK_ENV=development

7. Open the file vite.config.js and add the server section, along with its proxy sub-section:
   ```
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

    // https://vite.dev/config/
    export default defineConfig({
     plugins: [react()],
      server: {
        proxy: {
          '/api': 'http://localhost:5001',
        },
       },
     })
    ```
8. Open the file package.json and find the scripts section. This is where all the React commands are configured. In this section, add a api command defined as follows:
```
  // ...
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "api": "cd api && venv/bin/flask run --no-debugger"
  },
  // ...
```
