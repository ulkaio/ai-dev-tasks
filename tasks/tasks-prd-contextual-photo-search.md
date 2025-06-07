## Relevant Files

- `src/photo_search/main.py` - The main CLI application entry point using Typer.
- `src/photo_search/photos_service.py` - Service to interact with the Apple Photos library.
- `src/photo_search/vllm_service.py` - Service to communicate with the external VLLM.
- `src/photo_search/database.py` - Handles all database interactions (e.g., SQLite).
- `src/photo_search/config.py` - Manages configuration from environment variables or a config file.
- `tests/test_photos_service.py` - Unit tests for `photos_service.py`.
- `tests/test_vllm_service.py` - Unit tests for `vllm_service.py`.
- `tests/test_database.py` - Unit tests for `database.py`.
- `pyproject.toml` - Project metadata and dependencies managed by `uv`.
- `README.md` - Project documentation.
- `.gitignore` - Standard Python .gitignore file.
- `.env.example` - Example environment file for configuration.
- `.github/workflows/ci.yml` - GitHub Actions configuration for CI/CD.

### Notes

- Unit tests should be placed in the `tests/` directory.
- Use `uv run pytest` to run tests.
- Use `uv run ruff check .` and `uv run ruff format .` to lint and format the code.

## Tasks

- [x] **1.0 Project Setup & Initialization**
  - [x] 1.1 Create the project directory structure: `src/photo_search`, `tests`.
  - [x] 1.2 Initialize `uv` and create a `pyproject.toml` file with project metadata.
  - [x] 1.3 Add initial dependencies to `pyproject.toml`: `typer`, `rich`, `osxphotos`, `python-dotenv`, `sqlalchemy`, `pytest`, and `ruff`.
  - [x] 1.4 Configure `ruff` within `pyproject.toml` for linting and formatting.
  - [x] 1.5 Create a `.gitignore` file, a `README.md`, and an `.env.example` file.
  - [x] 1.6 Implement a `config.py` module to load settings (like VLLM API keys) from environment variables.

- [x] **2.0 Apple Photos Library Integration**
  - [x] 2.1 Create `src/photo_search/photos_service.py`.
  - [x] 2.2 In the service, implement a function to connect to the Photos database using `osxphotos`.
  - [x] 2.3 Add a function to fetch photos, including their unique IDs and file paths. Handle the case where the library is not found.
  - [x] 2.4 Write unit tests for the `photos_service` in `tests/test_photos_service.py`, mocking the `osxphotos` library.

- [x] **3.0 Image Analysis and Description Generation**
  - [x] 3.1 Create `src/photo_search/vllm_service.py`.
  - [x] 3.2 Implement a function that takes an image file path and sends it to the configured VLLM API endpoint.
  - [x] 3.3 Add logic to handle authentication, timeouts, and potential API errors gracefully.
  - [x] 3.4 Write unit tests for the `vllm_service` in `tests/test_vllm_service.py`, mocking the VLLM API calls.

- [x] **4.0 Database Storage**
  - [x] 4.1 Create `src/photo_search/database.py`.
  - [x] 4.2 Define a database schema using SQLAlchemy Core for a `photos` table (e.g., `id`, `uuid`, `filepath`, `description`).
  - [x] 4.3 Implement functions for initializing the database, inserting/updating photo descriptions, and checking if a photo has already been indexed.
  - [x] 4.4 Implement a function to search for photos based on a text query by matching against the `description` column.
  - [x] 4.5 Write unit tests for the database operations in `tests/test_database.py` using an in-memory SQLite database.

- [x] **5.0 CLI Commands**
  - [x] 5.1 Create `src/photo_search/main.py` using Typer.
  - [x] 5.2 Implement the `index` command, which uses the `photos_service`, `vllm_service`, and `database` module to process the library.
  - [x] 5.3 Add a progress bar from the `rich` library to the `index` command to show progress.
  - [x] 5.4 Implement the `search` command, which takes a query string, uses the `database` module to find photos, and prints the results.
  - [x] 5.5 Ensure the CLI output for search results is clean and readable.

- [x] **6.0 Documentation and Finalization**
  - [x] 6.1 Write PEP 257 compliant docstrings for all modules, functions, and classes.
  - [x] 6.2 Update `README.md` with detailed setup, configuration, and usage instructions for the CLI.
  - [x] 6.3 Create a basic CI pipeline in `.github/workflows/ci.yml` that installs dependencies, runs `ruff`, and executes `pytest`.

- [ ] **7.0 Unit Tests**
  - [ ] 7.1 Implement unit tests for `photos_service.py`.
  - [ ] 7.2 Implement unit tests for `vllm_service.py`.
  - [ ] 7.3 Implement unit tests for `database.py`.

- [x] **8.0 CI/CD**
  - [x] 8.1 Implement GitHub Actions for CI/CD.
  - [x] 8.2 Add project to GitHub Actions.

- [ ] **9.0 Deployment**
  - [ ] 9.1 Implement deployment process.
  - [ ] 9.2 Deploy project to production environment.