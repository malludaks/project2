if __name__ == "__main__":
    print("Testing expired key retrieval...")
    expired_key = get_private_key(expired=True)
    if expired_key:
        print("Successfully retrieved an expired key.")
    else:
        print("No expired key could be retrieved.")
