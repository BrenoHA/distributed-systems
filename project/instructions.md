# Interactions:

## 1. **Create File (Client → Server)**

- **Action**: The client sends a request to the server to create a new file with a specified name and path.
  - **Request**: `CREATE {file_name, file_path}`
  - **Server checks**:
    - If a file already exists with the same name at the specified path:
      - **Response**: `Failure: File already exists`
    - If the path is valid and the file doesn't exist:
      - **Response**: `Success: File created successfully`

## 2. **Read File (Client → Server)**

- **Action**: The client requests to read the contents of a file with a specified name at a given path.
  - **Request**: `READ {file_name, file_path}`
  - **Server checks**:
    - If the file exists at the specified path:
      - **Response**: `Success: File content` (with the file data)
    - If the file doesn’t exist:
      - **Response**: `Failure: File not found`

## 3. **Update File (Client → Server)**

- **Action**: The client requests to update the content of a file with a specified name at a given path.
  - **Request**: `UPDATE {file_name, file_path, new_content}`
  - **Server checks**:
    - If the file exists at the specified path:
      - **Response**: `Success: File updated successfully`
    - If the file doesn’t exist:
      - **Response**: `Failure: File not found`

## 4. **Delete File (Client → Server)**

- **Action**: The client requests to delete a file with a specified name at a given path.
  - **Request**: `DELETE {file_name, file_path}`
  - **Server checks**:
    - If the file exists at the specified path:
      - **Response**: `Success: File deleted successfully`
    - If the file doesn’t exist:
      - **Response**: `Failure: File not found`

## 5. **File Metadata (Client → Server)**

- **Action**: The client requests the metadata of a file with a specified name at a given path.
  - **Request**: `GET_METADATA {file_name, file_path}`
  - **Server checks**:
    - If the file exists at the specified path:
      - **Response**: `Success: Metadata {size, last_modified, etc.}`
    - If the file doesn’t exist:
      - **Response**: `Failure: File not found`

## 6. **File Path Validation (Server side)**

- **Action**: Server validates the file path before any operation.
  - **Request**: `Validation {file_name, file_path}`
  - **Server checks**:
    - If the file path is valid and accessible:
      - **Response**: `Valid path`
    - If the file path is invalid (e.g., directory not found, wrong format):
      - **Response**: `Invalid path`

## 7. **General Error Handling**

- For any unexpected failures or server errors:
  - **Response**: `Failure: Internal server error` or `Failure: Invalid request format`
