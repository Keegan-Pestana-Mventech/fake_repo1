from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
import traceback

# FORCE UTF-8 STREAMS (Fixes Windows Encoding Crashes)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Get API name from environment or default
API_NAME = os.environ.get("API_NAME", "Test API")

# Test pandas import
print(f"[{API_NAME}] Testing pandas import...")
pandas_available = False
numpy_available = False

try:
    import pandas as pd
    pandas_available = True
    print(f"[{API_NAME}] [OK] pandas imported successfully")
    print(f"[{API_NAME}] pandas version: {pd.__version__}")
except ImportError as e:
    print(f"[{API_NAME}] [WARNING] pandas import failed: {e}")
    pandas_available = False

print(f"[{API_NAME}] numpy_available: {numpy_available}")
print(f"[{API_NAME}] pandas_available: {pandas_available}")

# Create FastAPI app
app = FastAPI(title=API_NAME, version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - basic connectivity check"""
    return {
        "status": "ok",
        "message": f"{API_NAME} is running",
        "api_name": API_NAME
    }

@app.get("/health")
async def health():
    """Health check endpoint - used by frontend validation"""
    return {
        "status": "healthy",
        "api_name": API_NAME,
        "message": "All systems operational",
        "numpy_available": numpy_available,
        "pandas_available": pandas_available
    }

@app.get("/debug/imports")
async def debug_imports():
    """Debug endpoint to check import status"""
    import_status = {
        "numpy": {
            "available": numpy_available,
            "version": None,
            "path": None
        },
        "pandas": {
            "available": pandas_available,
            "version": pd.__version__ if pandas_available else None,
            "path": pd.__file__ if pandas_available else None
        }
    }
    return {
        "api_name": API_NAME,
        "imports": import_status,
        "python_version": sys.version,
        "executable": sys.executable
    }

@app.get("/debug/routes")
async def debug_routes():
    """Debug endpoint to list all registered routes"""
    routes = []
    for route in app.routes:
        if hasattr(route, "path"):
            routes.append({
                "path": route.path,
                "name": route.name if hasattr(route, "name") else None,
                "methods": list(route.methods) if hasattr(route, "methods") else []
            })
    return {
        "api_name": API_NAME,
        "total_routes": len(routes),
        "routes": routes
    }

@app.get("/info")
async def info():
    """Detailed API information"""
    return {
        "api_name": API_NAME,
        "version": "1.0.0",
        "numpy_available": numpy_available,
        "pandas_available": pandas_available,
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/info", "method": "GET", "description": "API information"},
            {"path": "/test", "method": "GET", "description": "Test endpoint with sample data"},
            {"path": "/debug/imports", "method": "GET", "description": "Import status"},
            {"path": "/debug/routes", "method": "GET", "description": "Registered routes"},
            {"path": "/shutdown", "method": "GET", "description": "Shutdown endpoint"},
        ]
    }

@app.get("/test")
async def test():
    """Test endpoint with sample data"""
    print(f"[{API_NAME}] /test endpoint called")
    print(f"[{API_NAME}] numpy_available: {numpy_available}")
    print(f"[{API_NAME}] pandas_available: {pandas_available}")
    
    # Test with pandas DataFrame if available
    if pandas_available:
        try:
            print(f"[{API_NAME}] Processing data with pandas DataFrame...")
            
            # Create sample DataFrame
            data = {
                'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
                'Age': [25, 30, 35, 28, 32],
                'City': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'],
                'Salary': [50000, 60000, 70000, 55000, 65000]
            }
            
            df = pd.DataFrame(data)
            
            # Perform some DataFrame operations
            average_age = df['Age'].mean()
            average_salary = df['Salary'].mean()
            total_records = len(df)
            
            # Get summary statistics
            age_stats = df['Age'].describe().to_dict()
            salary_stats = df['Salary'].describe().to_dict()
            
            data_payload = {
                "dataframe_sample": df.head().to_dict('records'),
                "summary": {
                    "total_records": total_records,
                    "average_age": float(average_age),
                    "average_salary": float(average_salary)
                },
                "statistics": {
                    "age_stats": {k: float(v) if isinstance(v, (int, float)) else v 
                                for k, v in age_stats.items()},
                    "salary_stats": {k: float(v) if isinstance(v, (int, float)) else v 
                                   for k, v in salary_stats.items()}
                }
            }
            data_type = "pandas_dataframe"
            print(f"[{API_NAME}] [OK] Pandas DataFrame processing successful")
            
            response = {
                "status": "success",
                "api_name": API_NAME,
                "data_type": data_type,
                "data": data_payload,
                "message": f"This is test data from {API_NAME} using pandas DataFrame"
            }
        except Exception as e:
            print(f"[{API_NAME}] [ERROR] Pandas DataFrame processing failed: {e}")
            traceback.print_exc()
            response = {
                "status": "error",
                "api_name": API_NAME,
                "data_type": "error",
                "data": {"error": f"Pandas processing failed: {e}"},
                "message": f"Error in {API_NAME}",
                "error_details": {
                    "stage": "pandas_processing",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
            }
    else:
        # Fallback to pure Python processing
        try:
            print(f"[{API_NAME}] Processing data with pure Python...")
            sample_list = [1, 2, 3, 4, 5]
            processed_data = [x * 10 for x in sample_list]
            data_payload = {
                "original": sample_list,
                "processed": processed_data,
                "sum": sum(processed_data),
                "count": len(processed_data)
            }
            data_type = "pure_python"
            print(f"[{API_NAME}] [OK] Data processing successful")
            
            response = {
                "status": "success",
                "api_name": API_NAME,
                "data_type": data_type,
                "data": data_payload,
                "message": f"This is test data from {API_NAME} (pandas not available)"
            }
        except Exception as e:
            print(f"[{API_NAME}] [ERROR] Data processing failed: {e}")
            traceback.print_exc()
            response = {
                "status": "error",
                "api_name": API_NAME,
                "data_type": "error",
                "data": {"error": f"Processing failed: {e}"},
                "message": f"Error in {API_NAME}",
                "error_details": {
                    "stage": "processing",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
            }
    
    return response

@app.get("/shutdown")
async def shutdown():
    """Graceful shutdown endpoint"""
    print(f"[{API_NAME}] Received shutdown request")
    print(f"[{API_NAME}] Performing cleanup...")
    print(f"[{API_NAME}] Shutdown complete")
    os._exit(0)

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"[{API_NAME}] Invalid port argument: {sys.argv[1]}, using default 8000")
    
    print(f"[{API_NAME}] Starting on port {port}...")
    print(f"[{API_NAME}] API_NAME: {API_NAME}")
    print(f"[{API_NAME}] Python: {sys.version}")
    print(f"[{API_NAME}] Executable: {sys.executable}")
    print(f"[{API_NAME}] Health check: http://127.0.0.1:{port}/health")
    print(f"[{API_NAME}] Test data: http://127.0.0.1:{port}/test")
    print(f"[{API_NAME}] Debug imports: http://127.0.0.1:{port}/debug/imports")
    print(f"[{API_NAME}] Debug routes: http://127.0.0.1:{port}/debug/routes")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
        log_level="info"
    )