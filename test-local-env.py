import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_package_imports():
    """Test if all required packages can be imported successfully."""
    packages = [
        "fastapi",
        "dotenv",
        "databricks.sdk",
        "psycopg2",
    ]

    print("Testing package imports...")
    failed_imports = []

    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {package}: {e}")
            failed_imports.append(package)

    if failed_imports:
        print(
            f"\n❌ {len(failed_imports)} package(s) failed to import: {', '.join(failed_imports)}"
        )
        return False
    else:
        print("\n✅ All packages imported successfully!")
        return True


def test_python_environment():
    """Test Python environment and binary path."""
    print("\nTesting Python environment...")

    # Get Python executable path
    python_executable = sys.executable
    print(f"✓ Python executable: {python_executable}")

    # Get current working directory
    cwd = os.getcwd()
    print(f"✓ Current working directory: {cwd}")

    # Check if we're using a virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✓ Running in a virtual environment")
        venv_active = True
    else:
        print("⚠️  Not running in a virtual environment")
        venv_active = False

    # Check if .venv exists and if we're using it
    venv_path = Path(".venv")
    if venv_path.exists():
        if venv_path.is_dir():
            print("✓ .venv folder exists")
            # Check if we're using the .venv Python
            if str(venv_path) in python_executable:
                print("✓ Using Python from .venv folder")
                return True
            else:
                print("⚠️  .venv folder exists but not using its Python")
                return False
        else:
            print("❌ .venv exists but is not a directory")
            return False
    else:
        print("❌ .venv folder does not exist")
        return False


def test_env_file():
    """Test if .env file exists and has all required values from example.env."""
    print("\nTesting .env file...")

    # Check if .env file exists
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file does not exist")
        return False

    print("✓ .env file exists")

    # Read example.env to get required keys
    example_env_path = Path("example.env")
    if not example_env_path.exists():
        print("❌ example.env file does not exist")
        return False

    # Parse example.env to get required keys (skip comments and empty lines)
    required_keys = []
    with open(example_env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key = line.split("=")[0]
                required_keys.append(key)

    print(f"✓ Found {len(required_keys)} required environment variables in example.env")

    # Check if .env has all required keys with non-empty values
    missing_keys = []
    empty_keys = []
    invalid_values = []

    with open(env_path, "r") as f:
        env_content = f.read()

    for key in required_keys:
        if key not in env_content:
            missing_keys.append(key)
        else:
            # Check if the key has a value (not just the key name)
            lines = env_content.split("\n")
            for line in lines:
                if line.startswith(f"{key}="):
                    value = line.split("=", 1)[1].strip()
                    if not value or value in [
                        "<your-full-databricks-email>",
                        "<RETRIEVE-FROM-BOTTOM-CELL-OF-NOTEBOOK-IN-NEXT-STEP>",
                        "''",
                        '""',
                    ]:
                        empty_keys.append(key)
                    else:
                        # Specific validation for MY_EMAIL and DATABRICKS_CLIENT_SECRET
                        if key == "MY_EMAIL":
                            if not value.lower().endswith("@databricks.com"):
                                invalid_values.append(
                                    f"{key} must end with @databricks.com (case-insensitive)"
                                )
                        elif key == "DATABRICKS_CLIENT_SECRET":
                            if not value.startswith("dose"):
                                invalid_values.append(
                                    f"{key} must start with 'dose', so it can't be a databricks client secret"
                                )
                    break

    if missing_keys:
        print(f"❌ Missing keys in .env: {', '.join(missing_keys)}")
        return False

    if empty_keys:
        print(f"❌ Empty or placeholder values in .env: {', '.join(empty_keys)}")
        return False

    if invalid_values:
        print(f"❌ Invalid values in .env: {', '.join(invalid_values)}")
        return False

    print("✅ .env file has all required values filled in!")
    return True


def test_env_vars():
    """Test if required environment variables are available."""
    required_vars = [
        "LAKEBASE_INSTANCE_NAME",
        "LAKEBASE_DB_NAME",
        "DATABRICKS_CLIENT_ID",
        "DATABRICKS_CLIENT_SECRET",
        "DATABRICKS_HOST",
        "MY_EMAIL",
    ]

    print("\nTesting environment variables...")
    all_present = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(
                f"✓ {var}: {value[:10]}..."
                if len(str(value)) > 10
                else f"✓ {var}: {value}"
            )
        else:
            print(f"✗ {var}: NOT FOUND")
            all_present = False

    return all_present


def main():
    """Main test function."""
    print("🧪 Running test script...\n")

    # Test Python environment
    python_ok = test_python_environment()

    # Test package imports
    packages_ok = test_package_imports()

    # Test .env file
    env_ok = test_env_file()

    # Test environment variables
    vars_ok = test_env_vars()

    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)

    if packages_ok and python_ok and env_ok and vars_ok:
        print("🎉 All tests passed! Your environment is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
