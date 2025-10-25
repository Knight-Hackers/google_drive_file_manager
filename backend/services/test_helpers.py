from drive_service import get_drive_service, list_files

Access_Token = "ya29.a0ATi6K2vrEjs6bgRpYAeerRka2fENXmHtehExpz5rOfYfVm9uNGyh4LmaY0Q5jZnVw44BNECiTSLEa4jWnJIUQrsWNx_QnaJTyUOTDEby5_RzV2k8ZAM_DEolwE2Y1tpySGpOVJA93zF2z3_3qw1WvbTWtzQdQP-dIHT11QzfGvAC0N_OAmDwO-TT7zKa5FxygZKITUkaCgYKAaMSARUSFQHGX2MiNIbfYR0hg2pGqe4PaRkZ1g0206"


def test_drive_api():
    try: 
        service = get_drive_service(Access_Token)
        print("Drive service created successfully.")

        files = list_files(service)
        print(f"Retrived {len(files)} files")

        for file in files:
            print(f"File Name: {file['name']}, ID: {file['id']}")
    except Exception as e:
        print("error: ", e)
    
if __name__ == "__main__":
    test_drive_api()