from fastapi import HTTPException
class FieldValidationMiddleware:
    async def validate_input_login(request):
        try:
            data = await request.form()
            print(data)
            print(type(data['username']))
            if type(data['username']) is not str:
                raise HTTPException(status_code=400, detail=f"Value for key username must be a string")
            if type(data['password']) is not str:
                raise HTTPException(status_code=400, detail=f"Value for key username must be a string")
            if data["username"]=="" or data["password"]=="":
                raise HTTPException(status_code=400,detail=f"value for key username or password cannot be null")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid JSON data")



    # async def validate_input_login(request):
    #     try:
    #         data = await request.form()
    #         print(data)
    #         print(type(data['username']))
    #         if type(data['username']) is not str:
    #             raise HTTPException(status_code=400, detail=f"Value for key username must be a string")
    #         if type(data['password']) is not str:
    #             raise HTTPException(status_code=400, detail=f"Value for key username must be a string")
    #         if data["username"]=="" or data["password"]=="":
    #             raise HTTPException(status_code=400,detail=f"value for key username or password cannot be null")
    #     except ValueError:
    #         raise HTTPException(status_code=400, detail="Invalid JSON ")
 

    # async def validate_protected_route_developer(request):
    #     try:
    #         data = await request.json()
    #         print(type(data['token']))
    #         if type(data['token']) is not str:
    #                 raise HTTPException(status_code=400, detail=f"Value for key token must be a string")
    #         if data["token"]=="":
    #                  raise HTTPException(status_code=400,detail=f"value for key token cannot be null")
    #     except ValueError:
    #         raise HTTPException(status_code=400, detail="Invalid JSON data")

    
    # async def validate_protected_route_admin(request):
    #     try:
    #         data = await request.json()
    #         print(data)
    #         for key, value in data.items():
    #             if not isinstance(value, str):
    #                 raise HTTPException(status_code=400, detail=f"Value for key '{key}' must be a string")
    #             if data["token"]=="":
    #                  raise HTTPException(status_code=400,detail=f"value for key token cannot be null")
    #     except ValueError:
    #         raise HTTPException(status_code=400, detail="Invalid JSON data")
