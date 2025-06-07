# Product Requirements Document: Contextual Photo Search

## 1. Introduction/Overview

This document outlines the requirements for a Command-Line Interface (CLI) tool that enables contextual, natural language search for a user's personal photo library. The system will analyze photos from the user's Apple Photos library using a visual Large Language Model (VLLM) to generate rich text descriptions. These descriptions will then be used to match against natural language search queries, allowing the user to find photos based on their content rather than just metadata like dates or locations.

## 2. Goals

*   **Enable Contextual Search:** Allow users to search their photo library using descriptive, natural language queries (e.g., "photos from my mountain trip").
*   **Automate Photo Tagging:** Automatically generate detailed descriptions for each photo, removing the need for manual tagging.
*   **Improve Discoverability:** Provide a fast and intuitive way for a user to find specific photos without remembering exact dates or file names.
*   **Personal Use Focus:** Create a tool tailored for a single user's personal photo management workflow.

## 3. User Stories

*   **As a photographer,** I want to automatically generate descriptions for all the photos in my Apple Photos library so that I don't have to spend hours manually tagging them.
*   **As a photographer,** I want to search for my photos using phrases like "pictures of sunsets at the beach" so that I can quickly find them for my portfolio.
*   **As a photographer,** I want to use a CLI to index and search my photos so I can easily integrate it into my existing scripts and technical workflows.

## 4. Functional Requirements

1.  **Photo Library Integration:** The system must be able to connect to and read from the user's local Apple Photos library on macOS.
2.  **Image Analysis:** The system must iterate through each photo in the library and send it to a user-specified VLLM for analysis.
3.  **Description Storage:** The system must store the generated text description for each photo in a local database, linking it to a unique identifier for the photo.
4.  **Indexing Command:** The system must provide a CLI command to initiate the process of analyzing the photo library and storing the descriptions. This command should be able to handle new photos and avoid re-processing existing ones unless specified.
5.  **Search Command:** The system must provide a CLI command that accepts a natural language string as a search query.
6.  **Search Execution:** The search command must query the stored descriptions to find photos that semantically match the user's query.
7.  **Displaying Results:** The search results must be displayed in the terminal, showing the file paths or identifiers of the matching photos.

## 5. Non-Goals (Out of Scope)

*   A graphical user interface (web, desktop, or mobile).
*   Any photo editing or modification capabilities.
*   Multi-user accounts or cloud synchronization features.
*   Support for photo libraries other than Apple Photos in the initial version.
*   Hosting, managing, or providing the VLLM. The user is responsible for providing access to a VLLM.

## 6. Design Considerations

*   The CLI output for both indexing and searching should be clear, human-readable, and well-formatted.
*   A progress bar or status indicator should be displayed during the library indexing process, as it may be long-running.
*   Search results should be ranked by relevance.

## 7. Technical Considerations

*   A library such as `osxphotos` should be considered for interfacing with the Apple Photos library.
*   A simple, file-based database like SQLite is recommended for storing the photo descriptions and metadata locally.
*   The system will require a clear configuration method (e.g., a config file or environment variables) for the user to provide the VLLM's API endpoint and credentials.
*   The choice of text embedding model and vector search strategy will be critical for the quality of the semantic search results.

## 8. Success Metrics

*   The system can successfully index a library of over 10,000 photos without crashing.
*   A search query returns relevant results in under 3 seconds on an indexed library.
*   The primary user can successfully find photos for at least 90% of their test queries.

## 9. Open Questions

*   What is the specific API contract for the VLLM? (e.g., REST endpoint, required headers, request/response format).
*   How should the system handle updates? If a photo is deleted from Apple Photos, should its description be removed from the database?
*   What is the preferred format for displaying search results in the CLI? (e.g., a list of file paths, image thumbnails using a library like `viuer`). 