# 🚀 Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Node.js 18+ installed (`node --version`)
- ✅ Python 3.9+ installed (`python --version`)
- ✅ Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Step-by-Step Setup

### 1️⃣ Backend Setup (5 minutes)

```powershell
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file from example
copy ..\.env.example .env

# Edit .env file and add your Gemini API key
# Open .env in notepad and replace 'your_gemini_api_key_here' with your actual key
notepad .env
```

### 2️⃣ Frontend Setup (5 minutes)

```powershell
# Open a new terminal
# Navigate to frontend directory
cd frontend

# Install Node dependencies (this may take a few minutes)
npm install

# Create .env file
copy .env.example .env
```

### 3️⃣ Running the Application

**Option A: Using Two Terminals (Recommended)**

Terminal 1 - Backend:
```powershell
cd backend
python main.py
```
You should see: `Uvicorn running on http://0.0.0.0:8000`

Terminal 2 - Frontend:
```powershell
cd frontend
npm run dev
```
You should see: `Local: http://localhost:5173/`

**Option B: Using PowerShell Script (Coming Soon)**

### 4️⃣ Access the Application

Open your browser and go to:
```
http://localhost:5173
```

## Troubleshooting

### PowerShell Script Execution Error

If you see "running scripts is disabled on this system":

```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Backend Won't Start

**Error: "GEMINI_API_KEY not found"**
- Solution: Make sure you created `.env` file in the backend directory with your API key

**Error: "Module not found"**
- Solution: Run `pip install -r requirements.txt` again

### Frontend Won't Start

**Error: "Cannot find module"**
- Solution: Delete `node_modules` folder and run `npm install` again

**Error: "Port 5173 is already in use"**
- Solution: Kill the process using port 5173 or change the port in `vite.config.js`

### Connection Issues

**Error: "Unable to connect to the server"**
- Solution: Make sure backend is running on port 8000
- Check: Visit http://localhost:8000/health in your browser

## Testing the Application

1. **Paste Sample Text**: Copy this sample text:
   ```
   Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
   ```

2. **Select Length**: Choose "Medium"

3. **Click Summarize**: Wait 2-3 seconds for the AI-generated summary

4. **Test Features**:
   - ✅ Copy the summary
   - ✅ Regenerate for a different version
   - ✅ Clear and try with different text

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🎨 Customize the design in `frontend/src/index.css`
- 🔧 Modify prompts in `backend/main.py`
- 🚀 Deploy to production (see R2 roadmap)

## Need Help?

- Check the [README.md](README.md) troubleshooting section
- Review the [TRACKING.md](TRACKING.md) for development status
- Create an issue in the repository

---

**Enjoy your AI Text Summarization Agent! 🎉**
