# Deploy to Render - Simple Step-by-Step Guide

## Step 1: Prepare Your Code (Already Done! ✅)
Your project is ready with:
- ✅ `requirements.txt` - All dependencies listed
- ✅ `Procfile` - Instructions for Render
- ✅ `runtime.txt` - Python version specified
- ✅ `.gitignore` - Unnecessary files ignored
- ✅ `settings.py` - Updated for production

## Step 2: Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 3: Create Account on Render
1. Go to https://render.com
2. Sign up with GitHub (click "Sign up with GitHub")
3. Authorize Render to access your GitHub account

## Step 4: Create New Web Service
1. Click **"+ New"** button (top right)
2. Select **"Web Service"**
3. Select your GitHub repository: `appointment_system`
4. Click **"Connect"**

## Step 5: Configure Your Service

### Fill in the form:
- **Name**: `appointment-system` (or any name)
- **Environment**: `Python 3`
- **Region**: Keep default or choose your region
- **Branch**: `main`
- **Build Command**: 
  ```
  pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
  ```
- **Start Command**:
  ```
  gunicorn appointment_booking.wsgi
  ```

## Step 6: Add Environment Variables

Click **"Advanced"** at the bottom and add these:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` (you'll get this after deploy) |
| `SECRET_KEY` | Generate a new one: `django-insecure-` + random string (or use Django's command) |

## Step 7: Deploy
1. Click **"Create Web Service"**
2. Render will start deploying (takes 2-3 minutes)
3. Wait for "Your service is live on https://your-app-name.onrender.com"

## Step 8: Create Admin Account
Once deployed, run this command in Render's shell:
1. Go to your service dashboard
2. Click **"Shell"** tab
3. Run:
   ```
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin username/password

## Step 9: Access Your App
- **Main App**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`

## Important Notes

⚠️ **Free Tier Limitations:**
- Your app spins down after 15 minutes of inactivity
- First request after idle takes 30 seconds to respond
- Limited storage for database

✅ **When You're Live:**
- Update `ALLOWED_HOSTS` in Render dashboard with actual domain
- Your app will auto-deploy on every `git push`

## Troubleshooting

**App won't start?**
- Check **Logs** tab in Render dashboard
- Common issues: wrong SECRET_KEY, database errors

**Static files not loading?**
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` in settings.py

**Login not working?**
- Create admin account again
- Check database is created with migrations

---

Need help? Check: https://render.com/docs/deploy-django
